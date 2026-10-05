
import base64, io, uuid
import cv2, numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .analytics import analyze
from .guidance import get_guidance

app=FastAPI(title="AquaGuard AI MVP",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

def data_url(img):
    ok,enc=cv2.imencode(".jpg",img,[cv2.IMWRITE_JPEG_QUALITY,88])
    if not ok: raise RuntimeError("Image encoding failed")
    return "data:image/jpeg;base64,"+base64.b64encode(enc.tobytes()).decode()

@app.get("/api/health")
def health():
    return {"status":"ok","version":"0.1.0"}

@app.post("/api/analyze")
async def analyze_image(file:UploadFile=File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400,"Please upload an image file.")
    try:
        raw=await file.read()
        pil=Image.open(io.BytesIO(raw)).convert("RGB")
        bgr=cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise HTTPException(400,f"Invalid image: {e}")
    r=analyze(bgr)
    task={
        "task_id":"TASK-"+uuid.uuid4().hex[:4].upper(),
        "target_zone":r["target_zone"],
        "action":"surface_collection",
        "priority":r["target_priority"],
        "execution_mode":"assisted_autonomy",
        "status":"READY"
    }
    return {
        "file_name":file.filename,
        "detector":r["detector"],
        "model_confidence":None,
        "confidence_note":r["confidence_note"],
        "detected_class":"Floating vegetation (prototype category)",
        "coverage_percent":r["coverage_percent"],
        "density":r["density"],
        "target_zone":r["target_zone"],
        "target_priority":r["target_priority"],
        "zones":r["zones"],
        "overlay_image":data_url(r["overlay"]),
        "guidance":get_guidance(r["density"],r["target_zone"]),
        "robot_task":task
    }
