

from datetime import datetime
from rest_framework.response import Response
from apps.analysis.models import VehicleObject


def get_multiline_chart_records_history(site_name,from_date,to_date):
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
        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date__range=(from_date,to_date),
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
        return {
            'data_multi': multi_line_chart_data,
            'time_stamp_multi': time_stamp,
            'max_in_multi': max(result['car'] + result['bike'] + result['bus'] + result['truck'] + result['rickshaw'] + result['van'])+8,
            'max_out_multi': max(result['car_out'] + result['bike_out'] + result['bus_out'] + result['truck_out'] + result['rickshaw_out'] + result['van_out'])+8
        }
    except Exception as e:
        return {
            'error': str(e)
        }


def get_line_chart_records_history(site_name,from_date,to_date):
    try:
        result = {
            "time_stamp": ["Time_stamp"],
            "IN": ["IN"],
            "OUT": ["OUT"],
        }
        In,out= 0, 0
        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date__range=(from_date,to_date),
            image__stream__site_name=site_name
        )
        
        for obj in today_count:
            result["time_stamp"].append(obj.image.timestamp.strftime("%H:%M:%S"))
            if obj.total_count_in == 1:
                In += 1
                result["IN"].append(In)
                result["OUT"].append(out)
            elif obj.total_count_out == 1:
                out += 1
                result["OUT"].append(out)
                result["IN"].append(In)
                

        return {
            'data_line': [
                result["time_stamp"],
                result["IN"],
                result["OUT"]
            ]
        }
    except Exception as e:
        return {
            'error': str(e)
        }




def get_bar_chart_records_history(site_name,from_date,to_date):
    try:
        result = {
            "IN": {
                'name': "IN",
            'type': 'bar',
            'data': [0, 0, 0, 0, 0, 0,0]
            },
            "OUT": {
                'name': "OUT",
            'type': 'bar',
            'data': [0, 0, 0, 0, 0, 0,0]
            },
        }
        In=[0, 0, 0, 0, 0, 0,0]
        Out=[0, 0, 0, 0, 0, 0,0]

        today_count = VehicleObject.objects.select_related('image').filter(
            image__timestamp__date__range=(from_date,to_date),
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
                
        result["IN"]['data']=In
        result["OUT"]['data']=Out

        return {
            "data_bar": [
                result["IN"],
                result["OUT"]
            ],
            "max_bar": max(In+Out)+5

        }
    except Exception as e:
        return {
            'error': str(e)
        }
