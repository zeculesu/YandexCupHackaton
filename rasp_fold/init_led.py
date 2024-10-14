from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call

from xr_car_light import Car_light

car_light = Car_light()


while True:
    car_light.init_led()
    time.sleep(5)