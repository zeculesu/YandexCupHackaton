from servo import ServoController, angle_limit
import config as cfg


class CameraController(ServoController):

    def __init__(self):
        super().__init__()
        self.cur_cubit_angle = cfg.CAM_CUBIT_DEFAULT
        self.cur_rotate_angle = cfg.CAM_ROTATE_DEFAULT
        self.set_default_position()

    def set_default_position(self) -> None:
        self.cur_cubit_angle = cfg.CAM_CUBIT_DEFAULT
        self.cur_rotate_angle = cfg.CAM_ROTATE_DEFAULT
        self.set_position()

    def set_position(self) -> None:
        self.set(cfg.CAM_CUBIT_PORT, self.cur_cubit_angle)
        self.set(cfg.CAM_ROTATE_PORT, self.cur_rotate_angle)

    def move_cubit(self, angle: int) -> None:
        self.cur_cubit_angle = angle_limit(angle + self.cur_cubit_angle)
        self.set_position()

    def move_rotate(self, angle: int) -> None:
        self.cur_rotate_angle = angle_limit(angle + self.cur_rotate_angle)
        self.set_position()
