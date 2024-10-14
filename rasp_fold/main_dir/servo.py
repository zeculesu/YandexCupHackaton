from i2c import I2c
import config as cfg


def angle_limit(angle):
    if angle > cfg.ANGLE_MAX:
        angle = cfg.ANGLE_MAX
    elif angle < cfg.ANGLE_MIN:
        angle = cfg.ANGLE_MIN
    return angle


class ServoController(object):

    def __init__(self):
        self.i2c = I2c()

    def set_default_position(self):
        pass

    def set_position(self):
        pass

    def set(self, servo_port, angle):
        angle = angle_limit(angle)
        buf = [cfg.HEADER, 0x01, servo_port, angle, cfg.HEADER]
        try:
            self.i2c.write_data(self.i2c.mcu_address, buf)
        except Exception as e:
            print('servo write error:', e)
