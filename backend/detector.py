# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")

# def detect_objects(frame):
#     results = model(frame)
#     detected = []

#     for r in results:
#         for box in r.boxes:
#             cls = int(box.cls[0])
#             label = model.names[cls]
#             detected.append(label)

#     return list(set(detected))  # remove duplicates




from ultralytics import YOLO

# 🔥 Load model once (fast)
model = YOLO("yolov8n.pt")

# 🎯 Confidence threshold (tune kar sakta hai)
CONF_THRESHOLD = 0.5


def detect_objects(frame):
    # 🔥 faster inference (no gradients)
    results = model(frame, conf=CONF_THRESHOLD, verbose=False)

    detected = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # 🎯 confidence filter
            if conf < CONF_THRESHOLD:
                continue

            label = model.names[cls]
            detected.append(label)

    # 🔥 remove duplicates
    return list(set(detected))