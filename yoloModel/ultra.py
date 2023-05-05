import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = "b.dav"
cap = cv2.VideoCapture(video_path)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Choose the video codec
out = cv2.VideoWriter('output.mp4', fourcc, 25.0, (0, 0))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame,conf=0.4)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Save the annotated frame into the output video
        out.write(annotated_frame)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object, the VideoWriter object, and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()
