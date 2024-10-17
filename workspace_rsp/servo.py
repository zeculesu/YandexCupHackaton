import config as cfg
from i2c import I2c
from config import ANGLE_MAX


def angle_limit(angle):
    if angle > cfg.ANGLE_MAX:
        angle = cfg.ANGLE_MAX
    elif angle < cfg.ANGLE_MIN:
        angle = cfg.ANGLE_MIN
    return angle

def claw_limit(angle):
    if angle > cfg.CLOSED_CLAW:
        angle = cfg.CLOSED_CLAW
    elif angle < cfg.OPENED_CLAW:
        angle = cfg.OPENED_CLAW
    return angle

def cubit_cam_limit(angle):
    if angle > cfg.ANGLE_MAX:
        angle = cfg,ANGLE_MAX
    elif angle < cfg.CAM_CUBIT_MIN:
        angle = cfg.CAM_CUBIT_MIN
    return angle

class ServoController(object):

    def __init__(self):
        self.i2c = I2c()

    def set_default_position(self) -> None:
        pass

    def set_position(self) -> None:
        pass

    def set(self, servo_port: int, angle) -> None:
        angle = angle_limit(angle)
        buf = [cfg.HEADER, 0x01, servo_port, angle, cfg.HEADER]
        try:
            self.i2c.write_data(self.i2c.mcu_address, buf)
        except Exception as e:
            print('servo write error:', e)
