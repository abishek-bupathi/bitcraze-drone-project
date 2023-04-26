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

URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf, default_height=0.3) as mc:
            
            print('Taking off!')
            time.sleep(2)
            mc.up(0.8)
            mc.forward(0.2)
            mc.turn_left(90)
            mc.back(0.1)
            mc.turn_left(90)
            mc.forward(0.2)
            mc.down(0.8)
            
                
            print('Landing!')



"""
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

% Commands

% Turning left
mc.turn_left(90)

% Turning right
mc.turn_right(90)

"""