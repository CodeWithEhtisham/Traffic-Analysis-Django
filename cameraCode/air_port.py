import socketio

# Initialize the Socket.IO client
sio = socketio.Client()

# Define an event handler for the 'connect' event
@sio.on('connect')
def on_connect():
    print('Connected to the server')

# Define an event handler for the 'disconnect' event
@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

# Connect to the server
sio.connect('http://localhost:8000')


import cv2
import base64
import numpy as np
import time

detectionLines = []
laneSides = {'IN':0, 'OUT':0}
x1 = 0
y1 = 0
drawing = False

def drawLine(event, x, y, flags, param):
    global x1, y1, drawing, detectionLines
    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            x1, y1 = x, y
            drawing = True
        else:
            x2, y2 = x, y
            detectionLines.append([x1, y1, x2, y2])
            drawing = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        for i in detectionLines:
            p1 = np.array([i[0], i[1]])
            p2 = np.array([i[2], i[3]])
            p3 = np.array([x, y])
            if i[0] < i[2]:
                largerX = i[2]
                smallerX = i[0]
            else:
                largerX = i[0]
                smallerX = i[2]
            if abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)) < 10 and smallerX - 10 < x < largerX + 10:
                detectionLines.remove(i)

cap = cv2.VideoCapture('b.dav')
frame_count = 0
while True:
    ret, frame = cap.read()
    if ret:
        if frame_count == 0:
            cv2.namedWindow("Draw Lines")
            cv2.setMouseCallback("Draw Lines", drawLine)
            while 1:
                print("Draw lines on the frame and press 'q' to continue")
                frame2 = frame.copy()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows() 
                    lanesCount = [0] * len(detectionLines)
                    print(lanesCount)
                    try:
                        laneSides["IN"] = lanesCount[0]
                        laneSides["OUT"] = lanesCount[1]
                    except Exception as e:
                        print(e)
                    break
                for l in detectionLines:
                    cv2.line(frame, (l[0],l[1]), (l[2],l[3]), (255,203,48),6)
                cv2.imshow("Draw Lines", frame2)
                print(laneSides)
                data={
                    "site_name": "Air port road",
                    "frame_number": frame_count,
                    "lane_sides": laneSides,
                    "detection_lines": detectionLines,
                    "frame": base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()
                }
                # print(data)
                sio.emit('frist_frame', data)
                # time.sleep(10)
            frame_count += 1
                # print(frame_count)
        else:
        
            # for dl in detectionLines:
            #     cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (255, 203, 48), 6)
            frame_count += 1
            data = {
                "site_name": "Air port road",
                "frame_number": frame_count,
                # "lane_sides": laneSides,
                # "detection_lines": detectionLines,
                "frame": base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()
            }
            sio.emit('received_frame', data)
        print(frame_count)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
