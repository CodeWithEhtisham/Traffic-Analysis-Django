import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8m.pt')

frame=cv2.imread('photo6.jpg')


# Run YOLOv8 inference on the frame
results = model(frame)

for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs

    print(boxes.cls)
    print(boxes.conf)
    print(boxes.xywh)