from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
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
from .models import *
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

try:
    model = YOLO("best.pt")
except FileNotFoundError as e:
    print()
from apps.analysis.models import *

async def process_frame(site_name):
    # run while loop till redis list is empty
    # print("processing fr  `1              vvv vame",site_name)
    global redis_client,vehicle_counting_dict
    while redis_client.llen(site_name) > 0:
        # print("processing frame len",redis_client.llen(site_name))
        # pop the frame from redis list from the right side
        frame_data = redis_client.rpop(site_name)

        if frame_data is None:
            continue
        data=pickle.loads(frame_data)
        # print("processing frame",site_name,data['frame_number'])
        print(data['time_stamp'])
        print(site_name)
        image=base64.b64decode(data['frame'])
        jpg_as_np = np.frombuffer(image, dtype=np.uint8)
        jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
        result=model.predict(jpg_as_np)[0].boxes.data
        if result is not None and len(result)>0:
            vehicle_counting_dict[site_name].prediction(result,site_name,data['time_stamp'],jpg_as_np)
    # print(site_name,"done")
    # print(vehicle_counting_dict[site_name].VCount['IN']['total_count_in'])
    # print(vehicle_counting_dict[site_name].VCount['OUT']['total_count_out'])



# async funtion to add frame and meta data to redis
async def add_frame_to_redis(site_name,data):
    global threading_dict,vehicle_counting_dict
    # print("adding frame to redis",site_name,threading_dict)
    redis_client.lpush(site_name, pickle.dumps(data))
    # print("adding frame to redis",site_name,threading_dict)
    # print(f"dict keys {threading_dict.keys()}   {site_name}")
    if site_name not in threading_dict:
        threading_dict[site_name] = threading.Thread(target=asyncio.run,args=(process_frame(site_name),))
        threading_dict[site_name].start()
        # print("Thread started", threading_dict)
        vehicle_counting_dict[site_name] = VehicleDetection(data['lane_sides'],data['detection_lines'])
    else:
        if threading_dict[site_name] is None or not threading_dict[site_name].is_alive():
            threading_dict[site_name] = threading.Thread(target=asyncio.run,args=(process_frame(site_name),))
            threading_dict[site_name].start()
    print(f"dict for vehicle counting {vehicle_counting_dict}")


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

# Define an event handler for the 'disconnect' event
@sio.on('disconnect')
def on_disconnect(sid):
    print('Client disconnected:', sid)
    # send disconect message to client
    sio.emit('disconnect',sid)

def run_socketio_server():
    # global model
    # model = YOLO('best.pt')
    app = socketio.WSGIApp(sio)
    wsgi.server(eventlet.listen(('localhost', 7000)), app)


class Index(TemplateView):  
    def get(self, request):
        user_id = request.user.id
        print("user id is ",user_id)
        user=CustomUser.objects.get(id=user_id)
        if user.is_staff and user.is_active:
            site_name=Stream.objects.all().values_list('site_name',flat=True)
            print(site_name)
            # print([s for s in site_name])
            return render(request, 'index.html', {'site_name': site_name})
        elif user.is_active:
             site_name=Stream.objects.filter(users=user).values_list('site_name',flat=True)
             return render(request, 'index.html', {'site_name': site_name})
        
        # print("Index view is called")
        print(request.GET)
        user_id = request.GET.get('user_id')
        print("user_id:", user_id)  # Add this line to check the value of 'user_id'
        if user_id:
            c = CustomUser.objects.get(id=user_id)
            site_name = Stream.objects.filter(users=c).values_list('site_name', flat=True)
        else:
            # Handle the case when 'user_id' is not provided in the URL
            site_name = None
        print("site_name:", site_name)  # Add this line to check the value of 'site_name'
        return render(request, 'index.html', {'site_name': site_name})

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
from django.core.files.storage import FileSystemStorage
import os
def video_analysis(request):
    # def get(self, request):
    
    # def post(self, request):
        try:
            if request.method == 'POST' and request.FILES.get('video'):
                video_name = request.POST.get('video_name')
                date_time = request.POST.get('date_time')
                video_file = request.FILES['video']
                print(video_name, date_time)
                # save video file into directory
                fs = FileSystemStorage()
                # Define the directory and file name
                video_directory = 'save_video'
                # Construct the full file path
                video_path = os.path.join(video_directory, f'{video_name}.mp4')
                if not os.path.exists(video_directory):os.makedirs(video_directory)
                filename = fs.save(video_path, video_file)
                uploaded_file_url = fs.url(filename)
                date_time=datetime.strptime(date_time, '%Y-%m-%dT%H:%M').strftime("%Y-%m-%d %H:%M:%S")
                print(date_time)
                VideoAnalysisModel.objects.create(
                    video_name=video_name,
                    date_time=date_time,
                    video_path=uploaded_file_url
                ).save()
                # site_names = Stream.objects.all().values_list('site_name', flat=True)
                # video_analysis = VideoAnalysisModel.objects.all()
                # print(video_analysis)
                # return HttpResponseRedirect(reverse("video_analysis"))
                # return redirect('video_analysis')
            site_names = Stream.objects.all().values_list('site_name', flat=True)
            video_analysis = VideoAnalysisModel.objects.all()
            print(video_analysis)
            return render(request, 'video_analysis.html',{
                'site_names':site_names,
                'video_analysis':video_analysis
            })
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})

