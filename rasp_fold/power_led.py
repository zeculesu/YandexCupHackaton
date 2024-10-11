from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call

from xr_car_light import Car_light

car_light = Car_light()

import xr_config as cfg

while True:
    car_light.set_ledgroup(cfg.POWER_LIGHT, 8, cfg.COLOR['green'])  # 设置电量灯条为绿色
    time.sleep(5)
    car_light.set_ledgroup(cfg.POWER_LIGHT, 6, cfg.COLOR['orange'])
    time.sleep(5)
    car_light.set_ledgroup(cfg.POWER_LIGHT, 2, cfg.COLOR['red'])
    time.sleep(5)