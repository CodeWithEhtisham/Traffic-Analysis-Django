# import cv2
# import numpy as np
# import socket
# import pickle
# import struct

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 12345))

# cap = cv2.VideoCapture(0)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     print(ret)
#     # Encode frame as jpeg
#     encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

#     # Get length of encoded frame
#     frame_size = struct.pack('!I', len(encoded_frame))

#     # Send frame size to server
#     client_socket.sendall(frame_size)

#     # Send encoded frame to server
#     client_socket.sendall(encoded_frame)

#     # Wait for response from server
#     # data = client_socket.recv(1024)

#     # Do something with the response (if any)
#     # print(data)

#     # Exit loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture
# cap.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import socket
import pickle
import struct
import base64
from datetime import datetime
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

cap = cv2.VideoCapture('b.dav')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(ret)

    # Define tags
    tags = {'fps': cap.get(cv2.CAP_PROP_FPS),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,
            # 'width': cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            # 'height': cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            'site': 'air port road'}

    # Serialize tags as byte stream
    tags_data = pickle.dumps(tags)

    # Encode frame as jpeg
#     encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
    encoded_frame =  base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()

    # Get length of encoded frame and tags
    frame_size = struct.pack('!I', len(encoded_frame))
    tags_size = struct.pack('!I', len(tags_data))

    # Send tags size to server
    client_socket.sendall(tags_size)

    # Send tags data to server
    client_socket.sendall(tags_data)

    # Send frame size to server
    client_socket.sendall(frame_size)

    # Send encoded frame to server
    client_socket.sendall(encoded_frame.encode())

    # Wait for response from server
    # data = client_socket.recv(1024)

    # Do something with the response (if any)
    # print(data)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
# cap.release()
# cv2.destroyAllWindows()