class LiveStream(TemplateView):
    def get(self, request):
        return render(request, 'live_stream.html')



@api_view(['GET'])
def get_vehicle_counts(request):
    pass
    # try:
    #     # number of rows inserted yesterday from object table
    #     yesterday = datetime.now() - timedelta(days=1)
    #     yesterday_count = Object.objects.filter(image__timestamp__date=yesterday.date()).count()

    #     # number of rows inserted today from object table
    #     today = datetime.now()
    #     today_count = Object.objects.filter(image__timestamp__date=today.date()).count()

    #     # return as json object 
    #     return Response({
    #         'yesterday': yesterday_count,
    #         'today': today_count
    #     })
    # except Exception as e:
    #     return Response({
    #         'error': str(e)
    #     })


from .serializer import ObjectSerializer, ImageSerializer, StreamSerializer,ImageWithObjectsSerializer
from django.db.models import Prefetch
@api_view(['GET'])
def get_objects(request):
    pass
    # try:
    #     objects = Object.objects.all().order_by('-id')[0:10]
    #     serializer = ObjectSerializer(objects, many=True)
    #     return Response(serializer.data)
    # except Exception as e:
    #     return Response({
    #         'error': str(e)
    #     })
    

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

import json

@api_view(['POST'])
def get_table_records(request):
    try:
        result = {
            "car": 0,
            "bike": 0,
            "bus": 0,
            "truck": 0,
            "rickshaw": 0,
            "van": 0,
        }
        percentage = []
        # print(request.POST)
        # data = json.loads(request.body)
        site_name = request.POST.get('site_name')
        # print(site_name)
        today = datetime.now()
        today_count = VehicleObject.objects.filter(
            image__timestamp__date=today.date().strftime("%Y-%m-%d"),
            image__stream__site_name=site_name
        )
        
        for obj in today_count:
            result[obj.label] += 1
        
        # Calculate the percentage of each vehicle
        total = sum(result.values())
        for key, value in result.items():
            percentage.append(round(value / total * 100, 2))
        
        return Response({
            'data': result,
            'percentage': percentage
        })
    except Exception as e:
        return Response({
            'error': str(e)
        })


