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
        with MotionCommander(scf, default_height=0.6) as mc:
            
            print('Taking off!')
            time.sleep(2)
            mc._cf.commander.send_stop_setpoint()
            #mc._is_flying = False

            time.sleep(2)

            mc.up(0.5, 0.7)
            
            mc._is_flying = True
            
            mc._thread.start()
            
            mc._cf.commander.send_stop_setpoint()
            
            time.sleep(2)

            mc.up(0.5, 0.7)
            
            mc._is_flying = True
            
            mc._thread.start()

            mc._cf.commander.send_stop_setpoint()
            time.sleep(2)

            mc.up(0.5, 0.7)
            
            mc._is_flying = True
            
            mc._thread.start()

            time.sleep(3)

            
            mc.land()

            #for i in range (0, 10):
            #     
            #    
            #    print('Moving down 0.2m')
            #    #mc.down(0.2, 0.75)

            #    # Wait a bit
            #    time.sleep(0.1)
            #

            #    print('Moving down 0.2m')
            #    mc.right(0.3, 0.5)

            #    # Wait a bit
            #    time.sleep(0.2)
            #
            #    print('Moving down 0.2m')
            #    mc.left(0.3, 0.5)

            #    # Wait a bit
            #    time.sleep(0.2)

            #    #mc.up(0.2, 0.75)

            #    # Wait a bit
            #    time.sleep(0.1)

            # We land when the MotionCommander goes out of scope
            print('Landing!')



"""
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

% Commands

% Turning left
mc.turn_left(90)

% Turning right
mc.turn_right(90)

"""