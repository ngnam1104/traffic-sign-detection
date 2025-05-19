# traffic-sign-detection
We use YOLOv11 for traffic sign detection on the TT100K dataset, which contains over 100,000 street images with annotated traffic signs. YOLOv11 offers a good balance between speed and accuracy, making it well-suited for real-time detection tasks in complex road scenes.

##  Dataset

We use the [TT100K dataset](https://cg.cs.tsinghua.edu.cn/traffic-sign/) for training and evaluation. It contains:

* 100,000+ street images from China (After preprocessing: 14000)
* 221 traffic sign classes (After preprocessing: 175)
* Bounding box annotations in Pascal VOC or COCO format

You can download the dataset from the [official website](https://cg.cs.tsinghua.edu.cn/traffic-sign/) or use [my dataset](https://app.roboflow.com/traffic-sign-detection-q6yz3/tt100k-jx9tb/1) provided. Then rename [my dataset](https://app.roboflow.com/traffic-sign-detection-q6yz3/tt100k-jx9tb/1) to "datasets"

## Model: YOLOv11

YOLOv11 is a recent object detection model optimized for:

* High accuracy on small objects (like traffic signs)
* Fast inference speed, suitable for real-time applications
* Improved attention mechanisms and large kernel convolution layers
* **Enhanced box regression loss using Focal IoU loss instead of traditional IoU loss**, which applies a modulating factor to focus learning on hard examples and includes a class-specific weighting term $\alpha^t$ to balance different classes. The Focal IoU loss is formulated as:

$$
\mathcal{L}_{\text{FocalIoU}} = - \alpha^t (1 - \text{IoU})^\gamma \log(\text{IoU})
$$

where:

* $\alpha^t$ is the weighting factor for class $t$, helping to balance classes with different frequencies or difficulties,
* $\gamma$ is the focusing parameter that reduces the loss contribution from easy examples,
* $\text{IoU}$ is the Intersection over Union between predicted and ground truth boxes.

We use the Ultralytics YOLOv11 framework for training and inference. See: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)

##  Installation

Install the dependencies via `pip`:

```bash
pip install -r requirements.txt
```

> Recommended: Use a virtual environment or `conda` environment.

## Project Structure

```
traffic-sign-detection/
├── datasets/
├── runs/
├── static/
├── templates/
├── ultralytics/
├── app.py
├── train_and_test.py
├── requirements.txt
└── README.md
```

## Training

To train the model on the TT100K dataset:

```bash
python train_and_test.py
```

You can modify the training configuration in train_and_test.py.
After training, the results (including trained weights and logs) are saved in the runs/detect directory by default.


## Running the Application

After training or testing the model, you can run the detection web app using:

```bash
python app.py
```

This will start the web server where you can upload images and perform traffic sign detection with the trained YOLOv11 model in real-time.


##  Results

| Metric         | Value         |
| -------------- | ------------- |
| Precision       | 80%         |
| Recall  | 60%         |
| mAP\@0.5       | 66.7%         |
| mAP\@0.5:0.95  | 53.8%        |


These are sample results from our best model. Performance may vary depending on system and training.
