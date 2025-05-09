from ultralytics import YOLOv10

def train_yolov10(model_id, yaml_path, image_size=640, epochs=50, batch_size=16):
    model = YOLOv10.from_pretrained(f'jameslahm/{model_id}')
    model.train(    
        data=yaml_path,
        imgsz=image_size,
        epochs=epochs,
        batch=batch_size,
        optimizer='auto'
    )

def test_yolov10(model_path, yaml_path, image_size=640, conf_threshold=0.25):
    model = YOLOv10(model_path)
    model.val(data=yaml_path, imgsz=image_size, conf=conf_threshold)

if __name__ == "__main__":
    # ==== CẤU HÌNH ====
    train = True     # Đặt True để train, False để test
    model_id = "yolov10s"
    yaml_path = "datasets/tt100k.yaml"
    image_size = 640
    epochs = 20
    batch_size = 32
    trained_model_path = "runs/best.pt"

    if train:
        train_yolov10(model_id, yaml_path, image_size, epochs, batch_size)
    else:
        test_yolov10(trained_model_path, yaml_path, image_size)
