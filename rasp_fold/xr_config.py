# coding:utf-8
"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :配置文件
@contact :
@Time    :2020/05/09
@File    :xr_config.py
@Software: PyCharm
"""

from socket import *
import numpy as np


CRUISING_FLAG = 0  			# 当前循环模式，不同标志位进入不同模式，由上位机软件下发不同模式来改变参数。
PRE_CRUISING_FLAG = 0  		# 预循环模式
CRUISING_SET = {'normal': 0, 'irfollow': 1, 'trackline': 2, 'avoiddrop': 3, 'avoidbyragar': 4, 'send_distance': 5,
		 'maze': 6, 'camera_normal': 7, 'camera_linepatrol': 8, 'facefollow':9, 'colorfollow':10, 'qrcode_detection':11}
CAMERA_MOD_SET = {'camera_normal': 0, 'camera_linepatrol': 1, 'facefollow':2, 'colorfollow':3, 'qrcode_detection':4}

ANGLE_MAX = 160  			# 舵机角度上限值，防止舵机卡死，可设置小于180的数值
ANGLE_MIN = 15  			# 舵机角度下限值，防止舵机卡死，可设置大于0的数值

VOICE_MOD = 0
VOICE_MOD_SET = {'normal': 0, 'openlight': 1, 'closelight': 2, 'forward': 3, 'back': 4, 'left': 5,
		 'right': 6, 'stop': 7, 'nodhead': 8, 'shakehead':9}

PATH_DECT_FLAG = 0  		# 摄像头巡线标志位，0为巡黑线（浅色地面，深色线）；1为巡白线（深色地面，浅色线）

LEFT_SPEED = 80  			# 机器人左侧速度
RIGHT_SPEED = 80  			# 机器人右侧速度
LASRT_LEFT_SPEED = 100  	# 上一次机器人左侧速度
LASRT_RIGHT_SPEED = 100  	# 上一次机器人右侧速度

SERVO_NUM = 1				# 舵机号
SERVO_ANGLE = 90			# 舵机角度
SERVO_ANGLE_LAST = 90		# 上一次舵机角度
ANGLE = [90, 90, 90, 90, 90, 90, 90, 5]		# 8个舵机存储的角度

DISTANCE = 0  			# 超声波测距值
AVOID_CHANGER = 1  		# 超声波避障启动标志
AVOIDDROP_CHANGER = 1 	# 红外防跌落启动标志

MAZE_TURN_TIME = 400    # 迷宫状态转向角度设置

CAMERA_MOD = 0  		# 摄像头模式
LINE_POINT_ONE = 320  	# 摄像头巡线线1 x方向坐标
LINE_POINT_TWO = 320  	# 摄像头巡线线2 x方向坐标

CLAPPER = 4  			# 蜂鸣器音乐节拍
BEET_SPEED = 50  		# 蜂鸣器播放速度
TUNE = 0  				# 钢琴音调默认为C调0-6对应CDEFGAB

VREF = 5.12  			# 参考电压值
POWER = 3  				# 电量值0-3
LOOPS = 0  				# 定时检测值
PS2_LOOPS = 0  			# 定时检测值

PROGRAM_ABLE = True		# 系统程序运行状态

LIGHT_STATUS = 0  		# 车灯状态
LIGHT_LAST_STATUS = 0  	# 上一次车灯状态
LIGHT_OPEN_STATUS = 0   # 车灯打开状态
STOP = 1  				# 车灯停止状态
TURN_FORWARD = 2 		# 车灯前进状态
TURN_BACK = 3			# 车灯后退状态
TURN_LEFT = 4  			# 车灯左转状态
TURN_RIGHT = 5  		# 车灯右转状态
POWER_LIGHT = 1  		# 设置电量灯组标志
CAR_LIGHT = 2  			# 设置车灯组标志

# RGB灯的颜色值设定，有且只有这几组灯的颜色，不可设置其他颜色
COLOR = {'black': 0, 'red': 1, 'orange': 2, 'yellow': 3, 'green': 4, 'Cyan': 5,
		 'blue': 6, 'violet': 7, 'white': 8}

LOGO = "XiaoR GEEK"  # OLED显示屏显示的信息是英文
OLED_DISP_MOD = ["正常模式", "红外跟随", "红外巡线", "红外防掉落", "超声波避障",
				 "超声波距离显示", "超声波走迷宫", "摄像头调试",
				 "摄像头巡线", "人脸检测跟随", "颜色检测跟随", "二维码识别",
				 ]  # 模式显示的是中文
OLED_DISP_MOD_SIZE = 16  # 中文一个字占用16像素的大小，如果模式显示字体改成英文则将这个值改成8

BT_CLIENT = False  	# 蓝牙客户端
TCP_CLIENT = False  # TCP客户端
RECV_LEN = 5 		# 接收的字符长度

# 蓝牙服务端参数设置
try:
	BT_SERVER = socket(AF_INET, SOCK_STREAM)
	BT_SERVER.bind(('', 2002))		# 蓝牙绑定2002端口
	BT_SERVER.listen(1)
	# TCP服务端参数设置
	TCP_SERVER = socket(AF_INET, SOCK_STREAM)
	TCP_SERVER.bind(('', 2001))  # WIFI绑定2002端口
	TCP_SERVER.listen(1)
except Exception:
	pass



# PS2手柄按键定义
PS2_ABLE = False		# PS2手柄是否正常连接标志
PS2_READ_KEY = 0		# 读取的PS2手柄值
PS2_LASTKEY = 0			# 读取的PS2手柄上一次的值
PS2_KEY = {'PSB_PAD_UP': 1, 'PSB_PAD_DOWN': 2, 'PSB_PAD_LEFT': 3, 'PSB_PAD_RIGHT': 4,
'PSB_RED': 5, 'PSB_PINK': 6, 'PSB_GREEN': 7, 'PSB_BLUE': 8}		# 手柄左侧上下左右及右侧功能按键

# 颜色检测跟随的颜色区间
# 颜色区间低阀值
COLOR_LOWER = [
	# 红色
	np.array([0, 43, 46]),
	# 绿色
	np.array([35, 43, 46]),
	# 蓝色
	np.array([100, 43, 46]),
	# 紫色
	np.array([125, 43, 46]),
	# 橙色
	np.array([11, 43, 46])
]
# 颜色区间高阀值
COLOR_UPPER = [
	# 红色
	np.array([10, 255, 255]),
	# 绿色
	np.array([77, 255, 255]),
	# 蓝色
	np.array([124, 255, 255]),
	# 紫色
	np.array([155, 255, 255]),
	# 橙色
	np.array([25, 255, 255])
]
COLOR_FOLLOW_SET = {'red': 0, 'green': 1, 'blue': 2, 'violet': 3, 'orange': 4}		# 颜色跟随功能颜色区间下标设置，在socket通信中使用
COLOR_INDEX = 0			# 颜色区间阈值下标，在socket通信中改变


BARCODE_DATE = None		# 二维码识别数据
BARCODE_TYPE = None		# 二维码识别数据类型