@api_view(['POST'])
def get_multiline_chart_records(request):
    try:
        result = {
            "car": [0],
            "bike": [0],
            "bus": [0],
            "truck": [0],
            "rickshaw": [0],
            "van": [0],
            "car_out": [0],
            "bike_out": [0],
            "bus_out": [0],
            "truck_out": [0],
            "rickshaw_out": [0],
            "van_out": [0],
        }
        
        car, bike, bus, truck, rickshaw, van = 0, 0, 0, 0, 0, 0
        car_out, bike_out, bus_out, truck_out, rickshaw_out, van_out = 0, 0, 0, 0, 0, 0
        # result = []
        time_stamp = []
        site_name = request.POST.get('site_name')
        today = datetime.now()
        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date=today.date().strftime("%Y-%m-%d"),
            image__stream__site_name=site_name
        )
        
        for obj in today_count:
            time_stamp.append(obj.image.timestamp.strftime("%H:%M:%S"))
            if obj.total_count_in:
                if obj.label == 'car':
                    car += 1
                    result['car'].append(car)
                    result['bike'].append(bike)
                    result['bus'].append(bus)
                    result['truck'].append(truck)
                    result['rickshaw'].append(rickshaw)
                    result['van'].append(van)
                elif obj.label == 'bike':
                    bike += 1
                    result['bike'].append(bike)
                    result['car'].append(car)
                    result['bus'].append(bus)
                    result['truck'].append(truck)
                    result['rickshaw'].append(rickshaw)
                    result['van'].append(van)
                elif obj.label == 'bus':
                    bus += 1
                    result['bus'].append(bus)
                    result['car'].append(car)
                    result['bike'].append(bike)
                    result['truck'].append(truck)
                    result['rickshaw'].append(rickshaw)
                    result['van'].append(van)
                elif obj.label == 'truck':
                    truck += 1
                    result['truck'].append(truck)
                    result['car'].append(car)
                    result['bike'].append(bike)
                    result['bus'].append(bus)
                    result['rickshaw'].append(rickshaw)
                    result['van'].append(van)
                elif obj.label == 'rickshaw':
                    rickshaw += 1
                    result['rickshaw'].append(rickshaw)
                    result['car'].append(car)
                    result['bike'].append(bike)
                    result['bus'].append(bus)
                    result['truck'].append(truck)
                    result['van'].append(van)
                elif obj.label == 'van':
                    van += 1
                    result['van'].append(van)
                    result['car'].append(car)
                    result['bike'].append(bike)
                    result['bus'].append(bus)
                    result['truck'].append(truck)
                    result['rickshaw'].append(rickshaw)
                result['car_out'].append(car_out)
                result['bike_out'].append(bike_out)
                result['bus_out'].append(bus_out)
                result['truck_out'].append(truck_out)
                result['rickshaw_out'].append(rickshaw_out)
                result['van_out'].append(van_out)
                print("in count call ", len(result['car_out']),car_out,obj.image.timestamp.strftime("%H:%M:%S"))

            else:
                if obj.label == 'car':
                    car_out += 1
                    result['car_out'].append(car_out)
                    result['bike_out'].append(bike_out)
                    result['bus_out'].append(bus_out)
                    result['truck_out'].append(truck_out)
                    result['rickshaw_out'].append(rickshaw_out)
                    result['van_out'].append(van_out)
                elif obj.label == 'bike':
                    bike_out += 1
                    result['bike_out'].append(bike_out)
                    result['car_out'].append(car_out)
                    result['bus_out'].append(bus_out)
                    result['truck_out'].append(truck_out)
                    result['rickshaw_out'].append(rickshaw_out)
                    result['van_out'].append(van_out)
                elif obj.label == 'bus':
                    bus_out += 1
                    result['bus_out'].append(bus_out)
                    result['car_out'].append(car_out)
                    result['bike_out'].append(bike_out)
                    result['truck_out'].append(truck_out)
                    result['rickshaw_out'].append(rickshaw_out)
                    result['van_out'].append(van_out)
                elif obj.label == 'truck':
                    truck_out += 1
                    result['truck_out'].append(truck_out)
                    result['car_out'].append(car_out)
                    result['bike_out'].append(bike_out)
                    result['bus_out'].append(bus_out)
                    result['rickshaw_out'].append(rickshaw_out)
                    result['van_out'].append(van_out)
                elif obj.label == 'rickshaw':
                    rickshaw_out += 1
                    result['rickshaw_out'].append(rickshaw_out)
                    result['car_out'].append(car_out)
                    result['bike_out'].append(bike_out)
                    result['bus_out'].append(bus_out)
                    result['truck_out'].append(truck_out)
                    result['van_out'].append(van_out)
                elif obj.label == 'van':
                    van_out += 1
                    result['van_out'].append(van)
                    result['car_out'].append(car_out)
                    result['bike_out'].append(bike_out)
                    result['bus_out'].append(bus_out)
                    result['truck_out'].append(truck_out)
                    result['rickshaw_out'].append(rickshaw_out)
                result['van'].append(van)
                result['car'].append(car)
                result['bike'].append(bike)
                result['bus'].append(bus)
                result['truck'].append(truck)
                result['rickshaw'].append(rickshaw)

        multi_line_chart_data = [
            {
                'name': 'Car',
                'type': 'line',
                'symbolSize':8,
                'data': result['car']
            },
            {
                'name': 'Bike',
                'type': 'line',
                'symbolSize':8,
                'data': result['bike']
            },
            {
                'name': 'Bus',
                'type': 'line',
                'symbolSize':8,
                'data': result['bus']
            },
            {
                'name': 'Truck',
                'type': 'line',
                'symbolSize':8,
                'data': result['truck']
            },
            {
                'name': 'Rickshaw',
                'type': 'line',
                'symbolSize':8,
                'data': result['rickshaw']
            },
            {
                'name': 'Van',
                'type': 'line',
                'symbolSize':8,
                'data': result['van']
            },

            {
                'name': 'Car',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['car_out']
            },
            {
                'name': 'Bike',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['bike_out']
            },
            {
                'name': 'Bus',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['bus_out']
            },
            {
                'name': 'Truck',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['truck_out']
            },
            {
                'name': 'Rickshaw',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['rickshaw_out']
            },
            {
                'name': 'Van',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'symbolSize':8,
                'data': result['van_out']
            }
        ]        
        # print(time_stamp)
        return Response({
            'data': multi_line_chart_data,
            'time_stamp': time_stamp,
            'max_in': max(result['car'] + result['bike'] + result['bus'] + result['truck'] + result['rickshaw'] + result['van'])+8,
            'max_out': max(result['car_out'] + result['bike_out'] + result['bus_out'] + result['truck_out'] + result['rickshaw_out'] + result['van_out'])+8
        })
    except Exception as e:
        return Response({
            'error': str(e)
        })


