from xr_servo import Servo

CLAW_PORT = 4
OPENED_CLAW = 20
CLOSED_CLAW = 20

MAIN_PORT = 1
MAIN_UP = 180
MAIN_DOWN = 60
cur_main_angle = 0

CUBIT_PORT = 2
CUBIT_UP = 180
CUBIT_DOWN = 180
CUBIT_THROW = 90

WRIST_PORT = 3
WRIST_STRAIGHT = 50
WRIST_ROTATED = 70


class ServoController(Servo):
    cur_main_angle = MAIN_UP
    cur_cubit_angle = CUBIT_UP
    cur_wrist_angle = WRIST_ROTATED
    cur_claw_angle = OPENED_CLAW

    def __init__(self):
        super().__init__()
        self.set_default_position()
        self.close_claw()

    def set_default_position(self):
        self.cur_main_angle = MAIN_UP
        self.cur_cubit_angle = CUBIT_UP
        self.cur_wrist_angle = WRIST_ROTATED
        self.set_position()

    def close_claw(self):
        self.cur_claw_angle = CLOSED_CLAW
        self.set_position()

    def open_claw(self):
        self.cur_claw_angle = OPENED_CLAW
        self.set_position()

    def set_throw_position(self):
        self.cur_main_angle = MAIN_UP
        self.cur_cubit_angle = CUBIT_THROW
        self.cur_wrist_angle = WRIST_ROTATED
        self.set_position()

    def set_down_position(self):
        self.cur_main_angle = MAIN_DOWN
        self.cur_cubit_angle = CUBIT_DOWN
        self.cur_wrist_angle = WRIST_STRAIGHT
        self.set_position()

    def move_main(self, angle):
        self.cur_main_angle = self.angle_limit(angle + self.cur_main_angle)
        self.set_position()

    def move_cubit(self, angle):
        self.cur_cubit_angle = self.angle_limit(angle + self.cur_cubit_angle)
        self.set_position()

    def move_wrist(self, angle):
        self.cur_wrist_angle = self.angle_limit(angle + self.cur_wrist_angle)
        self.set_position()

    def move_claw(self, angle):
        self.cur_main_angle = self.angle_limit(angle + self.cur_claw_angle)
        self.set_position()

    def set_position(self):
        self.set(MAIN_PORT, self.cur_main_angle)
        self.set(CUBIT_PORT, self.cur_cubit_angle)
        self.set(WRIST_PORT, self.cur_wrist_angle)
        self.set(CLAW_PORT, self.cur_claw_angle)
