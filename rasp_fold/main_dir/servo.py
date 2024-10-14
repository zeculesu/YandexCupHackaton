from i2c import I2c
import config as cfg


def angle_limit(angle):
    if angle > cfg.ANGLE_MAX:
        angle = cfg.ANGLE_MAX
    elif angle < cfg.ANGLE_MIN:
        angle = cfg.ANGLE_MIN
    return angle


class ServoController(object):
    cur_main_angle = cfg.MAIN_UP
    cur_cubit_angle = cfg.CUBIT_DEFAULT
    cur_wrist_angle = cfg.WRIST_ROTATED
    cur_claw_angle = cfg.OPENED_CLAW

    def __init__(self):
        super().__init__()
        self.i2c = I2c()
        self.set_default_position()
        self.close_claw()

    def set_default_position(self):
        self.cur_main_angle = cfg.MAIN_UP
        self.cur_cubit_angle = cfg.CUBIT_DEFAULT
        self.cur_wrist_angle = cfg.WRIST_ROTATED
        self.set_position()

    def close_claw(self):
        self.cur_claw_angle = cfg.CLOSED_CLAW
        self.set_position()

    def open_claw(self):
        self.cur_claw_angle = cfg.OPENED_CLAW
        self.set_position()

    def set_throw_position(self):
        self.cur_main_angle = cfg.MAIN_UP
        self.cur_cubit_angle = cfg.CUBIT_THROW
        self.cur_wrist_angle = cfg.WRIST_ROTATED
        self.set_position()

    def set_down_position(self):
        self.cur_main_angle = cfg.MAIN_DOWN
        self.cur_cubit_angle = cfg.CUBIT_DEFAULT
        self.cur_wrist_angle = cfg.WRIST_STRAIGHT
        self.set_position()

    def move_main(self, angle):
        self.cur_main_angle = angle_limit(angle + self.cur_main_angle)
        self.set_position()

    def move_cubit(self, angle):
        self.cur_cubit_angle = angle_limit(angle + self.cur_cubit_angle)
        self.set_position()

    def move_wrist(self, angle):
        self.cur_wrist_angle = angle_limit(angle + self.cur_wrist_angle)
        self.set_position()

    def move_claw(self, angle):
        self.cur_main_angle = angle_limit(angle + self.cur_claw_angle)
        self.set_position()

    def set_position(self):
        self.set(cfg.MAIN_PORT, self.cur_main_angle)
        self.set(cfg.CUBIT_PORT, self.cur_cubit_angle)
        self.set(cfg.WRIST_PORT, self.cur_wrist_angle)
        self.set(cfg.CLAW_PORT, self.cur_claw_angle)

    def set(self, servo_port, angle):
        angle = angle_limit(angle)
        buf = [0xff, 0x01, servo_port, angle, 0xff]
        try:
            self.i2c.write_data(self.i2c.mcu_address, buf)
        except Exception as e:
            print('servo write error:', e)