@api_view(['POST'])
def get_line_chart_records(request):
    try:
        result = {
            "time_stamp": ["Time_stamp"],
            "IN": ["IN"],
            "OUT": ['OUT'],
        }
        In,out= 0, 0
        site_name = request.POST.get('site_name')
        today = datetime.now()
        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date=today.date().strftime("%Y-%m-%d"),
            image__stream__site_name=site_name
        )
        
        for obj in today_count:
            result['time_stamp'].append(obj.image.timestamp.strftime("%H:%M:%S"))
            if obj.total_count_in == 1:
                In += 1
                result['IN'].append(In)
                result['OUT'].append(out)
            elif obj.total_count_out == 1:
                out += 1
                result['OUT'].append(out)
                result['IN'].append(In)
                

        return Response({
            'data': [
                result['time_stamp'],
                result['IN'],
                result['OUT']
            ]
        })
    except Exception as e:
        return Response({
            'error': str(e)
        })




@api_view(['POST'])
def get_bar_chart_records(request):
    try:
        result = {
            "IN": {
                'name': 'IN',
            'type': 'bar',
            'data': [0, 0, 0, 0, 0, 0,0]
            },
            "OUT": {
                'name': 'OUT',
            'type': 'bar',
            'data': [0, 0, 0, 0, 0, 0,0]
            },
        }
        In=[0, 0, 0, 0, 0, 0,0]
        Out=[0, 0, 0, 0, 0, 0,0]

        site_name = request.POST.get('site_name')
        today = datetime.now()
        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date=today.date().strftime("%Y-%m-%d"),
            image__stream__site_name=site_name
        )
        
        for obj in today_count:
            if obj.total_count_in==1:
                if obj.label == 'car':
                    In[0] += 1
                elif obj.label == 'bike':
                    In[1] += 1
                elif obj.label == 'bus':
                    In[2] += 1
                elif obj.label == 'truck':
                    In[3] += 1
                elif obj.label == 'rickshaw':
                    In[4] += 1
                elif obj.label == 'van':
                    In[5] += 1
            elif obj.total_count_out==1:
                if obj.label == 'car':
                    Out[0] += 1
                elif obj.label == 'bike':
                    Out[1] += 1
                elif obj.label == 'bus':
                    Out[2] += 1
                elif obj.label == 'truck':
                    Out[3] += 1
                elif obj.label == 'rickshaw':
                    Out[4] += 1
                elif obj.label == 'van':
                    Out[5] += 1
                
        result['IN']['data']=In
        result['OUT']['data']=Out

        return Response({
            'data': [
                result['IN'],
                result['OUT']
            ],
            'max': max(In+Out)+5

        })
    except Exception as e:
        return Response({
            'error': str(e)
        })


