import socketio
import cv2
import base64
import numpy as np
import datetime

# Initialize the Socket.IO client
sio = socketio.Client()

# Define an event handler for the 'connect' event
@sio.on('connect')
def on_connect():
    print('Connected to the server')
    send_frames()

# Define an event handler for the 'disconnect' event
@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

desired_fps = 10
delay_ms = int(1000 / desired_fps)
frame_count = 0
drawing = False
detectionLines = []
laneSides = {'IN': 0, 'OUT': 0}
x1, y1 = 0, 0
def send_frames():
    print('Sending frames to the server')
    global frame_count, drawing, detectionLines, laneSides, x1, y1

    def drawLine(event, x, y, flags, param):
        print(x,y)
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
        print(detectionLines)

    cap = cv2.VideoCapture('Produce.mp4')
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print("Frames per second (fps):", fps)
    # return None

    while True:
        ret, frame = cap.read()
        if ret or frame not in [None, ""]:
            frame=cv2.resize(frame,(400,400))
            if frame_count == 0:
                cv2.namedWindow("Draw Lines")
                cv2.setMouseCallback("Draw Lines", drawLine)
                while True:
                    # print("Draw lines on the frame and press 'q' to continue")
                    frame2 = frame.copy()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        lanesCount = [0] * len(detectionLines)
                        # print(lanesCount)
                        try:
                            laneSides["IN"] = lanesCount[0]
                            laneSides["OUT"] = lanesCount[1]
                        except Exception as e:
                            print(e)
                        break
                    for l in detectionLines:
                        cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (255, 203, 48), 6)
                    cv2.imshow("Draw Lines", frame2)
                    # print(laneSides)

                cv2.destroyAllWindows()
                data = {
                    "site_name": "Air Port Road",
                    "time_stamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "frame_number": frame_count,
                    "lane_sides": laneSides,
                    "detection_lines": detectionLines,
                    "frame": base64.b64encode(cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()
                }
                sio.emit('frist_frame', data)

            else:
                data = {
                    "site_name": "Air Port Road",
                    "time_stamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "frame_number": frame_count,
                    "lane_sides": laneSides,
                    "detection_lines": detectionLines,
                    "frame": base64.b64encode(cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()
                }
                sio.emit('received_frame', data)

            frame_count += 1
            print(frame_count)
            # cv2.imshow('frame', frame)

            # # Exit loop if 'q' is pressed
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # cap.release()
    # cv2.destroyAllWindows()

# Connect to the server
sio.connect('http://localhost:7000')

# Run the event loop
sio.wait()
