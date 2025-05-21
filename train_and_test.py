from ultralytics import YOLO

def train_yolo(model_yaml_path, pretrained_weights, data_yaml_path, epochs=50, batch_size=16, imgsz=1024):
    model = YOLO(model_yaml_path)
    if pretrained_weights:
        model.load(pretrained_weights, weights_only=True)
    result = model.train(
        data=data_yaml_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        optimizer='auto',
        save=True,
        save_period=1
    )
    print(f"Training completed. Results: {result}")

def test_yolo(model_path, data_yaml_path, conf_threshold=0.25):
    model = YOLO(model_path)
    print(model.model.info())

if __name__ == "__main__":
    train = True
    model_yaml_path = "ultralytics/cfg/models/11/yolo11.yaml"
    pretrained_weights = "traffic-sign-detection/best.pt"
    data_yaml_path = "datasets/tt100k.yaml"
    epochs = 100
    batch_size = 16
    imgsz = 1024

    if train:
        train_yolo(model_yaml_path, pretrained_weights, data_yaml_path, epochs, batch_size, imgsz)
    else:
        test_yolo(pretrained_weights, data_yaml_path)
