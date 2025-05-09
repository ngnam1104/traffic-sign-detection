import gradio as gr
import cv2
import numpy as np
from ultralytics import YOLOv10

model = YOLOv10("runs/last.pt") 
print(model.info())
print(model.model.names) 
def infer_image(image):
    results = model.predict(source=image, imgsz=640, conf=0.25)
    return results[0].plot()

def infer_video(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = "/tmp/output.webm"
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'vp80'), fps, (w, h))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(source=frame, imgsz=640, conf=0.25)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
    return output_path

with gr.Blocks() as demo:
    gr.Markdown("## 🔍 YOLOv10 - Detection trên ảnh & video")

    with gr.Tab("📸 Ảnh"):
        image_input = gr.Image(type="numpy")
        image_output = gr.Image()
        image_button = gr.Button("Phát hiện đối tượng")
        image_button.click(fn=infer_image, inputs=image_input, outputs=image_output)

    with gr.Tab("🎞️ Video"):
        video_input = gr.Video()
        video_output = gr.Video()
        video_button = gr.Button("Phát hiện đối tượng trong video")
        video_button.click(fn=infer_video, inputs=video_input, outputs=video_output)

demo.launch()
