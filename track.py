from ultralytics import YOLO

# # Load a model
model = YOLO('best.onnx')  # load an official detection model
# # model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
# # model = YOLO('path/to/best.pt')  # load a custom model

# # Track with the model
# results = model.track(source="cameraCode/Produce.mp4",conf=0.3, iou=0.5, show=True, tracker="botsort.yaml")  # or .track() 
# # results = model.track(source="https://youtu.be/Zgi9g1ksQHc", show=True, tracker="bytetrack.yaml") 
import cv2
from ultralytics import YOLO

# # Load the YOLOv8 model
# model = YOLO('yolov8n.pt')

# # Open the video file
# video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture('cameraCode/Produce.mp4')
frame_count = 0
# Loop through the video frames
try:
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success and frame_count % 5 == 0:
            print(frame_count)
            # Run YOLOv8 inference on the frame
            results = model.track(source=frame, conf=0.3, iou=0.5, tracker="bytetrack.yaml",persist=True)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            frame_count += 1
        else:
            # Break the loop if the end of the video is reached
            # break
            frame_count += 1

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
    cap.release()
    cv2.destroyAllWindows()