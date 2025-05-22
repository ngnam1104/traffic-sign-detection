from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import os
import uuid
import logging
from threading import Lock

app = Flask(__name__)
CORS(app)

OUTPUT_FOLDER = "static/output"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

model = YOLO("best_enhanced_loss.pt")
model_lock = Lock()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_image', methods=['POST'])
def predict_image():
    request_id = uuid.uuid4().hex[:6]
    logging.info(f"[Req ID: {request_id}] Received /predict_image request.")
    file = request.files.get('image')

    if not file or file.filename == '':
        return jsonify({'error': 'No image file provided'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid image file type'}), 400

    try:
        image_np = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Failed to decode image'}), 400

        with model_lock:
            results = model.predict(source=image, imgsz=640, conf=0.25, verbose=False)

        annotated_image = results[0].plot()
        output_filename = f"output_{uuid.uuid4().hex}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        cv2.imwrite(output_path, annotated_image)

        return jsonify({'output_path': f"/static/output/{output_filename}"})

    except Exception as e:
        logging.exception("Error processing image")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/predict_video', methods=['POST'])
def predict_video():
    file = request.files.get('video')

    if not file or file.filename == '':
        return jsonify({'error': 'No video file provided'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid video file type'}), 400

    try:
        input_filename = f"input_{uuid.uuid4().hex}.mp4"
        input_path = os.path.join(OUTPUT_FOLDER, input_filename)
        file.save(input_path)

        output_filename = f"output_{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            os.remove(input_path)
            return jsonify({'error': 'Failed to open video'}), 400

        fps = cap.get(cv2.CAP_PROP_FPS)
        w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (w, h))

        if not out.isOpened():
            cap.release()
            os.remove(input_path)
            return jsonify({'error': 'Failed to write output video'}), 500

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            with model_lock:
                results = model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)
            annotated = results[0].plot()
            out.write(annotated)

        cap.release()
        out.release()
        os.remove(input_path)

        return jsonify({'output_path': f"/static/output/{output_filename}"})

    except Exception as e:
        logging.exception("Error processing video")
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/predict_camera', methods=['POST'])
def predict_camera():
    file = request.files.get('frame')

    if not file or file.filename == '':
        return jsonify({'error': 'No camera frame provided'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid frame file type'}), 400

    try:
        frame_np = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode frame'}), 400

        with model_lock:
            results = model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)

        detections = []
        for *xyxy, conf, cls in results[0].boxes.data:
            x1, y1, x2, y2 = map(int, xyxy)
            label = model.names[int(cls)]
            confidence = float(conf)
            detections.append({
                "box": [x1, y1, x2, y2],
                "label": label,
                "confidence": confidence
            })

        return jsonify({
            "detections": detections
        })

    except Exception as e:
        logging.exception("Error processing camera frame")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/static/output/<filename>')
def uploaded_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
