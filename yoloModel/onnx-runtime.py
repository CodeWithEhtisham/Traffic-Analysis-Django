import onnxruntime
import cv2
import numpy as np
from PIL import Image

iou_threshold = 0.4
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



def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y

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

def load_model(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider']):
    session_options = onnxruntime.SessionOptions()
    session_options.enable_mem_pattern = True
    session_options.enable_cpu_mem_arena = True
    session_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    session = onnxruntime.InferenceSession(model_path, providers=providers)
    return session

def preprocess_image(image_path, input_shape):
    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(image_rgb, (input_shape[2], input_shape[3]))
    input_image = resized / 255.0
    input_image = input_image.transpose(2, 0, 1)
    input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)
    return input_tensor, image, image_height, image_width

def postprocess_predictions(predictions, input_shape, image_height, image_width, conf_thresold=0.1, iou_threshold=0.3):
    scores = np.max(predictions[:, 4:], axis=1)
    predictions = predictions[scores > conf_thresold, :]
    scores = scores[scores > conf_thresold]
    class_ids = np.argmax(predictions[:, 4:], axis=1)
    boxes = predictions[:, :4]
    input_shape = np.array([input_shape[1], input_shape[0], input_shape[1], input_shape[0]])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([image_width, image_height, image_width, image_height])
    boxes =predictions[:, :4]
    input_shape = np.array([input_shape[1], input_shape[0], input_shape[1], input_shape[0]])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([image_width, image_height, image_width, image_height])
    boxes = boxes.astype(np.int32)

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    sorted_indices = np.argsort(scores)[::-1]
    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the box with the highest score
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]
        sorted_indices = sorted_indices[keep_indices + 1]

    indices = np.array(keep_boxes)

    return xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]

def detect_objects(session, image_path):
    # Get model inputs and outputs
    model_inputs = session.get_inputs()
    input_shape = model_inputs[0].shape
    input_names = [model_inputs[i].name for i in range(len(model_inputs))]
    model_output = session.get_outputs()
    output_names = [model_output[i].name for i in range(len(model_output))]
    input_tensor, image, image_height, image_width = preprocess_image(image_path, input_shape)
    # Run inference
    outputs = session.run(output_names, {input_names[0]: input_tensor})[0]
    predictions = np.squeeze(outputs).T
    # Postprocess predictions
    boxes, scores, class_ids = postprocess_predictions(predictions, input_shape, image_height, image_width)
    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    indices = nms(boxes, scores, iou_threshold)
    # Draw bounding boxes on image
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
        # return image_draw
    cv2.imwrite('result1.jpg', image_draw)
    return image_draw


if __name__ == '__main__':
    model_path = 'yolov8l.onnx'
    image_path = 'photo6.jpg'
    detect_objects(load_model(model_path), image_path)