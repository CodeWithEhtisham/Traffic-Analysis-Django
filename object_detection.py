import cv2
import math
import numpy as np
from ultralytics import YOLO
import argparse


class Model():
    def __init__(self):
        self.model = None

    def loadModel(self, args):
        if self.model is None:
            print('args yolo', args['yolo'])
            self.model = YOLO(args['yolo'])
        return self.model


class TrackedVehicle:
    def __init__(self, vehicle_id, center):
        self.id = vehicle_id
        self.last_seen = center
        self.last_seen_framecount = 0
        self.crossed_line = False
        self.vehicle_class = None
        self.confidence = None
        self.detection_row = None
        self.framecount = 0
        self.distancethres = 20
        self.offset = 10
        self.recent_frames_threshold = 10

    def is_same_vehicle(self, center):
        distance = math.sqrt((center[0] - self.last_seen[0]) ** 2 + (center[1] - self.last_seen[1]) ** 2)
        return distance < self.distancethres

    def is_recently_seen(self):
        return self.framecount - self.last_seen_framecount <= self.recent_frames_threshold

    def is_crossed_line(self, detectionlines):
        for dl in detectionlines:
            p1 = np.array([dl[0], dl[1]])
            p2 = np.array([dl[2], dl[3]])
            p3 = np.array([self.last_seen[0], self.last_seen[1]])
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
                    smallerX - self.offset < self.last_seen[0] < largerX + self.offset and \
                    smallerY - self.offset < self.last_seen[1] < largerY + self.offset:
                self.crossed_line = True
                return True
        return False

    def mark_counted(self):
        self.crossed_line = True

    def get_lane_counts(self, detectionlines):
        lanesCount = [0] * len(detectionlines)
        if self.crossed_line:
            for i, dl in enumerate(detectionlines):
                p1 = np.array([dl[0], dl[1]])
                p2 = np.array([dl[2], dl[3]])
                p3 = np.array([self.last_seen[0], self.last_seen[1]])
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
                        smallerX - self.offset < self.last_seen[0] < largerX + self.offset and \
                        smallerY - self.offset < self.last_seen[1] < largerY + self.offset:
                    lanesCount[i] += 1
        return lanesCount
    # return lanesCoun

    def draw(self, frame):
        cv2.circle(frame, (int(self.last_seen[0]), int(self.last_seen[1])), 4, (41, 18, 252), 5)  # Plot center point

    def __str__(self):
        return f"TrackedVehicle {self.id}: Last Seen: {self.last_seen}, Crossed Line: {self.crossed_line}"


