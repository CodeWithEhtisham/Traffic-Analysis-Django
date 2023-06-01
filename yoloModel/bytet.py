# import cv2
# import numpy as np
# from bytetracker import BYTETracker

# # Load the pre-trained ByteTracker model
# tracker = BYTETracker("best.pt")

# # Open the video
# video = cv2.VideoCapture("b.dav")

# # Initialize the count
# count = 0

# # Loop over the frames in the video
# while video.isOpened():
#     # Get the next frame
#     ret, frame = video.read()

#     # If the frame is not empty
#     if ret:
#         # Track the objects in the frame
#         objects = tracker.track(frame)

#         # Get the bounding boxes of the tracked objects
#         boxes = np.array([obj.bbox for obj in objects])

#         # Count the number of objects that cross the line
#         count += np.count_nonzero(boxes[:, 0] > 0)

#         # Display the number of objects that have crossed the line
#         cv2.putText(frame, "Number of vehicles crossed the line: {}".format(count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#         # Display the frame
#         cv2.imshow("Frame", frame)

#         # Wait for a key press
#         key = cv2.waitKey(1)

#         # If the key is `q`, stop the loop
#         if key == ord("q"):
#             break

# # Close the video
# video.release()

# # Destroy all windows
# cv2.destroyAllWindows()


import supervision as sv
# from ultralytics import YOLO
# IMAGE = 'https://ultralytics.com/images/zidane.jpg'
# model = YOLO('best.pt')
# result = model(IMAGE)[0]
# detections = sv.Detections.from_yolov8(result)

# print(len(detections))

import cv2
from ultralytics import YOLO
# from supervision.tools.line_counter import LineCounter
# from supervision.geometry.dataclasses import Point


# LINE_START = Point(50, 1500)
# LINE_END = Point(3790, 1500)

# line_counter = LineCounter(start=LINE_START, end=LINE_END)
# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = "b.dav"
cap = cv2.VideoCapture(video_path)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Choose the video codec
# out = cv2.VideoWriter('output.mp4', fourcc, 25.0, (0, 0))
import time 
start = time.time()
i =0
# Loop through the video frames
while cap.isOpened():
    print(i)
    i+=1
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        # results = model(frame,conf=0.4, iou=0.5, show=True)
        # detections = sv.Detections.from_yolov8(results)
        # line_counter.update(detections)
        # add text to the frame
        # ln=len(detections)
        # print(detections)
        results =model.track(frame,conf=0.4, iou=0.5, show=True,tracker="bytetrack.yaml")
        # print(results)
        # break
        # Visualize the results on the frame
        # annotated_frame = results.plot()
        # cv2.putText(annotated_frame, f"Number of detections: {ln}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Save the annotated frame into the output video
        # out.write(annotated_frame)

        # Display the annotated frame
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
print(f"Time taken: {time.time()-start}")
# Release the video capture object, the VideoWriter object, and close the display window
cap.release()
# out.release()
cv2.destroyAllWindows()
