from servo import ServoController, angle_limit
import config as cfg
from servo import claw_limit
from servo import main_manipulator_angle_limit


class ManipulatorController(ServoController):

    def __init__(self):
        super().__init__()
        self.cur_main_angle = cfg.MAIN_UP
        self.cur_cubit_angle = cfg.CUBIT_DEFAULT
        self.cur_wrist_angle = cfg.WRIST_ROTATED
        self.cur_claw_angle = cfg.OPENED_CLAW
        self.set_default_position()
        self.close_claw()

    def set_default_position(self) -> None:
        self.cur_main_angle = cfg.MAIN_UP
        self.cur_cubit_angle = cfg.CUBIT_DEFAULT
        self.cur_wrist_angle = cfg.WRIST_ROTATED
        self.set_position()

    def close_claw(self) -> None:
        self.cur_claw_angle = cfg.CLOSED_CLAW
        self.set_position()

    def grab_cube(self):
        self.cur_claw_angle = cfg.CUBE_GRAB_ANGLE
        self.set_position()

    def open_claw(self) -> None:
        self.cur_claw_angle = cfg.OPENED_CLAW
        self.set_position()

    def set_throw_position(self) -> None:
        self.cur_main_angle = cfg.MAIN_UP
        self.cur_cubit_angle = cfg.CUBIT_THROW
        self.cur_wrist_angle = cfg.WRIST_STRAIGHT
        self.set_position()

    def set_down_position(self) -> None:
        self.cur_main_angle = cfg.MAIN_DOWN
        self.cur_cubit_angle = cfg.CUBIT_DEFAULT
        self.cur_wrist_angle = cfg.WRIST_STRAIGHT
        self.set_position()

    def move_main(self, angle: int) -> None:
        self.cur_main_angle = main_manipulator_angle_limit(angle + self.cur_main_angle)
        self.set_position()

    def move_cubit(self, angle: int) -> None:
        self.cur_cubit_angle = angle_limit(angle + self.cur_cubit_angle)
        self.set_position()

    def move_wrist(self, angle: int) -> None:
        self.cur_wrist_angle = angle_limit(angle + self.cur_wrist_angle)
        self.set_position()

    def move_claw(self, angle: int) -> None:
        self.cur_claw_angle = claw_limit(angle + self.cur_claw_angle)
        self.set_position()

    def set_position(self) -> None:
        self.set(cfg.MAIN_PORT, self.cur_main_angle)
        self.set(cfg.CUBIT_PORT, self.cur_cubit_angle)
        self.set(cfg.WRIST_PORT, self.cur_wrist_angle)
        self.set(cfg.CLAW_PORT, self.cur_claw_angle)
