import cv2
import math
import numpy as np
from ultralytics import YOLO
import datetime
from .models import VideoAnalysisModel,VideoAnalysisObject
# import widht or height of the the django setting
from django.conf import settings
args={
    "yolo":"best.onnx",
    "conf":0.2,
}

# args = vars(ap.parse_args())

class Model():
    def __init__(self) -> None:
        self.model=None

    def loadModel(self,args):
        if self.model is None:
            print('args yolo',args['yolo'])
            self.model=YOLO(args['yolo'])
        return self.model
    
class VehicleDetectionVideoAnalysis():
    def __init__(self,model,detectionLines,vid_id) -> None:
        self.offset = 10
        self.velocityoffset = 10
        self.distancethres = 20
        self.framecount = 0
        self.lanesCount = [0, 0, 0, 0, 0, 0]
        self.vid_id=VideoAnalysisModel.objects.get(id=vid_id)
        # print('lane sides',laneSides)
        self.laneSides = {'IN':0,'OUT':0}
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
        self.model=model
        self.class_list = ['car', 'bus', 'van', 'truck', 'bike', 'rickshaw']
        self.COLORS = np.random.randint(0, 255, size=(len(self.class_list), 3),dtype="uint8")

    def data_insertion_to_db(self,label,confidence,x,y,w,h,total_count_in,total_count_out,date_time):
        VideoAnalysisObject.objects.create(video_analysis=self.vid_id,label=label,confidence=confidence,x=x,y=y,w=w,h=h,total_count_in=total_count_in,total_count_out=total_count_out,date_time=date_time)
        


    # def updateCount(self,i,classes,confidence,row):
    def update_count(self, index, vehicle_class, confidence, detection_row,date_time):
        # print('update count start',self.laneSides,self.detectionlines)
        try:
            ins, outs = 0,0
            if index == 0:
                ins = 1
                # self.vTypeCount[self.class_list.index(vehicle_class)] += 1
            else:
                outs = 1
                # self.vTypeCountOut[self.class_list.index(vehicle_class)] += 1

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
            print('update count end',self.VCount)
            self.data_insertion_to_db(vehicle_class,confidence,detection_row[0],detection_row[1],detection_row[2],detection_row[3],ins,outs,date_time)
        except Exception as e:
            print('update count error',e)

    # def detectVehicle(self,frame):
    #     # print('detect vehicle',frame.shape)
    #     return 


    def prediction(self,path):
        print('prediction',path)
        cap = cv2.VideoCapture(path)
        date_time=self.vid_id.date_time
        frame_count=0

        while True:
            centersAndIDs = []
            unavailableIDs = []
            ret, frame = cap.read()
            print('ret',ret)
            if not ret:
                break
            if frame_count%30==0:
                # add one second to date_time
                print('date_time',date_time)
                date_time=date_time+datetime.timedelta(seconds=1)
            frame_count+=1
            frame=cv2.resize(frame,(settings.IMAGE_WIDTH,settings.IMAGE_HEIGHT))
            detection=self.model.predict(frame)[0].boxes.data

            for dl in self.detectionlines:
                cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (255, 203, 48), 6)

            for ind, row in enumerate(detection):
                confidence=float(row[4])
                obj = int(row[5])
                classes = self.class_list[obj]
                if confidence > args['conf']:    
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
                    cv2.circle(frame, (int(center[0]), int(center[1])), 4, (41, 18, 252), 5)   # Plot center point

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
                                        cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                        alreadyCounted = True
                                        break

                                if not alreadyCounted:
                                    self.detectedVehicleIDs.append(vehicleId)
                                    cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                    self.lanesCount[i] += 1
                                    try:
                                        print('update count')
                                        self.update_count(i,classes,confidence,row,date_time)
                                        print(self.VCount)
                                    except Exception as e:
                                        print(e)
                                    else:
                                        continue
                    cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  
                    text = "{}: {:.4f}".format(classes, confidence)
                    color = [int(c) for c in self.COLORS[obj]]
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(frame, "IN:" + str(self.laneSides["IN"]), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
                    cv2.putText(frame, "OUT:" + str(self.laneSides["OUT"]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)


            cv2.imshow("Frame", frame)
            self.framecount +=1
            cacheSize = 5
            self.cache.insert(0, centersAndIDs.copy())
            if len(self.cache) > cacheSize:
                del self.cache[cacheSize]

            if cv2.waitKey(1)&0xFF==27:
                return False
        import pandas as pd
        df = pd.DataFrame(columns=['VEHICLE','IN','OUT'])
        vehicle=[]
        ins=[]
        outs=[]
        for k,v in zip(self.VCount.get("IN"),self.VCount.get("OUT")):
            if k=="total_count_in":
                k="TOTAL"
                vehicle.append(k)
                ins.append(sum(ins))
                outs.append(sum(outs))
                continue
            vehicle.append(k)
            ins.append(int(len(self.VCount.get("IN").get(k))))
            outs.append(int(len(self.VCount.get("OUT").get(v))))

        print(vehicle,ins,outs)
        df['VEHICLE']=vehicle
        df['IN']=ins
        df['OUT']=outs
        name=self.vid_id.video_path.split("/")[-1].split(".")[0]
        df.to_csv(f"./media/excel/{name}.csv",index=False)
        VideoAnalysisModel.objects.filter(id=int(self.vid_id.id)).update(excel_path=f"./media/excel/{name}.csv",status=True)
        cap.release()
        cv2.destroyAllWindows()


# import socketio
# import eventlet
# from eventlet import wsgi
# import base64
# import threading

# # Create a Socket.IO server
# sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
# model=Model().loadModel(args)
# record_dict={}


# # Define an event handler for the 'connect' event
# @sio.on('connect')
# def on_connect(sid, environ):
#     print('Client connected:', sid)

# # Define an event handler for the 'data' event
# @sio.on('frist_frame')
# def on_received_first_frame(sid, data):
#     global record_dict,model

#     if data['site_name'] not in record_dict:
#         record_dict[data['site_name']]=VehicleDetection(model,data['lane_sides'],data['detection_lines'])

# @sio.on("received_frame")
# def on_received_frame(sid,data):
#     global record_dict
#     image=base64.b64decode(data['frame'])
#     jpg_as_np = np.frombuffer(image, dtype=np.uint8)
#     jpg_as_np = cv2.imdecode(jpg_as_np, flags=1)
#     threading.Thread(target=process_frame,args=(record_dict,data['site_name'],jpg_as_np,data['frame_number'])).start()


# # Define an event handler for the 'disconnect' event
# @sio.on('disconnect')
# def on_disconnect(sid):
#     # again try to connect to the server
#     print('Client disconnected:', sid)


# def process_frame(record_dict, site_name, frame,frame_no):
#     try:
#         print("received frame",site_name,frame_no)
#         print(record_dict.keys())
#         record_dict[site_name].prediction(frame)
#     except Exception as e:
#         print(e)

# app = socketio.WSGIApp(sio)
# if __name__ == '__main__':
#     # Wrap the Socket.IO server with the eventlet server
#     wsgi.server(eventlet.listen(('localhost', 8000)), app)
