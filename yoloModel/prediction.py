import cv2
import numpy as np
# import onnxruntime as ort
from ultralytics import YOLO

model = YOLO('yoloModel/best.pt')
results = model('yoloModel/prediction.py', save=True)