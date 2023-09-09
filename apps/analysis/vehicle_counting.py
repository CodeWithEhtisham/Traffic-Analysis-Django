import cv2
import math
import numpy as np
from ultralytics import YOLO
# import argparse
from apps.analysis.models import *
import os
import threading
import asyncio
from asgiref.sync import sync_to_async
model_name = 'best.onnx'
conf=0.2

# async def data_insertion(site_name,image,time_stamp,lable,conf,x,y,w,h,count_in,count_out):
#     stream=Stream.objects.get(site_name=site_name)
#     # save image into directory and save image path into database
#     # frame.save(f'./media/{stream.site_name}/{stream.stream_id}/{stream.stream_id}_.jpg')
#     if not os.path.exists(f"./media/{site_name}"):
#         os.mkdir(f"./media/{site_name}")
#     cv2.imwrite(f'./media/{site_name}/{time_stamp}_.jpg', image)
#     print('image saved#######################33',time_stamp,'#######################33')
#     image_obj=Image.objects.create(
#         stream=stream,
#         timestamp=time_stamp,
#         image_path=f'./media/{site_name}/{time_stamp}.jpg'
#     ).save()

#     VehicleObject.objects.create(
#         image=image_obj,
#         label=lable,
#         confidence=conf,
#         x=x,y=y,w=w,h=h,
#         total_count_in=count_in,
#         total_count_out=count_out
#     ).save
#     print("Data Inserted into the DB site:",site_name)

async def data_insertion_async(site_name, image, time_stamp, lable, conf, x, y, w, h, count_in, count_out):
    stream = await sync_to_async(Stream.objects.get)(site_name=site_name)

    if not os.path.exists(f"./media/{site_name}"):
        os.mkdir(f"./media/{site_name}")
    cv2.imwrite(f'./media/{site_name}/{time_stamp}_.jpg', image)
    # print('image saved#######################33', time_stamp, '#######################33')

    image_obj = await sync_to_async(Image.objects.create)(
        stream=stream,
        timestamp=time_stamp,
        image_path=f'./media/{site_name}/{time_stamp}.jpg'
    )
    await sync_to_async(image_obj.save)()

    vehicle_obj = await sync_to_async(VehicleObject.objects.create)(
        image=image_obj,
        label=lable,
        confidence=conf,
        x=x, y=y, w=w, h=h,
        total_count_in=count_in,
        total_count_out=count_out
    )
    await sync_to_async(vehicle_obj.save)()

    print("Data Inserted into the DB site:", site_name)


class Model:

    def __init__(self):
        self.model = model_name
    def loadmodel(self):
        self.model = YOLO(model_name)
        return self.model
    
