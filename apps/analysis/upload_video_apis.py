from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
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
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
import redis
import sys
import pickle
from .vehicle_counting import VehicleDetection


# @api_view(['POST'])
# def get_table_records_uploads(request):
#     try:
#         result = {
#             "car": 0,
#             "bike": 0,
#             "bus": 0,
#             "truck": 0,
#             "rickshaw": 0,
#             "van": 0,
#         }
#         percentage = []
#         # print(request.POST)
#         # data = json.loads(request.body)
#         site_name = request.POST.get('site_name')
#         # print(site_name)
#         today = datetime.now()
#         today_count = VehicleObject.objects.filter(
#             image__timestamp__date=today.date().strftime("%Y-%m-%d"),
#             image__stream__site_name=site_name
#         )
        
#         for obj in today_count:
#             result[obj.label] += 1
        
#         # Calculate the percentage of each vehicle
#         total = sum(result.values())
#         for key, value in result.items():
#             percentage.append(round(value / total * 100, 2))
        
#         return Response({
#             'data': result,
#             'percentage': percentage
#         })
#     except Exception as e:
#         return Response({
#             'error': str(e)
#         })


@api_view(['POST'])
def get_multiline_chart_records_uploads(request):
    print("get_multiline_chart_records_uploads")
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
        vid_id = request.POST.get('id')
        today = datetime.now()
        records=VideoAnalysisObject.objects.filter(video_analysis__id=vid_id).select_related('video_analysis')
        
         
        for obj in records:
            print(obj.date_time)
            time_stamp.append(obj.date_time.strftime("%H:%M:%S"))
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
                # print("in count call ", len(result['car_out']),car_out,obj.image.timestamp.strftime("%H:%M:%S"))

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
        # print(multi_line_chart_data)
        # print(result)
        # print(time_stamp)
        return Response({
            'data': multi_line_chart_data,
            'time_stamp': time_stamp,
            'max_in': max(result['car'] + result['bike'] + result['bus'] + result['truck'] + result['rickshaw'] + result['van'])+8,
            'max_out': max(result['car_out'] + result['bike_out'] + result['bus_out'] + result['truck_out'] + result['rickshaw_out'] + result['van_out'])+8
        })
    except Exception as e:
        print(e)
        return Response({
            'error': str(e)
        })


@api_view(['POST'])
def get_line_chart_records_uploads(request):
    try:
        result = {
            "time_stamp": ["Time_stamp"],
            "IN": ["IN"],
            "OUT": ['OUT'],
        }
        In,out= 0, 0
        vid_id = request.POST.get('id')
        record=VideoAnalysisObject.objects.filter(video_analysis__id=vid_id)
        
        for obj in record:
            result['time_stamp'].append(obj.date_time.strftime("%H:%M:%S"))
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
def get_bar_chart_records_uploads(request):
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

        vid_id = request.POST.get('id')
        records=VideoAnalysisObject.objects.filter(video_analysis__id=vid_id)
        
        for obj in records:
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
            'max': max(In+Out)+2

        })
    except Exception as e:
        return Response({
            'error': str(e)
        })
