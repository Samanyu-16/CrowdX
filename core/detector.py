from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people(frame):
    results = model(frame, conf=0.6, verbose=False)  # 🔥 higher threshold

    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0 and conf > 0.6:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w = x2 - x1
                h = y2 - y1

                # 🔥 STRICT HUMAN SIZE FILTER
                if w < 60 or h < 120:
                    continue

                detections.append(([x1, y1, w, h], conf))

    return detections