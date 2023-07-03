from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import cv2
import numpy as np
import threading
import socket
import struct
import pickle
from django.http import HttpResponse
from eventlet import wsgi
import eventlet
# from .socket_handlers import sio
import threading
import socketio
import base64

import cv2
from ultralytics import YOLO
import asyncio
from .models import Stream, Image, Object
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
import redis
import sys
import pickle
from .vehicle_counting import VehicleDetection
# eventlet.monkey_patch()
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
redis_host = 'localhost'  # Redis server host
redis_port = 6379  # Redis server port
redis_client = redis.Redis(host='localhost', port=6379, db=0)
threading_dict = {}
vehicle_counting_dict = {}

async def process_frame(site_name):
    # run while loop till redis list is empty
    # print("processing frame",site_name)
    while redis_client.llen(site_name) > 0:
        # pop the frame from redis list from the right side
        frame_data = redis_client.rpop(site_name)
        if frame_data is None:
            continue
        data=pickle.loads(frame_data)
        print("processing frame",site_name,data['frame_number'])
        image=base64.b64decode(data['frame'])
        jpg_as_np = np.frombuffer(image, dtype=np.uint8)
        jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
        print("processing frame",vehicle_counting_dict)



# async funtion to add frame and meta data to redis
async def add_frame_to_redis(site_name,data):
    global threading_dict,vehicle_counting_dict
    # print("adding frame to redis",site_name,threading_dict)
    redis_client.lpush(site_name, pickle.dumps(data))
    # print("adding frame to redis",site_name,threading_dict)
    if site_name not in threading_dict:
        threading_dict[site_name] = threading.Thread(target=asyncio.run,args=(process_frame(site_name),))
        threading_dict[site_name].start()
        vehicle_counting_dict[site_name] = VehicleDetection(data['lane_sides'],data['detection_lines'])
        print("Thread started", threading_dict)
    else:
        if threading_dict[site_name] is None or not threading_dict[site_name].is_alive():
            threading_dict[site_name] = threading.Thread(target=asyncio.run,args=(process_frame(site_name),))
            threading_dict[site_name].start()


# Define an event handler for the 'connect' event
@sio.on('connect')
def on_connect(sid, environ):
    print('Client connected:', sid)

# Define an event handler for the 'data' event
# Define an event handler for the 'frist_frame' event
@sio.on('frist_frame')
def on_received_first_frame(sid, data):
    print(f"received first frame from {data['site_name']} with frame number {data['frame_number']}")
    site_key = data['site_name']
    frame_data = pickle.dumps(data)
    # # Append the frame data to the site's list
    redis_client.lpush(site_key, frame_data)

# Define an event handler for the 'received_frame' event
@sio.on("received_frame")
def on_received_frame(sid, data):
    # print(f"received frame from {data['site_name']} with frame number {data['frame_number']}")
    threading.Thread(target=asyncio.run,args=(add_frame_to_redis(data['site_name'],data),)).start()
    sio.emit(data['site_name'],data['frame'])
    # add_frame_to_redis(data['site_name'],data)
    # site_key = data['site_name']
    # frame_data = pickle.dumps(data)
    
    # Append the frame data to the site's list
    # redis_client.lpush(site_key, frame_data)


# @sio.on("received_frame")
# def on_received_frame(sid,data):
    # print(f"received frame from {data['site_name']} with frame number {data['frame_number']}")
    # image = base64.b64decode(data['frame'])
    # jpg_as_np = np.frombuffer(image, dtype=np.uint8)
    # jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
    # print(f"frame size {sys.getsizeof(jpg_as_np)/1024} KB")
    # print(f"frame shape {sys.getsizeof(data['frame'])/1024} KB")
    # image=
    # sio.emit(data['site_name'],cv2.imdecode(np.frombuffer(jpg_as_np, np.uint8), cv2.IMREAD_COLOR))
    # sio.emit(data['site_name'],data['frame'])
    # redis_client.rpush(data['site_name'], json.dumps(data))
    # cv2.imshow("frame",jpg_as_np)
    # cv2.waitKey(1)
    
    # global record_dict
    # image=base64.b64decode(data['frame'])
    # jpg_as_np = np.frombuffer(image, dtype=np.uint8)
    # jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
    # threading.Thread(target=process_frame,args=(record_dict,data['site_name'],jpg_as_np,data['frame_number'])).start()


