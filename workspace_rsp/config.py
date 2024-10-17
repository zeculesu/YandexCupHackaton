#HOST PORT
PORT = 4141

# Buzzer
from tkinter import YView

BEET_SPEED = 35
CLAPPER = 4

# Header and end caption
HEADER = 0xff

# Servo vars
ANGLE_MAX = 180
ANGLE_MIN = 0

CAM_CUBIT_PORT = 8
CAM_ROTATE_PORT = 7
CAM_CUBIT_DEFAULT = 110
CAM_ROTATE_DEFAULT = 85
CAM_CUBIT_MIN = 90

CLAW_PORT = 4
OPENED_CLAW = 40
CLOSED_CLAW = 88
CUBE_GRAB_ANGLE = 70

MAIN_PORT = 1
MAIN_UP = 150
MAIN_DOWN = 65
cur_main_angle = 0

CUBIT_PORT = 2
CUBIT_DEFAULT = 180
CUBIT_THROW = 100

WRIST_PORT = 3
WRIST_STRAIGHT = 90
WRIST_ROTATED = 175

# Motor vars
STEP_TIME = 0.1
DEFAULT_SPEED = 50

# RGB Panels
RGB_POWER = 1
RGB_PANEL = 2

BLACK = 0
RED = 1
YELLOW = 2
SALAD = 3
GREEN = 4
LIGHT_BLUE = 5
BLUE = 6
PURPLE = 7
WHITE = 8

# OLED
LOGO = "4+1 TM"  # OLED显示屏显示的信息是英文
OLED_DISP_MOD = ["正常模式", "红外跟随", "红外巡线", "红外防掉落", "超声波避障",
                 "超声波距离显示", "超声波走迷宫", "摄像头调试",
                 "摄像头巡线", "人脸检测跟随", "颜色检测跟随", "二维码识别",
                 ]  # 模式显示的是中文
OLED_DISP_MOD_SIZE = 16
POWER = 3  # 电量值0-3
DISTANCE = 0  # 超声波测距值
CRUISING_FLAG = 0
