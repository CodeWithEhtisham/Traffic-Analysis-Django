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
    try:
        result = {
            "car": [0],
            "bike": [0],
            "bus": [0],
            "truck": [0],
            "rickshaw": [0],
            "van": [0],
        }
        car, bike, bus, truck, rickshaw, van = 0, 0, 0, 0, 0, 0
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

        multi_line_chart_data = [
            {
                'name': 'Car',
                'type': 'line',
                'data': result['car']
            },
            {
                'name': 'Bike',
                'type': 'line',
                'data': result['bike']
            },
            {
                'name': 'Bus',
                'type': 'line',
                'data': result['bus']
            },
            {
                'name': 'Truck',
                'type': 'line',
                'data': result['truck']
            },
            {
                'name': 'Rickshaw',
                'type': 'line',
                'data': result['rickshaw']
            },
            {
                'name': 'Van',
                'type': 'line',
                'data': result['van']
            }
        ]        
        # print(time_stamp)
        return Response({
            'data': multi_line_chart_data,
            'time_stamp': time_stamp,
            'max': max(result['car'] + result['bike'] + result['bus'] + result['truck'] + result['rickshaw'] + result['van'])+25
        })
    except Exception as e:
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