# Define an event handler for the 'disconnect' event
@sio.on('disconnect')
def on_disconnect(sid):
    print('Client disconnected:', sid)
    # send disconect message to client
    sio.emit('disconnect',sid)



# app = socketio.WSGIApp(sio)
# wsgi.server(eventlet.listen(('localhost', 7000)), app)
# Define a global variable to hold the most recent frame received from the client
# latest_frame = None
# stream_data = None
# labels = ['car','bus','van','truck','bike','rickshaw']

# Load the YOLOv8 model
# model = YOLO('best.pt')
# sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')

# # print(model,'######################')
# @sio.event
# def connect(sid, environ):
#     print('Client connected:', sid)


# @sio.event
# def disconnect(sid):
#     print('Client disconnected:', sid)


# @sio.event
# def my_event(sid, data):
#     print('Received data from client:', data)
#     sio.emit('my_response', {'response': 'OK'}, room=sid)

def run_socketio_server():
    # global model
    # model = YOLO('best.pt')
    app = socketio.WSGIApp(sio)
    wsgi.server(eventlet.listen(('localhost', 7000)), app)

# def receive_frames():
#     global latest_frame
#     global stream_data

#     # Create a socket object
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Bind the socket to a local address and port
#     host = 'localhost'  # replace with the IP address or hostname of the server
#     port = 12345  # replace with the port number you want to use
#     sock.bind((host, port))

#     # Listen for incoming connections
#     sock.listen()

#     # Accept incoming connections and receive frames
#     while True:
#         conn, addr = sock.accept()
#         with conn:
#             print('Connected by', addr)
#             while True:
#                 # Receive the tags size from the client
#                 tags_size_data = conn.recv(4)
#                 if not tags_size_data:
#                     break

#                 # Unpack the tags size and receive the tags data
#                 tags_size = struct.unpack('!I', tags_size_data)[0]
#                 tags_data = b''
#                 while len(tags_data) < tags_size:
#                     data = conn.recv(tags_size - len(tags_data))
#                     if not data:
#                         break
#                     tags_data += data

#                 # Check if the received data matches the expected size
#                 if len(tags_data) != tags_size:
#                     print('Received incomplete tags data')
#                     continue

#                 # Deserialize the tags data into a dictionary
#                 tags = pickle.loads(tags_data)

#                 # Receive the frame size from the client
#                 frame_size_data = conn.recv(4)
#                 if not frame_size_data:
#                     break

#                 # Unpack the frame size and receive the encoded frame
#                 frame_size = struct.unpack('!I', frame_size_data)[0]
#                 encoded_data = b''
#                 while len(encoded_data) < frame_size:
#                     data = conn.recv(frame_size - len(encoded_data))
#                     if not data:
#                         break
#                     encoded_data += data

#                 # Check if the received data matches the expected size
#                 if len(encoded_data) != frame_size:
#                     print('Received incomplete frame data')
#                     continue
#                 decoded_data = encoded_data.decode()
#                 image = base64.b64decode(decoded_data)
#                 image = np.frombuffer(image, dtype=np.uint8)
#                 latest_frame = cv2.imdecode(image, flags=1)
#                 stream_data = tags
#                 # Decode the frame and update the global variable
#                 # latest_frame = cv2.imdecode(np.frombuffer(encoded_data, np.uint8), cv2.IMREAD_COLOR)

#                 # Do something with the tags and frame (if needed)
#                 # print(tags)
#                 sio.emit('frame', decoded_data)
#                 # cv2.imshow('frame', latest_frame)

#     #             if cv2.waitKey(1) & 0xFF == ord('q'):
#     #                 break
#     # cv2.destroyAllWindows()

# # Start a background thread to receive frames from the client
# async def predict(frame):
#     global model
#     return model(frame)

# def insert_data(resutls, frame,stream_metadata):
#     if Stream.objects.filter(site_name=stream_metadata['site']).exists():
#         stream = Stream.objects.get(site_name=stream_metadata['site'])
#     else:
#         Stream.objects.create(
#             site_name=stream_metadata['site'],
#             stream_id='1',
#             stream_url='http://localhost:7000',

