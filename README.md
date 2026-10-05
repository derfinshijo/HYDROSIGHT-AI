# AquaGuard AI — MVP v0.1

## Demo flow
Upload → AI analysis → vegetation mask → coverage → density → hotspot → guidance → robot task.

## Important
This first build uses an OpenCV vegetation-like segmentation baseline. It is NOT a trained species classifier and does not produce validated model accuracy. The code is structured so a trained YOLO segmentation model can replace the baseline later.

## Run

Python 3.10+ recommended.

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start backend:

```bash
uvicorn backend.main:app --reload
```

4. Serve frontend in a second terminal:

```bash
python -m http.server 5500 --directory frontend
```

5. Open:

http://127.0.0.1:5500

API health:
http://127.0.0.1:8000/api/health

## Demo
1. Upload a water-body image with visible green/floating vegetation.
2. Click ANALYZE WATER BODY.
3. Show the segmentation overlay and coverage.
4. Show the 3×2 hotspot grid.
5. Show the guidance card.
6. Show the generated robot task.
7. Click SIMULATE ROBOT DISPATCH.

## Next
v0.2: annotate real aquatic-vegetation images and plug in YOLO segmentation.
v0.3: historical scans + better spatial scoring.
v0.4: ESP32 command receiver and motor control.
v0.5: measured before/after closed-loop demo.

Never present the baseline's output as species identification, toxin detection, water-safety certification, or validated model accuracy.
