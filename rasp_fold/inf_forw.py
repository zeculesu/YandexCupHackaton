import time

import xr_motor

rd = xr_motor.RobotDirection()
try:
    while True:
        rd.forward()
        time.sleep(2)
        rd.right()
        time.sleep(2)
        rd.stop()
except KeyboardInterrupt:
    rd.stop()
    print("keyboard interrupt")
    quit()
