import cv2
import numpy as np
import socket
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(ret)
    # Encode frame as jpeg
    encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

    # Get length of encoded frame
    frame_size = struct.pack('!I', len(encoded_frame))

    # Send frame size to server
    client_socket.sendall(frame_size)

    # Send encoded frame to server
    client_socket.sendall(encoded_frame)

    # Wait for response from server
    # data = client_socket.recv(1024)

    # Do something with the response (if any)
    # print(data)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
