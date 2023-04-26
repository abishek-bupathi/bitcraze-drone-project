
import cv2
from orange_detector import OrangeDetector
from kalmanfilter import KalmanFilter
import numpy as np
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M/E7E7E7E7E7'
cflib.crtp.init_drivers(enable_debug_driver=False)
drone_pos_x = 500
drone_pos_y = 220

K = np.array([[1398.8, 0, 946.3022],
              [0, 1389.2, 536.2068],
              [0, 0, 1]])
dist_coef = np.array([0.1118, -0.1749, 0, 0, 0])

cap = cv2.VideoCapture(1)

# Load detector
od = OrangeDetector()

# Load Kalman filter to predict the trajectory
kf = KalmanFilter()

# Create empty list to store previous points
prev_points = []

with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf, default_height=0.3) as mc:
            while True:
                ret, frame = cap.read()
                if ret is False:
                    break
    
                frame = cv2.undistort(frame, K, dist_coef)


                orange_bbox = od.detect(frame)
                x, y, x2, y2 = orange_bbox
                cx = int((x + x2) / 2)
                cy = int((y + y2) / 2)
                #print("Current position of ball: x "+str(cx)+", y "+str(cy))

                predicted = kf.predict(cx, cy)

                # Add predicted point to list of previous points
                prev_points.append(predicted)
    
                # Keep only the last 20 points
                if len(prev_points) > 20:
                    prev_points = prev_points[-20:]

                # Fit a quadratic using previous 3 points and predict next point
                if len(prev_points) >= 3:
                    x = np.array([p[0] for p in prev_points])
                    y = np.array([p[1] for p in prev_points])
                    if x.all() != 0 or y.all() != 0:
                        z = np.polyfit(x, y, 2)
                        f = np.poly1d(z)
                        next_x = predicted[0] + 50  # arbitrary offset for visualization
                        next_y = int(f(next_x))

                        # Compute angle of line using the slope of the quadratic
                        dy = f(next_x+10) - f(next_x)
                        dx = 10
                        angle = np.arctan2(dy, dx)

                        # Draw predicted point and quadratic with arrow
                        cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)
                        points = np.array([(x, int(f(x))) for x in range(int(next_x) - 100, int(next_x) + 100)])
                        cv2.polylines(frame, [points], False, (255, 255, 0), thickness=2)
                        
                        if len(points) >= 2:
                            p1 = tuple(points[-2])
                            p2 = tuple(points[-1])
                            cv2.arrowedLine(frame, p1, p2, (255, 255, 0), thickness=2, tipLength=4)

                            end_point_text = "End Point: ({}, {})".format(p2[0], p2[1])
                            cv2.putText(frame, end_point_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


                            # Print out the end point of the fitted polynomial line
                            #end_point = (int(next_x), next_y)
                            #print("End point of fitted polynomial line:", end_point)

                            # Check collision with drone
                
                            if abs(p2[0]-drone_pos_x) < 30 and abs(p2[1]-drone_pos_y) < 30:
                                mc.left(0.3, 1)
                                time.sleep(1)
                                mc.right(0.3, 1)

                           
                # Draw current point
                cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4)

                

                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break