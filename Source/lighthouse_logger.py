
"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig

# URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
URI = 'radio://0/80/2M/E7E7E7E7E7'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def log_pos_config():
    log_config = LogConfig(name="KinematicsLog", period_in_ms=10)
    log_config.add_variable("stateEstimate.x", "float")
    log_config.add_variable("stateEstimate.y", "float")
    log_config.add_variable("stateEstimate.z", "float")
    return log_config

def pos_callback(timestamp, data, pos_config):
    x, y, z = (data["stateEstimate.x"],
               data["stateEstimate.y"],
               data["stateEstimate.z"])
    #print(str(x)+" "+str(y)+" "+str(z))
    return x, y, z

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache="./cache")) as scf:
        # We take off when the commander is created
        with PositionHlCommander(scf, default_height=0.5) as pc:

            cf = scf.cf

            log_config = log_pos_config()

            cf.log.add_config(log_config)
            log_config.start()
            print(log_config.__dir__())
           
            
            while(True):
                log_config.data_received_cb.add_callback(pos_callback)
                time.sleep(1)

                

            
            #print('Taking off!')
            #time.sleep(2)
            #currentPosition = pc.get_position()
            #print('Initial position: ' + str(currentPosition))
            #pc.go_to(0.5,0.5,1)
            #currentPosition = pc.get_position()
            #print('Final position: ' + str(currentPosition))
            #time.sleep(2)
         
            #for i in range (0, 5):
                
            #    mc.right(0.5, 1)
            #    # wait a bit
            #    time.sleep(1)

                
            #    mc.left(0.5, 1)
            #    # wait a bit
            #    time.sleep(1)

            #   # mc.forward(0.2)
                

    
            print('Landing!')






"""
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

% Commands

% Turning left
mc.turn_left(90)

% Turning right
mc.turn_right(90)

"""