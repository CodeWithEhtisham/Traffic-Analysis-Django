import cv2
import math
import numpy as np
from ultralytics import YOLO
import argparse
import multiprocessing


# args = vars(ap.parse_args())

class Model():
    def __init__(self) -> None:
        self.model=None

    def loadModel(self,args):
        if self.model is None:
            print('args yolo',args['yolo'])
            self.model=YOLO(args['yolo'])
        return self.model
class VehicleDetection():
    def __init__(self,model) -> None:
        self.offset = 10
        self.velocityoffset = 10
        self.distancethres = 20
        self.x1 = 0
        self.y1 = 0
        self.drawing = False
        self.framecount = 0
        self.lanesCount = [0, 0, 0, 0, 0, 0]
        self.laneSides = {'IN':None, 'OUT':None}
        self.vTypeCount = [0, 0, 0, 0, 0, 0]
        self.vTypeCountOut = [0, 0, 0, 0, 0, 0]
        self.detectionlines = []
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


    def drawLine(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:
                # Start self.drawing a line
                self.x1, self.y1 = x, y
                self.drawing = True
            else:
                # Stop self.drawing a line
                x2, y2 = x, y
                self.detectionlines.append([self.x1, self.y1, x2, y2])
                self.drawing = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Delete right clicked line
            for i in self.detectionlines:
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
                    self.detectionlines.remove(i)

    # def updateCount(self,i,classes,confidence,row):
    def update_count(self, index, vehicle_class, confidence, detection_row):
        print('update count')
        if index == 0:
            self.vTypeCount[self.class_list.index(vehicle_class)] += 1
        else:
            self.vTypeCountOut[self.class_list.index(vehicle_class)] += 1

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


    def detectVehicle(self,frame):
        return self.model.predict(frame)[0].boxes.data
    
    def frame_prediction(self, frame_queue, detection_queue, args):
        while True:
            # Get a frame from the queue
            frame = frame_queue.get()
            if frame is None:
                break
            # Perform prediction on the frame
            detection = self.detectVehicle(frame)
            # Put the detection result into the queue
            detection_queue.put((frame, detection))

    def frame_display(self, frame_queue, detection_queue):
        unavailableIDs = []
        centersAndIDs = []

        while True:
            # Get a frame and its prediction result from the queue
            frame, detection = detection_queue.get()
            if frame is None or detection is None:
                break
            # Display the frame with the detection result
            # You may need to adjust this part depending on how you want to visualize the detection result
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

                                        self.update_count(i,classes,confidence,row)
                                        print(self.VCount)
                                    except Exception as e:
                                        print()
                                    else:
                                        continue
                    cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  
                    text = "{}: {:.4f}".format(classes, confidence)
                    color = [int(c) for c in self.COLORS[obj]]
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(frame, "IN:" + str(self.laneSides["IN"]), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)
                    cv2.putText(frame, "OUT:" + str(self.laneSides["OUT"]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (55,18,219), 3)

                # ... your visualization code ...
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    def prediction(self,args):
        cap = cv2.VideoCapture(args["frame"])
        frame_queue = multiprocessing.Queue()
        detection_queue = multiprocessing.Queue()

        # Create separate processes for frame prediction and display
        prediction_process = multiprocessing.Process(target=self.frame_prediction, args=(frame_queue, detection_queue, args))
        display_process = multiprocessing.Process(target=self.frame_display, args=(frame_queue, detection_queue,))

        # Start the processes
        prediction_process.start()
        display_process.start()

        # Feed frames into the queue for prediction
        first_frame = True
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if first_frame:
                cv2.imshow("Frame", frame)
                cv2.setMouseCallback("Frame", self.drawLine)
                while True:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("p"):  # press 'p' to pause and draw lines
                        break
                first_frame = False

            frame_queue.put(frame)

        # Wait for processes to finish
        prediction_process.join()
        display_process.join()

        cap.release()
        cv2.destroyAllWindows()

            

        #     cv2.imshow("Frame", frame)
        #     self.framecount +=1
        #     cacheSize = 5
        #     self.cache.insert(0, centersAndIDs.copy())
        #     if len(self.cache) > cacheSize:
        #         del self.cache[cacheSize]

        #     if cv2.waitKey(1)&0xFF==27:
        #         break
        # cap.release()
        # cv2.destroyAllWindows()

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--frame", required=True,
        help="path to input frame")
    ap.add_argument("-y", "--yolo", required=True,
        help="base path to YOLO directory")
    ap.add_argument("-n", "--names",
        help="base path to YOLO directory", default='torchweight/names.txt')
    ap.add_argument("-c", "--conf", type=float, default=0.2,
        help="minimum probability to filter weak detections")
    return vars(ap.parse_args())

args = parse_args()


if __name__ == "__main__":
    model=Model().loadModel(args)
    vehicle = VehicleDetection(model)
    vehicle.prediction(args)

