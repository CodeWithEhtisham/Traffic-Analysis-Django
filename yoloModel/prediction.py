# import io
# from typing import List, Tuple
# import cv2
# import numpy as np
# # import uvicorn
# # from fastapi import FastAPI, File
# from numpy import ndarray
# from PIL import Image


# class Detection:
#     def __init__(self, model_path: str, classes: List[str]):
#         self.model_path = model_path
#         self.classes = classes
#         self.model = self.__load_model()

#     def __load_model(self) -> cv2.dnn_Net:
#         net = cv2.dnn.readNet(self.model_path)
#         net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
#         net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
#         return net

#     def __extract_ouput(
#         self,
#         preds: ndarray,
#         image_shape: Tuple[int, int],
#         input_shape: Tuple[int, int],
#         score: float = 0.1,
#         nms: float = 0.0,
#         confidence: float = 0.0,
#     ) -> dict:
#         class_ids, confs, boxes = list(), list(), list()

#         image_height, image_width = image_shape
#         input_height, input_width = input_shape
#         x_factor = image_width / input_width
#         y_factor = image_height / input_height

#         rows = preds[0].shape[0]
#         for i in range(rows):
#             row = preds[0][i]
#             conf = row[4]

#             classes_score = row[4:]
#             _, _, _, max_idx = cv2.minMaxLoc(classes_score)
#             class_id = max_idx[1]
#             # print(classes_score[class_id])
#             if classes_score[class_id] > score:
#                 confs.append(conf)
#                 label = self.classes[int(class_id)]
#                 class_ids.append(label)

#                 # extract boxes
#                 x, y, w, h = (
#                     row[0].item(),
#                     row[1].item(),
#                     row[2].item(),
#                     row[3].item(),
#                 )
#                 left = int((x - 0.5 * w) * x_factor)
#                 top = int((y - 0.5 * h) * y_factor)
#                 width = int(w * x_factor)
#                 height = int(h * y_factor)
#                 box = np.array([left, top, width, height])
#                 boxes.append(box)

#         r_class_ids, r_confs, r_boxes = list(), list(), list()
#         indexes = cv2.dnn.NMSBoxes(boxes, confs, confidence, nms)
#         for i in indexes:
#             r_class_ids.append(class_ids[i])
#             r_confs.append(confs[i] * 100)
#             r_boxes.append(boxes[i].tolist())

#         return {"boxes": r_boxes, "confidences": r_confs, "classes": r_class_ids}

#     def __call__(
#         self,
#         image: ndarray,
#         width: int = 640,
#         height: int = 640,
#         score: float = 0.1,
#         nms: float = 0.0,
#         confidence: float = 0.0,
#     ) -> dict:

#         blob = cv2.dnn.blobFromImage(
#             image, 1 / 255.0, (width, height), swapRB=True, crop=False
#         )
#         self.model.setInput(blob)
#         preds = self.model.forward()
#         preds = preds.transpose((0, 2, 1))

#         # extract output
#         results = self.__extract_ouput(
#             preds=preds,
#             image_shape=image.shape[:2],
#             input_shape=(height, width),
#             score=score,
#             nms=nms,
#             confidence=confidence,
#         )
#         return results



# # Define yolov8 classes
# # Define yolov8 classes
# CLASESS_YOLO = [
#  'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
#  'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 
#  'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 
#  'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
#  'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 
#  'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
#  'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 
#  'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
#  'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase',
#  'scissors', 'teddy bear', 'hair drier', 'toothbrush'
# ]

# detection = Detection(
#    model_path='yolov8s.onnx', 
#    classes=CLASESS_YOLO
# )

# image = Image.open('prediction.jpg')
# image = np.array(image)
# image = image[:, :, ::-1].copy()
# results = detection(image)
# print(results)

import cv2

# Load Model
net = cv2.dnn.readNet('yolov8s.onnx')