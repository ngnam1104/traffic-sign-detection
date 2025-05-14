from ultralytics import YOLO

def train_yolo(model_id, yaml_path, epochs=50, batch_size=16, imgsz=1024):
    model = YOLO(model_id) 
    result = model.train(
        data=yaml_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,            
        optimizer='auto',
        save=True,
        save_period=1
    )
    print(f"Training completed. Results: {result}")

def test_yolo(model_path, yaml_path, conf_threshold=0.25):
    model = YOLO(model_path)
    model.val(data=yaml_path, conf=conf_threshold)

if __name__ == "__main__":
    # ==== CẤU HÌNH ====
    train = True  # Đặt True để train, False để test
    model_id = "traffic-sign-detection/best.pt"
    yaml_path = "datasets/tt100k.yaml"
    epochs = 80
    batch_size = 16
    imgsz = 1024

    if train:
        train_yolo(model_id, yaml_path, epochs, batch_size, imgsz)
    else:
        test_yolo(model_id, yaml_path)
