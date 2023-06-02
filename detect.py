import cv2
import math
import numpy as np
from ultralytics import YOLO
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input frame")
ap.add_argument("-y", "--yolo", required=True,
 	help="base path to YOLO directory")
ap.add_argument("-n", "--names",
 	help="base path to YOLO directory", default='torchweight/names.txt')
ap.add_argument("-c", "--confidence", type=float, default=0.2,
 	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

def drawLine(event, x, y, flags, param):
    # Mouse event handlers for drawing lines
    global x1, y1, drawing, detectionLines
    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:  # Start drawing a line
            x1, y1 = x, y
            drawing = True
        else:  # Stop drawing a line
            x2, y2 = x, y
            detectionLines.append([x1, y1, x2, y2])
            drawing = False
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
                
offset = 10
velocityoffset = 10
distancethres = 20
x1 = 0
y1 = 0
drawing = False
framecount = 0
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
VCount = {'IN':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_in':0},
        'OUT':{'car':[],'bus':[],'van':[],'truck':[],'bike':[],'rickshaw':[],'total_count_out':0}}
model=YOLO(args['yolo'])

my_file = open(args['names'], "r")
data = my_file.read()
class_list = data.split("\n") 


COLORS = np.random.randint(0, 255, size=(len(class_list), 3),
    dtype="uint8")

cap=cv2.VideoCapture(args["video"])


while True:  
      
    centersAndIDs = []
    unavailableIDs = []			
    boxes = []
    ret,frame = cap.read()
    (H, W) = frame.shape[:2]
    if framecount == 0:
        cv2.namedWindow("Draw Lines")
        cv2.setMouseCallback("Draw Lines", drawLine)
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
    
    for dl in detectionLines:
        cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (255, 203, 48), 6)
    
    results=model.predict(frame)
    detection=results[0].boxes.data
    
    for ind, row in enumerate(detection):
        confidence=float(row[4])
        obj = int(row[5])
        classes = class_list[obj]
        if confidence > args['confidence']:    
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
                centersAndIDs.append([center[0], center[1],id])
                id+=1
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
                                if i == 0:
                                    if classes == 'car':
                                        vTypeCount[0] +=1
                                        VCount['IN']['car']\
                                            .append({'count':vTypeCount[0],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'bus':
                                        vTypeCount[1] +=1
                                        VCount['IN']['bus']\
                                            .append({'count':vTypeCount[1],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'van':
                                        vTypeCount[2] +=1
                                        VCount['IN']['van']\
                                            .append({'count':vTypeCount[2],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'truck':
                                        vTypeCount[3] +=1
                                        VCount['IN']['truck']\
                                            .append({'count':vTypeCount[3],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'bike':
                                        vTypeCount[4] +=1
                                        VCount['IN']['bike']\
                                            .append({'count':vTypeCount[4],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    else:
                                        vTypeCount[5] +=1
                                        VCount['IN']['rickshaw']\
                                            .append({'count':vTypeCount[5],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    laneSides["IN"] +=1
                                    VCount['IN']['total_count_in'] = laneSides['IN']

                                if i == 1:
                                    if classes == 'car':
                                        vTypeCountOut[0] +=1
                                        VCount['OUT']['car']\
                                            .append({'count':vTypeCountOut[0],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'bus':
                                        vTypeCountOut[1] +=1
                                        VCount['OUT']['bus']\
                                            .append({'count':vTypeCountOut[1],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'van':
                                        vTypeCountOut[2] +=1
                                        VCount['OUT']['van']\
                                            .append({'count':vTypeCountOut[2],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'truck':
                                        vTypeCountOut[3] +=1
                                        VCount['OUT']['truck']\
                                            .append({'count':vTypeCountOut[3],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    elif classes == 'bike':
                                        vTypeCountOut[4] +=1
                                        VCount['OUT']['bike']\
                                            .append({'count':vTypeCountOut[4],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    else:
                                        vTypeCountOut[5] +=1
                                        VCount['OUT']['rickshaw']\
                                            .append({'count':vTypeCountOut[5],
                                            'conf':f'{confidence:.2f}',
                                            'x':row[0].numpy().astype(float),
                                            'y':row[1].numpy().astype(float),
                                            'w':row[2].numpy().astype(float),
                                            'h':row[3].numpy().astype(float)
                                            })
                                    
                                    laneSides["OUT"] +=1
                                    VCount['OUT']['total_count_out'] = laneSides['OUT']

                                print(VCount)
                            except Exception as e:
                                print()
                            else:
                                continue
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  
            text = "{}: {:.4f}".format(classes, confidence)
            color = [int(c) for c in COLORS[obj]]
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.putText(frame, "IN:" + str(laneSides["IN"]), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
            cv2.putText(frame, "OUT:" + str(laneSides["OUT"]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)


    cv2.imshow("Frame", frame)
    framecount +=1
    cacheSize = 5
    cache.insert(0, centersAndIDs.copy())
    if len(cache) > cacheSize:
        del cache[cacheSize]
		
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