class VehicleDetection():
    def __init__(self, model):
        self.offset = 10
        self.distancethres = 20
        self.detectionlines = []
        self.lanesCount = [0, 0, 0, 0, 0, 0]
        self.laneSides = {'IN': None, 'OUT': None}
        self.VCount = {'IN': {'car': [], 'bus': [], 'van': [], 'truck': [], 'bike': [], 'rickshaw': [], 'total_count_in': 0},
                       'OUT': {'car': [], 'bus': [], 'van': [], 'truck': [], 'bike': [], 'rickshaw': [], 'total_count_out': 0}}
        self.model = model
        self.class_list = ['car', 'bus', 'van', 'truck', 'bike', 'rickshaw']
        self.COLORS = np.random.randint(0, 255, size=(len(self.class_list), 3), dtype="uint8")

    def drawLine(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:
                # Start drawing a line
                self.x1, self.y1 = x, y
                self.drawing = True
            else:
                # Stop drawing a line
                x2, y2 = x, y
                self.detectionlines.append([self.x1, self.y1, x2, y2])
                self.drawing = False

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Delete right-clicked line
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

    def detectVehicle(self, frame):
        return self.model.predict(frame)[0].boxes.data

    def update_count(self, index, vehicle_class, confidence, detection_row):
        if index == 0:
            self.VCount['IN'][vehicle_class].append({
                'count': len(self.VCount['IN'][vehicle_class]) + 1,
                'conf': f'{confidence:.2f}',
                'x': detection_row[0],
                'y': detection_row[1],
                'w': detection_row[2],
                'h': detection_row[3]
            })
            self.VCount['IN']['total_count_in'] += 1
        else:
            self.VCount['OUT'][vehicle_class].append({
                'count': len(self.VCount['OUT'][vehicle_class]) + 1,
                'conf': f'{confidence:.2f}',
                'x': detection_row[0],
                'y': detection_row[1],
                'w': detection_row[2],
                'h': detection_row[3]
            })
            self.VCount['OUT']['total_count_out'] += 1

        self.laneSides['IN'] = len(self.VCount['IN'][vehicle_class])
        self.laneSides['OUT'] = len(self.VCount['OUT'][vehicle_class])

    def prediction(self, args):
        cap = cv2.VideoCapture(args["frame"])
        frame_skip = 5  # Skip every 5 frames
        frame_count = 0
        tracked_vehicles = {}
        drawing = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue  # Skip this frame

            if frame_count == 1:
                # Draw detection lines on the first frame
                cv2.namedWindow("Frame")
                cv2.setMouseCallback("Frame", self.drawLine)
                while True:
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("r"):
                        # Reset the detection lines
                        self.detectionlines = []
                    elif key == ord("q"):
                        # Quit the program
                        break

                cv2.destroyAllWindows()

            centersAndIDs = []
            detection = self.detectVehicle(frame)

            for row in detection:
                confidence = float(row[4])
                obj = int(row[5])
                classes = self.class_list[obj]
                if confidence > args['conf']:
                    (x, y) = (int(row[0]), int(row[1]))
                    (w, h) = (int(row[2]), int(row[3]))
                    center = (x + w) / 2, (y + h) / 2

                    # Track vehicles over multiple frames
                    vehicle_id = None
                    for vehicle in tracked_vehicles.values():
                        if vehicle.is_same_vehicle(center):
                            vehicle_id = vehicle.id
                            break

                    if vehicle_id is None:
                        vehicle_id = len(tracked_vehicles) + 1
                        tracked_vehicles[vehicle_id] = TrackedVehicle(vehicle_id, center)

                    centersAndIDs.append([center[0], center[1], vehicle_id])

                    cv2.circle(frame, (int(center[0]), int(center[1])), 4, (41, 18, 252), 5)

            # Remove expired tracked vehicles
            tracked_vehicles = {k: v for k, v in tracked_vehicles.items() if v.is_recently_seen()}

            # Perform vehicle counting and update counts
            for tracked_vehicle in tracked_vehicles.values():
                if tracked_vehicle.is_crossed_line(self.detectionlines):
                    tracked_vehicle.mark_counted()
                    lanesCount = tracked_vehicle.get_lane_counts(self.detectionlines)
                    for i, count in enumerate(lanesCount):
                        self.lanesCount[i] += count
                        if count > 0:
                            self.update_count(i, tracked_vehicle.vehicle_class, tracked_vehicle.confidence,
                                              tracked_vehicle.detection_row)

            # Draw detection lines and tracked vehicles on the frame
            for dl in self.detectionlines:
                cv2.line(frame, (dl[0], dl[1]), (dl[2], dl[3]), (255, 203, 48), 6)

            for tracked_vehicle in tracked_vehicles.values():
                tracked_vehicle.draw(frame)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--frame", required=True, help="path to input frame")
    ap.add_argument("-y", "--yolo", required=True, help="base path to YOLO directory")
    ap.add_argument("-n", "--names", help="base path to YOLO directory", default='torchweight/names.txt')
    ap.add_argument("-c", "--conf", type=float, default=0.2, help="minimum probability to filter weak detections")
    return vars(ap.parse_args())


args = parse_args()

if __name__ == "__main__":
    model = Model().loadModel(args)
    vehicle = VehicleDetection(model)
    vehicle.prediction(args)
