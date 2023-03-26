from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import cv2
import numpy as np
import threading
import socket
import struct
# Define a global variable to hold the most recent frame received from the client
latest_frame = None
def receive_frames():
    global latest_frame
    
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a local address and port
    host = 'localhost'  # replace with the IP address or hostname of the server
    port = 12345  # replace with the port number you want to use
    sock.bind((host, port))
    
    # Listen for incoming connections
    sock.listen()
    
    # Accept incoming connections and receive frames
    while True:
        conn, addr = sock.accept()
        with conn:
            print('Connected by', addr)
            while True:
                # Receive the frame size from the client
                size_data = conn.recv(4)
                if not size_data:
                    break
                
                # Unpack the frame size and receive the encoded frame
                frame_size = struct.unpack('!I', size_data)[0]
                encoded_data = b''
                while len(encoded_data) < frame_size:
                    data = conn.recv(frame_size - len(encoded_data))
                    if not data:
                        break
                    encoded_data += data
                
                # Check if the received data matches the expected size
                if len(encoded_data) != frame_size:
                    print('Received incomplete data')
                    continue
                
                # Decode the frame and update the global variable
                latest_frame = cv2.imdecode(np.frombuffer(encoded_data, np.uint8), cv2.IMREAD_COLOR)

                # cv2.imshow('frame', latest_frame)
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    # cv2.destroyAllWindows()

from django.http import StreamingHttpResponse
import cv2
import numpy as np

def video_stream(request):

    # Iterate over frames and send them as HTTP response
    def generate():
        while True:
            global latest_frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame.tobytes() + b'\r\n')

    # Create HTTP response and set content type to multipart/x-mixed-replace
    response = StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

    return response


# Start a background thread to receive frames from the client
thread = threading.Thread(target=receive_frames)
thread.daemon = True
thread.start()


class Index(TemplateView):
    def get(self,request):
        return render(request,'index.html')

class Dashboard(TemplateView):
    def get(self,request):
        return render(request,'dashboard.html')

class History(TemplateView):
    def get(self,request):
        return render(request,'history.html')

class VideoAnalysis(TemplateView):
    def get(self,request):
        return render(request,'video_analysis.html')

class LiveStream(TemplateView):
    def get(self,request):
        return render(request,'live_stream.html')
    

    