import cv2
import numpy as np

# Global variables
image = None
polygon = []
current_polygon = []
drawing = False

def draw_polygon(event, x, y, flags, param):
    global image, polygon, current_polygon, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_polygon = [(x, y)]

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            current_polygon.append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.polylines(image, [np.array(current_polygon)], False, (0, 0, 255), 2)
        if len(current_polygon) > 1:
            cv2.line(image, current_polygon[-2], current_polygon[-1], (255, 0, 0), thickness=2)
        polygon.append(np.array(current_polygon))

def main():
    global image

    cap = cv2.VideoCapture('b.dav')
    
    # Read first frame
    ret, frame = cap.read()

    # Check if frame read successfully
    if not ret:
        print("Can't read video stream or file")
        return

    # Display the first frame to user for drawing polygons
    image = frame.copy()
    cv2.namedWindow('Draw Polygons')
    cv2.setMouseCallback('Draw Polygons', draw_polygon)

    while True:
        cv2.imshow('Draw Polygons', image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    # Start playing the video and overlay the polygons on each frame
    while True:
        ret, frame = cap.read()

        # If frame was not read successfully then break the loop
        if not ret:
            break

        # Draw polygons on the frame
        for poly in polygon:
            cv2.polylines(frame, [poly], False, (0, 0, 255), 2)

        # Show the frame
        cv2.imshow('Video Stream', frame)

        key = cv2.waitKey(1) & 0xFF

        # If 'q' is pressed on the keyboard, 
        # stop the loop
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
