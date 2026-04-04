from flask import Flask, Response, jsonify, request
import cv2
import os
import time
from detector import detect_objects
from email_alert import send_email
from flask_cors import CORS
from utils import is_frame_changed

app = Flask(__name__)
CORS(app)

# 🔥 MULTI CAMERA STORAGE
cameras = {}          # cam_id -> VideoCapture
camera_urls = {}      # cam_id -> URL
prev_frames = {}      # cam_id -> previous frame
last_capture_times = {}  # cam_id -> last capture time

running = False
COOLDOWN = 2  # seconds
user_email = None

# 🎯 TARGET OBJECTS
TARGET_OBJECTS = [
    "person",
    "car", "truck", "bus", "motorcycle",
    "dog", "cat", "cow", "horse", "sheep", "bird"
]


# ✅ ADD CAMERA API
@app.route('/add_camera', methods=['POST'])
def add_camera():
    global cameras, camera_urls, prev_frames, last_capture_times

    data = request.json
    url = data.get("url")

    cam_id = str(len(cameras))

    cameras[cam_id] = cv2.VideoCapture(url)
    camera_urls[cam_id] = url
    prev_frames[cam_id] = None
    last_capture_times[cam_id] = 0

    print(f"Camera {cam_id} added: {url}")

    return jsonify({"camera_id": cam_id})


# ✅ SET EMAIL API
@app.route('/set_email', methods=['POST'])
def set_email():
    global user_email
    data = request.json
    user_email = data.get("email")

    print("Email set:", user_email)
    return jsonify({"status": "email set"})


# 🎥 GENERATE FRAMES PER CAMERA
def generate_frames(cam_id):
    global running

    camera = cameras.get(cam_id)

    frame_count = 0

    while True:
        if not running:
            time.sleep(0.1)
            continue

        success, frame = camera.read()

        if not success:
            print(f"Camera {cam_id} reconnecting...")
            camera.open(camera_urls[cam_id])
            time.sleep(1)
            continue

        frame = cv2.resize(frame, (480, 320))
        frame_count += 1

        # 🔥 skip frames
        if frame_count % 2 != 0:
            continue

        prev_frame = prev_frames[cam_id]

        if prev_frame is not None:
            if is_frame_changed(prev_frame, frame):

                current_time = time.time()

                if current_time - last_capture_times[cam_id] > COOLDOWN:

                    objects = detect_objects(frame)

                    filtered = [obj for obj in objects if obj in TARGET_OBJECTS]

                    if filtered:
                        print(f"[CAM {cam_id}] Detected:", filtered)

                        filename = f"backend/captures/{cam_id}_{int(current_time)}.jpg"
                        cv2.imwrite(filename, frame)

                        if user_email:
                            send_email(filename, user_email)

                        last_capture_times[cam_id] = current_time

        prev_frames[cam_id] = frame.copy()

        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


# 🎥 STREAM PER CAMERA
@app.route('/video/<cam_id>')
def video(cam_id):
    return Response(generate_frames(cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ▶️ START
@app.route('/start')
def start():
    global running
    running = True
    print("Monitoring Started")
    return jsonify({"status": "started"})


# ⏹ STOP
@app.route('/stop')
def stop():
    global running
    running = False
    print("Monitoring Stopped")
    return jsonify({"status": "stopped"})


# HOME
@app.route('/')
def home():
    return "AI Multi-Camera Monitoring Running..."


if __name__ == "__main__":
    os.makedirs("backend/captures", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)