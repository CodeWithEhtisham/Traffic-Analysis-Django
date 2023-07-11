import cv2
import math
import numpy as np
from ultralytics import YOLO
import argparse

offset = 10
velocityoffset = 10
distancethres = 20
x1 = 0
y1 = 0
drawing = False
lanesCount = [0, 0, 0, 0, 0, 0]
laneSides = {'IN':None, 'OUT':None}
vTypeCount = [0, 0, 0, 0, 0, 0]
vTypeCountOut = [0, 0, 0, 0, 0, 0]
detectionLines = []
previousCentersAndIDs = []
id = 0
detectedVehicleIDs = []
cache = []
vehicleVelocities = {} 
import pandas as pd
df = pd.DataFrame(columns=['Video Name',"CAR_IN","CAR_OUT","BUS_IN","BUS_OUT","VAN_IN","VAN_OUT","TRUCK_IN","TRUCK_OUT","BIKE_IN","BIKE_OUT","RICKSHAW_IN","RICKSHAW_OUT","TOTAL_IN","TOTAL_OUT"])

VCount = {'IN':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_in':0},
        'OUT':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_out':0}}

args={
    'model':'../best.pt',
    'names':'../model/names.txt',
    'video_path':'/home/carl/Downloads/videos/',                                                                                                     
    'conf':0.25,
}
class Model:

    def __init__(self):
        self.args = args

        self.model = self.args['model']
    def loadmodel(self):
        self.model = YOLO(self.args['model'])
        return self.model
    
    def names(self):
        my_file = open(self.args['names'], "r")
        data = my_file.read()
        namesTxt = data.split("\n") 
        return namesTxt

class VehicleDetection(Model):
    def __init__(self):
        Model.__init__(self)
        self.drawing = False
        self.x = 0
        self.y = 0
        self.framecount = 0
        self.id = 0
        self.model=self.loadmodel()
        self.COLORS = np.random.randint(0, 255, size=(len(self.names()), 3),
        dtype="uint8")
        
    def update_count(self, index, vehicle_class, confidence, detection_row):
        print('update count',index, vehicle_class, confidence, detection_row)
        try:
            if index == 0:
                vTypeCount[self.names().index(vehicle_class)] += 1
            else:
                vTypeCountOut[self.names().index(vehicle_class)] += 1

            detection_type = "IN" if index == 0 else "OUT"
            VCount[detection_type][vehicle_class].append({
                'count': vTypeCount[self.names().index(vehicle_class)] if index == 0 else vTypeCountOut[self.names().index(vehicle_class)],
                'conf': f'{confidence:.2f}',
                'x': detection_row[0],
                'y': detection_row[1],
                'w': detection_row[2],
                'h': detection_row[3]
            })
            laneSides[detection_type] += 1
            VCount[detection_type]['total_count_in' if index == 0 else 'total_count_out'] += 1
            print(VCount)
        except Exception as e:
            print(f"Error in update_count: {e}")

    def drawLine(self,event, x, y, flags, param):
        # Mouse event handlers for drawing lines
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:  # Start drawing a line
                self.x1, self.y1 = x, y
                self.drawing = True
            else:  # Stop drawing a line
                x2, y2 = x, y
                detectionLines.append([self.x1, self.y1, x2, y2])
                self.drawing = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Delete right clicked line
            for i in detectionLines:
                p1 = np.array([i[0], i[1]])
                p2 = np.array([i[2], i[3]])
                p3 = np.array([x, y])
                if i[0] < i[2]:
                    largerX = i[2]
                    smallerX = i[0]
                else:
                    largerX = i[0]
                    smallerX = i[2]
                if abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)) < 10 and smallerX - 10 < x < largerX + 10:
                    detectionLines.remove(i)
            print('detectino',detectionLines)
    
    def run(self,path):
        cap = cv2.VideoCapture(path)
        
        while True:
            centersAndIDs = []
            unavailableIDs = []			
            # boxes = []
            ret,frame = cap.read()
            if not ret:
                break
            (H, W) = frame.shape[:2]
            if self.framecount == 0:
                cv2.namedWindow("Draw Lines")
                cv2.setMouseCallback("Draw Lines", self.drawLine)
                while 1:
                    frame2 = frame.copy()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows() 
                        lanesCount = [0] * len(detectionLines)
                        try:
                            laneSides["IN"] = lanesCount[0]
                            laneSides["OUT"] = lanesCount[1]
                        except Exception as e:
                            print(e)
                        break
                    for l in detectionLines:
                        cv2.line(frame, (l[0],l[1]), (l[2],l[3]), (255,203,48),6)
                    cv2.imshow("Draw Lines", frame2)
            print('detection',detectionLines)
            for dl in detectionLines:
                cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (255, 203, 48), 6)
            
            # if self.framecount % 2 == 0:
            self.framecount+=1
            #     continue

            results = self.model.predict(frame)
            detection = results[0].boxes.data
            # detection=[]
            for ind, row in enumerate(detection):
                confidence=float(row[4])
                obj = int(row[5])
                classes = self.names()[obj]
                if confidence > args['conf']:    
                    (x, y) = (int(row[0]), int(row[1]))
                    (w, h) = (int(row[2]), int(row[3]))
                    center = (x + w) / 2, (y + h) / 2
                    sameVehicleDetected = False
                    alreadyCounted = False
                    for indx,c in enumerate(cache):
                        minDistance = distancethres * ((indx+2)/2)
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

                    for i, dl in enumerate(detectionLines):
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
                    
                        if abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)) < offset and \
                            smallerX - offset < center[0] < largerX + offset and \
                            smallerY - offset < center[1] < largerY + offset:

                            for dvi in detectedVehicleIDs:
                                if dvi == vehicleId:
                                    cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                    alreadyCounted = True
                                    break
                            if not alreadyCounted:
                                detectedVehicleIDs.append(vehicleId)
                                cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (90, 224, 63), 6)
                                lanesCount[i] += 1
                                try:
                                    self.update_count(i,classes,confidence,row)
                                except Exception as e:
                                    print(f"while loop error: {e}")
                    cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  
                    text = "{}: {:.4f}".format(classes, confidence)
                    color = [int(c) for c in self.COLORS[obj]]
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(frame, "IN:" + str(laneSides["IN"]), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
                    cv2.putText(frame, "OUT:" + str(laneSides["OUT"]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
            
            cv2.imshow("Frame", frame)
            self.framecount +=1
            cacheSize = 5
            cache.insert(0, centersAndIDs.copy())
            if len(cache) > cacheSize:
                del cache[cacheSize]
            if cv2.waitKey(1)&0xFF==27:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print(VCount)
        # update the dataframe
        df.loc[len(df)] = [path.split('/')[-1],VCount['IN']['car'],VCount['OUT']['car'],VCount['IN']['bus'],VCount['OUT']['bus'],VCount['IN']['van'],VCount['OUT']['van'],VCount['IN']['truck'],VCount['OUT']['truck'],VCount['IN']['bike'],VCount['OUT']['bike'],VCount['IN']['rickshaw'],VCount['OUT']['rickshaw'],VCount['IN']['total_count_in'],VCount['OUT']['total_count_out']]
        df.to_csv('vehicle_count.csv',index=False)



if __name__ == '__main__':

    # args = parse_args()
    import os
    path = args['video_path']
    for file in os.listdir(path):
        detector = VehicleDetection()
        detector.run(path+file)