#         ).save()
#         stream = Stream.objects.get(site_name=stream_metadata['site'])
#     # save image into directory and save image path into database
#     # frame.save(f'./media/{stream.site_name}/{stream.stream_id}/{stream.stream_id}_.jpg')
#     cv2.imwrite(f'./media/{stream.site_name}/{stream.stream_id}/{stream_metadata["timestamp"]}_.jpg', frame)
#     print('image saved#######################33',stream_metadata['timestamp'],'#######################33')
#     Image.objects.create(
#         stream=stream,
#         timestamp=stream_metadata['timestamp'],
#         image_path=f'./media/{stream.site_name}/{stream.stream_id}/{stream_metadata["timestamp"]}.jpg'
#     ).save()
#     image = Image.objects.filter(stream=stream).last()
#     for box in resutls:
#         boxes=box.boxes
#         for cls,conf,xywh in zip(boxes.cls,boxes.conf,boxes.xywh):
#             Object.objects.create(
#                 image=image,
#                 label=labels[int(cls.item())],
#                 confidence=conf,
#                 x=xywh[0],
#                 y=xywh[1],
#                 w=xywh[2],
#                 h=xywh[3]
#             ).save()
        
        
#         # Object.objects.create(
#         #     image=image,
#         #     label=result.cls,
#         #     confidence=result.conf,
#         #     x=result.xywh[0],
#         #     y=result.xywh[1],
#         #     w=result.xywh[2],
#         #     h=result.xywh[3]
#         # ).save()

# async def prediction():
#     global latest_frame
#     global stream_data
#     while True:
#         # print('Waiting for frame...')

#         if latest_frame is not None:
#             # Wait for model prediction to complete
#             results = await predict(latest_frame)

#             # Process the prediction results here
#             print(results[0])
#             sio.emit('prediction_result', results[0].names)
#             threading.Thread(target=insert_data, args=(results, latest_frame,stream_data)).start()
#             # Reset the latest_frame to None after processing
#             # latest_frame = None

#         # Sleep for a short period of time to avoid CPU-intensive looping
#         await asyncio.sleep(0.01)

# def callback_detection():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(prediction())
#     loop.close()

class Index(TemplateView):
    def get(self, request):
        site_name = Stream.objects.all().values_list('site_name', flat=True)
        return render(request, 'index.html',{
            'site_name':site_name
        })

class Dashboard(TemplateView):
    def get(self, request,site_name):
        site_names = Stream.objects.all().values_list('site_name', flat=True)
        return render(request, 'dashboard.html',{
            'site_name':site_name,
            'site_names':site_names
        })

class History(TemplateView):
    def get(self, request):
        return render(request, 'history.html')

class VideoAnalysis(TemplateView):
    def get(self, request):
        return render(request, 'video_analysis.html')

class LiveStream(TemplateView):
    def get(self, request):
        return render(request, 'live_stream.html')



@api_view(['GET'])
def get_vehicle_counts(request):
    try:
        # number of rows inserted yesterday from object table
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_count = Object.objects.filter(image__timestamp__date=yesterday.date()).count()

        # number of rows inserted today from object table
        today = datetime.now()
        today_count = Object.objects.filter(image__timestamp__date=today.date()).count()

        # return as json object 
        return Response({
            'yesterday': yesterday_count,
            'today': today_count
        })
    except Exception as e:
        return Response({
            'error': str(e)
        })


from .serializer import ObjectSerializer, ImageSerializer, StreamSerializer,ImageWithObjectsSerializer
from django.db.models import Prefetch
@api_view(['GET'])
def get_objects(request):
    try:
        objects = Object.objects.all().order_by('-id')[0:10]
        serializer = ObjectSerializer(objects, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        })
    

@api_view(['GET'])
def get_images(request):
    try:
        # images = Image.objects.prefetch_related(Prefetch('object_set', queryset=Object.objects.all()))
        # print(images[0])
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        })
    
from django.db.models import F
@api_view(['GET'])
def get_image_objects(request):
    try:
        images_with_objects = Image.objects.prefetch_related('object_set').all().order_by('-id')[0:20][::-1]
        serializer = ImageWithObjectsSerializer(images_with_objects, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        })