class VehicleDetection():
    def __init__(self,laneSides,detectionLines) -> None:
        # Model.__init__(self)
        self.offset = 10
        self.velocityoffset = 10
        self.distancethres = 20
        # self.framecount = 0
        self.lanesCount = [0, 0, 0, 0, 0, 0]
        # print('lane sides',laneSides)
        self.laneSides = laneSides
        self.vTypeCount = [0, 0, 0, 0, 0, 0]
        self.vTypeCountOut = [0, 0, 0, 0, 0, 0]
        self.detectionlines = detectionLines
        # self.previousCentersAndIDs = []
        self.id = 0
        self.detectedVehicleIDs = []
        self.cache = []
        # self.vehicleVelocities = {}
        self.VCount = {'IN':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_in':0},
        'OUT':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_out':0}}
        # self.model=self.loadmodel()
        self.class_list = ['car', 'bus', 'van', 'truck', 'bike', 'rickshaw']
        self.COLORS = np.random.randint(0, 255, size=(len(self.class_list), 3),dtype="uint8")



    # def updateCount(self,i,classes,confidence,row):
    def update_count(self, index, vehicle_class, confidence, detection_row,site_name,time_stamp,frame):
        # print('update count start',self.laneSides,self.detectionlines)
        try:
            count_in=0
            count_out=0
            if index == 0:
                self.vTypeCount[self.class_list.index(vehicle_class)] += 1
                count_in=1
            else:
                self.vTypeCountOut[self.class_list.index(vehicle_class)] += 1
                count_out=1

            detection_type = "IN" if index == 0 else "OUT"
            self.VCount[detection_type][vehicle_class].append({
                'count': self.vTypeCount[self.class_list.index(vehicle_class)] if index == 0 else self.vTypeCountOut[self.class_list.index(vehicle_class)],
                'conf': f'{confidence:.2f}',
                'x': detection_row[0],
                'y': detection_row[1],
                'w': detection_row[2],
                'h': detection_row[3]
            })
            self.laneSides[detection_type] += 1
            self.VCount[detection_type]['total_count_in' if index == 0 else 'total_count_out'] += 1
            print('update count end',self.vTypeCount)
            print('update count end',self.vTypeCountOut)
            threading.Thread(target=asyncio.run,args=(data_insertion_async(
                site_name=site_name,
                image=frame,
                time_stamp=time_stamp,
                lable=vehicle_class,
                x=detection_row[0],
                y=detection_row[1],
                w=detection_row[2],
                h=detection_row[3],
                conf=f'{confidence:.2}',
                count_in=count_in,
                count_out=count_out
                ),)).start()


        except Exception as e:
            print('update count error',e)


    def prediction(self,detection,site_name,time_stamp,frame):
            # print('prediction')
        # while True:
            centersAndIDs = []
            unavailableIDs = []
            # detection=self.model.predict(frame)[0].boxes.data

            for ind, row in enumerate(detection):
                confidence=float(row[4])
                obj = int(row[5])
                classes = self.class_list[obj]
                if confidence > conf:    
                    (x, y) = (int(row[0]), int(row[1]))
                    (w, h) = (int(row[2]), int(row[3]))
                    center = (x + w) / 2, (y + h) / 2
                    sameVehicleDetected = False
                    alreadyCounted = False
                    for indx,c in enumerate(self.cache):
                        minDistance = self.distancethres * ((indx+2)/2)
                        for cid in c:
                            if cid[2] in unavailableIDs:
                                continue
                            distance = math.sqrt((center[0] - cid[0]) ** 2 + (center[1] - cid[1]) ** 2)
                            if distance < minDistance:
                                nearestBox = cid[2]
                                minDistance = distance
                                sameVehicleDetected = True
                        if sameVehicleDetected:
                            break

                    if not sameVehicleDetected:
                        centersAndIDs.append([center[0], center[1],self.id])
                        self.id+=1
                    else:
                        centersAndIDs.append([center[0], center[1], nearestBox])
                        unavailableIDs.append(nearestBox)


                    if len(centersAndIDs) !=0:
                        vehicleId = centersAndIDs[len(centersAndIDs) -1][2] 
                    # cv2.circle(frame, (int(center[0]), int(center[1])), 4, (41, 18, 252), 5)   # Plot center point

                    for i, dl in enumerate(self.detectionlines):
                        p1 = np.array([dl[0], dl[1]])
                        p2 = np.array([dl[2], dl[3]])
                        p3 = np.array([center[0], center[1]])
                        if dl[0] < dl[2]:
                            largerX = dl[2]
                            smallerX = dl[0]
                        else:
                            largerX = dl[0]
                            smallerX = dl[2]
                        if dl[1] < dl[3]:
                            largerY = dl[3]
                            smallerY = dl[1]
                        else:
                            largerY = dl[1]
                            smallerY = dl[3]

                        if abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)) < self.offset and \
                                smallerX - self.offset < center[0] < largerX + self.offset and \
                                smallerY - self.offset < center[1] < largerY + self.offset:
                                for dvi in self.detectedVehicleIDs:
                                    if dvi == vehicleId:
                                        # cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                        alreadyCounted = True
                                        break

                                if not alreadyCounted:
                                    self.detectedVehicleIDs.append(vehicleId)
                                    # cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                    self.lanesCount[i] += 1
                                    try:
                                        print('update count')
                                        self.update_count(i,classes,confidence,row,site_name,time_stamp,frame)
                                        print(self.VCount)
                                    except Exception as e:
                                        print()
                                    else:
                                        continue
                    # cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  
                    # text = "{}: {:.4f}".format(classes, confidence)
                    # color = [int(c) for c in self.COLORS[obj]]
                    # cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    # cv2.putText(frame, "IN:" + str(self.laneSides["IN"]), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
                    # cv2.putText(frame, "OUT:" + str(self.laneSides["OUT"]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)


            # cv2.imshow("Frame", frame)
            # self.framecount +=1
            cacheSize = 5
            self.cache.insert(0, centersAndIDs.copy())
            if len(self.cache) > cacheSize:
                del self.cache[cacheSize]

            # if cv2.waitKey(1)&0xFF==27:
            #     return False
        # cap.release()
        # cv2.destroyAllWindows()

# import socketio
# import eventlet
# from eventlet import wsgi
# import base64
# import threading

# # Create a Socket.IO server
# sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
# # model=Model().loadModel()
# record_dict={}


# # Define an event handler for the 'connect' event
# @sio.on('connect')
# def on_connect(sid, environ):
#     print('Client connected:', sid)

# # Define an event handler for the 'data' event
# @sio.on('frist_frame')
# def on_received_first_frame(sid, data):
#     global record_dict

#     if data['site_name'] not in record_dict:
#         record_dict[data['site_name']]=VehicleDetection(data['lane_sides'],data['detection_lines'])

# @sio.on("received_frame")
# def on_received_frame(sid,data):
#     global record_dict
#     image=base64.b64decode(data['frame'])
#     jpg_as_np = np.frombuffer(image, dtype=np.uint8)
#     jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
#     process_frame(data['site_name'],jpg_as_np,data['frame_number'])
#     # threading.Thread(target=process_frame,args=(data['site_name'],jpg_as_np,data['frame_number'])).start()


# # Define an event handler for the 'disconnect' event
# @sio.on('disconnect')
# def on_disconnect(sid):
#     # again try to connect to the server
#     print('Client disconnected:', sid)


# def process_frame( site_name, frame,frame_no):
#     try:
#         global record_dict
#         print("received frame",site_name,frame_no)
#         print(record_dict.keys())
#         # print(type(record_dict[site_name]))
#         record_dict[site_name].prediction(frame)
#     except Exception as e:
#         print(e)

# app = socketio.WSGIApp(sio)
# if __name__ == '__main__':
#     # Wrap the Socket.IO server with the eventlet server
#     wsgi.server(eventlet.listen(('localhost', 7000)), app)
