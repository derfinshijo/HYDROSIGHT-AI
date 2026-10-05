
import cv2
import numpy as np

def vegetation_mask(image_bgr):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    b, g, r = cv2.split(image_bgr.astype(np.float32))
    exg = 2*g - r - b
    green = exg > 20
    hsv_green = cv2.inRange(
        hsv, np.array([25,35,25], np.uint8),
        np.array([100,255,255], np.uint8)
    ) > 0
    mask = (green & hsv_green).astype(np.uint8)*255
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    cleaned = np.zeros_like(mask)
    min_area = max(30, int(mask.shape[0]*mask.shape[1]*0.0002))
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            cleaned[labels == i] = 255
    return cleaned

def overlay_mask(image, mask):
    out = image.copy()
    layer = np.zeros_like(image)
    layer[:,:,1] = 220
    layer[:,:,0] = 40
    layer[:,:,2] = 30
    idx = mask > 0
    out[idx] = (0.58*out[idx] + 0.42*layer[idx]).astype(np.uint8)
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, (0,255,255), 2)
    return out

def density_label(c):
    return "LOW" if c < 10 else ("MEDIUM" if c < 30 else "HIGH")

def hotspot_grid(mask, rows=2, cols=3):
    h,w = mask.shape
    cells=[]
    for row in range(rows):
        for col in range(cols):
            y0,y1=int(row*h/rows),int((row+1)*h/rows)
            x0,x1=int(col*w/cols),int((col+1)*w/cols)
            cell=mask[y0:y1,x0:x1]
            c=float(np.count_nonzero(cell)/cell.size*100)
            cells.append({"zone":chr(65+row*cols+col),"coverage_percent":round(c,2)})
    ranked=sorted(cells,key=lambda x:x["coverage_percent"],reverse=True)
    for i,c in enumerate(ranked):
        c["priority"]="HIGH" if i==0 else ("MEDIUM" if i==1 else "LOW")
    lookup={c["zone"]:c for c in ranked}
    return [lookup[c["zone"]] for c in cells], ranked[0]

def analyze(image_bgr):
    h,w=image_bgr.shape[:2]
    scale=min(1.0,900/max(h,w))
    if scale < 1:
        image_bgr=cv2.resize(image_bgr,(int(w*scale),int(h*scale)))
    mask=vegetation_mask(image_bgr)
    coverage=float(np.count_nonzero(mask)/mask.size*100)
    zones,top=hotspot_grid(mask)
    return {
        "coverage_percent":round(coverage,2),
        "density":density_label(coverage),
        "target_zone":top["zone"],
        "target_priority":top["priority"],
        "zones":zones,
        "overlay":overlay_mask(image_bgr,mask),
        "detector":"OpenCV vegetation baseline",
        "confidence_note":"Baseline CV estimate; not a trained species/model confidence score."
    }