from .video_prediction import VehicleDetectionVideoAnalysis
from django.conf import settings
from django.conf import settings
from django.http import FileResponse
import os

@api_view(['POST'])
def get_first_frame(request):
    try:
        print("$$$$$$$$$$$$$$$$$$$$$$$$")
        media_root = settings.MEDIA_ROOT
        video_path=request.POST.get("video_path")
        # video_path=video_path.split('media/')
        print(media_root[:-5]+video_path)
        # absolute_file_path = os.path.join(media_root, video_path.        
        # get first frame from video
        # print(absolute_file_path)
        # print("video loacation ",absolute_file_path)
        cap = cv2.VideoCapture("."+video_path)
        while True:
            ret, frame = cap.read()
            # print(ret)
            if ret:
                # convert frame into base64
                # resize image 400 to 400
                frame = cv2.resize(frame, (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))
                retval, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                break
            # continue
        # return as json object
        # print("first frame",jpg_as_text.decode())
        return Response({
            'frame': jpg_as_text.decode(),
            'video_id': VideoAnalysisModel.objects.get(video_path=video_path).id
        })
    except Exception as e:
        print("error",e)
        return Response({
            'error': str(e)
        })
@api_view(['POST'])
def video_prediction(request):
    try:
        vid_id=request.POST.get("video_id")
        video_path=VideoAnalysisModel.objects.get(id=vid_id).video_path
        detection_line=[request.POST.getlist("detection_line0[]"),request.POST.getlist("detection_line1[]")]

        print(vid_id)
        detection_line = [[int(x) for x in line] for line in detection_line]
        VideoAnalysisObject.objects.filter(video_analysis=vid_id).delete()

        obj=VehicleDetectionVideoAnalysis(model=model,detectionLines=detection_line,vid_id=vid_id)
        threading.Thread(target=obj.prediction, args=(video_path[1:],)).start()
        return Response({
            "message":True
        })
    except Exception as e:
        print(e)
        return Response({
            'message': False,
            'error': str(e)
        })
    
import mimetypes

@api_view(['POST'])
def download_excel(request):
    # Retrieve the file path from the query parameter
    file_path = request.POST.get('excel_path', None)
    print(file_path,'sadfsad')
    if file_path:
        # Check if the file exists
        if os.path.exists(file_path):
            # Set the appropriate content type for Excel
            content_type = mimetypes.guess_type(file_path)[0]
            if not content_type:
                content_type = 'application/octet-stream'

            # Generate the response with the file
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename=excel_file.csv'
                return response

    # Return an error response if the file path is invalid or the file doesn't exist
    print("file not found")
    return HttpResponse('File not found.', status=404)

@api_view(['DELETE'])
def delete_video(request):
    try:
        vid_id=request.POST.get("vid_id")
        print(vid_id,"id")
        video=VideoAnalysisModel.objects.get(id=vid_id)
        video_path=video.video_path
        excel_path=video.excel_path
        print(video_path,excel_path)
        if excel_path:
            if os.path.exists(excel_path[1:]):
                os.remove(excel_path[1:])
        if video_path:
            if os.path.exists(video_path[1:]):
                os.remove(video_path[1:])
        VideoAnalysisObject.objects.filter(video_analysis=video).delete()
        video.delete()
        print("video deleted")
        return Response({
            "message":True
        })
    except Exception as e:
        print(e)
        return Response({
            'message': False,
            'error': str(e)
        })