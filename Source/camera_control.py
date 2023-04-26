"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
import cv2
import numpy as np

URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
        # Capture video from default camera
    cap = cv2.VideoCapture(0)

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf, default_height=0.5) as mc:
 
            while True:
                # Read a new frame
                ret, frame = cap.read()
                if not ret:
                    print("Error: failed to capture frame.")
                    break

                # Display the frame
                cv2.imshow("Ping Pong Ball Tracker", frame)
                
                # Convert frame to HSV color space
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
                # Define the lower and upper bounds of the red color in HSV color space
                lower_red = np.array([0, 120, 70])
                upper_red = np.array([10, 255, 255])
                mask1 = cv2.inRange(hsv, lower_red, upper_red)
            
                lower_red = np.array([170, 120, 70])
                upper_red = np.array([180, 255, 255])
                mask2 = cv2.inRange(hsv, lower_red, upper_red)
            
                # Combine masks to obtain the final mask
                mask = cv2.bitwise_or(mask1, mask2)
            
                # Find the contours of the ball in the mask
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # If contours were found, track the ball
                if len(contours) > 0:
                    # Find the largest contour, which is most likely the ball
                    c = max(contours, key=cv2.contourArea)
            
                    # Get the center and radius of the ball
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
            
                    # Draw a circle around the ball
                    if radius > 5:
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        
                        #print(y)

                        if (y < 200):
                            mc.up(0.5, 0.5)
                            
                        if (y > 210):
                            mc.down(0.2, 0.5)
                           
                        

                    
           
        
            print('Landing!')



"""
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

% Commands

% Turning left
mc.turn_left(90)

% Turning right
mc.turn_right(90)

"""