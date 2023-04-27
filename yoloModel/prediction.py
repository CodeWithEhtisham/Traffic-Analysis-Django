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

#     def __load_model(self) :
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
#     ) :

#         blob = cv2.dnn.blobFromImage(
#             image, 1 / 255.0, (width, height), swapRB=True, crop=False
#         )
#         self.model.setInput(blob)
#         preds = self.model.forward()
#         preds = preds.transpose((0, 2, 1))

        
#         results = self.__extract_ouput(
#             preds=preds,
#             image_shape=image.shape[:2],
#             input_shape=(height, width),
#             score=score,
#             nms=nms,
#             confidence=confidence,
#         )
#         return results

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
#    model_path='yolov8n.onnx', 
#    classes=CLASESS_YOLO
# )

# image = Image.open('photo6.jpg')
# image = np.array(image)
# image = image[:, :, ::-1].copy()
# results = detection(image)
# print(results)








import onnxruntime
import cv2
import numpy as np
from PIL import Image
CLASSES = [
	'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
	'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 
	'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 
	'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
	'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 
	'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
	'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 
	'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
	'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase',
	'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

opt_session = onnxruntime.SessionOptions()
opt_session.enable_mem_pattern = True
opt_session.enable_cpu_mem_arena = True
opt_session.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL

model_path = r'yolov8l.onnx'
EP_list = ['CUDAExecutionProvider', 'CPUExecutionProvider']

ort_session = onnxruntime.InferenceSession(model_path, providers=EP_list)

model_inputs = ort_session.get_inputs()
input_names = [model_inputs[i].name for i in range(len(model_inputs))]
input_shape = model_inputs[0].shape

model_output = ort_session.get_outputs()
output_names = [model_output[i].name for i in range(len(model_output))]

image = cv2.imread('photo6.jpg')
image_height, image_width = image.shape[:2]
Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

input_height, input_width = input_shape[2:]
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
resized = cv2.resize(image_rgb, (input_width, input_height))

# Scale input pixel value to 0 to 1
input_image = resized / 255.0
input_image = input_image.transpose(2,0,1)
input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)

outputs = ort_session.run(output_names, {input_names[0]: input_tensor})[0]

predictions = np.squeeze(outputs).T

conf_thresold = 0.1
# Filter out object confidence scores below threshold
scores = np.max(predictions[:, 4:], axis=1)
predictions = predictions[scores > conf_thresold, :]
scores = scores[scores > conf_thresold]

# Get the class with the highest confidence
class_ids = np.argmax(predictions[:, 4:], axis=1)

# Get bounding boxes for each object
boxes = predictions[:, :4]

#rescale box
input_shape = np.array([input_width, input_height, input_width, input_height])
boxes = np.divide(boxes, input_shape, dtype=np.float32)
boxes *= np.array([image_width, image_height, image_width, image_height])
boxes = boxes.astype(np.int32)


def nms(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        # print(keep_indices.shape, sorted_indices.shape)
        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes

def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou

# Apply non-maxima suppression to suppress weak, overlapping bounding boxes
indices = nms(boxes, scores, 0.3)


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y

image_draw = image.copy()
for (bbox, score, label) in zip(xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]):
    bbox = bbox.round().astype(np.int32).tolist()
    cls_id = int(label)
    cls = CLASSES[cls_id]
    color = (0,255,0)
    cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
    cv2.putText(image_draw,
                f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60, [225, 255, 255],
                thickness=1)
Image.fromarray(cv2.cvtColor(image_draw, cv2.COLOR_BGR2RGB))

# Save image
cv2.imwrite('output1.jpg', image_draw)