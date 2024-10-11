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
@Explain :主线程
@Time    :2020/05/09
@File    :xr_startmain.py
@Software: PyCharm
"""
from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call
from xr_car_light import Car_light
car_light = Car_light()
import xr_config as cfg
from xr_motor import RobotDirection
go = RobotDirection()
from xr_socket import Socket
socket = Socket()
from xr_infrared import Infrared
infrared = Infrared()
from xr_ultrasonic import Ultrasonic
ultrasonic = Ultrasonic()
from xr_camera import Camera
camera = Camera()
from xr_function import Function
function = Function()
from xr_oled import Oled
try:
    oled = Oled()
except:
    print('oled initialization fail')
from xr_music import Beep
beep = Beep()
from xr_power import Power
power = Power()
from xr_servo import Servo
servo = Servo()
from xr_ps2 import PS2
ps2 = PS2()
from xr_i2c import I2c
i2c = I2c()
from xr_voice import Voice
voice = Voice()


def cruising_mode():
	"""
	模式切换函数
	:return:none
	"""
	# print('pre_CRUISING_FLAG：{}'.format(cfg.PRE_CRUISING_FLAG))
	time.sleep(0.001)
	if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_FLAG:  # 如果循环模式改变
		cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # 在切换其他模式的时候,恢复上次保存的速度值
		cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
		if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_SET['normal']:	 # 如果循环模式改变，且上次的模式不是正常模式
			go.stop()	  # 先停止小车
		cfg.PRE_CRUISING_FLAG = cfg.CRUISING_FLAG	 # 重新赋值上次模式标志位

	if cfg.CRUISING_FLAG == cfg.CRUISING_SET['irfollow']:  # 进入红外跟随模式
		# print("Infrared.irfollow")
		infrared.irfollow()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['trackline']:  # 进入红外巡线模式
		# print("Infrared.trackline")
		infrared.trackline()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoiddrop']:  # 进入红外防掉落模式
		# print("Infrared.avoiddrop")
		infrared.avoiddrop()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoidbyragar']:  # 进入超声波壁障模式
		# print("Ultrasonic.avoidbyragar")
		ultrasonic.avoidbyragar()
		time.sleep(0.5)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['send_distance']:  # 进入超声波测距模式
		# print("Ultrasonic.send_distance")
		ultrasonic.send_distance()
		time.sleep(1)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['maze']:  # 进入超声波走迷宫模式
		# print("Ultrasonic.maze")
		ultrasonic.maze()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_normal']:  # 进入调试模式
		time.sleep(2)
		print("CRUISING_FLAG == 7")
		# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
		#call("%s" % path_sh, shell=True)
		cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_linepatrol']:  # 进入摄像头循迹操作
		function.linepatrol_control()
		time.sleep(0.01)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['qrcode_detection']:  # 进入摄像头二维码检测识别应用
		function.qrcode_control()
		time.sleep(0.01)
	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
		if cfg.VOICE_MOD == cfg.VOICE_MOD_SET['normal']:
			time.sleep(0.001)
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['openlight']:	 # 打开灯光
			car_light.open_light()
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['closelight']:	 # 关闭灯光
			car_light.close_light()
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['forward']:		# 往前进
			go.forward()
			time.sleep(2)
			go.stop()
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['back']:		# 往后退
			go.back()
			time.sleep(2)
			go.stop()
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['left']:		# 往左转
			cfg.LIGHT_STATUS = cfg.TURN_LEFT
			go.left()
			time.sleep(0.8)
			go.stop()
			cfg.LIGHT_STATUS = cfg.STOP
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['right']:		# 往右转
			cfg.LIGHT_STATUS = cfg.TURN_RIGHT
			go.right()
			time.sleep(0.8)
			go.stop()
			cfg.LIGHT_STATUS = cfg.STOP
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['stop']:		# 请停止
			go.stop()
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['nodhead']:		# 请点头
			for i in range(1, 4):
				if i:
					for j in range(90, 0, -5):
						print(j)
						servo.set(8, j)
						time.sleep(0.04)
					time.sleep(0.1)
			servo.set(8, 0)
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['shakehead']:	 # 请摇头
			for i in range(1, 3):
				if i:
					for j in range(45, 135, 5):
						# print(j)
						servo.set(7, j)
						time.sleep(0.02)
					time.sleep(0.1)
					for j in range(135, 45, -5):
						# print(j)
						servo.set(7, j)
						time.sleep(0.02)
					time.sleep(0.1)
			servo.set(7, 90)
			cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']

	else:
		time.sleep(0.001)


def status():
	"""
	状态更新函数，如车灯，OLED需要定时更新的功能都可以写在这里
	:return:
	"""
	if cfg.PROGRAM_ABLE:	 # 如果系统程序标志启动
		if cfg.LOOPS > 30:   # 更新函数是每隔0.1秒进入一次，这里等于0.3秒检测车子方向并根据车子方向开启对应转向灯
			if cfg.LIGHT_STATUS == cfg.TURN_FORWARD:
				cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS	 # 没进入控制方向时都讲此次状态赋值给上一次状态
				car_light.forward_turn_light()
			elif cfg.LIGHT_STATUS == cfg.TURN_BACK:
				cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
				car_light.back_turn_light()
			elif cfg.LIGHT_STATUS == cfg.TURN_LEFT:
				cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
				car_light.left_turn_light()
			elif cfg.LIGHT_STATUS == cfg.TURN_RIGHT:
				cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
				car_light.right_turn_light()
			elif cfg.LIGHT_STATUS == cfg.STOP and cfg.LIGHT_LAST_STATUS != cfg.LIGHT_STATUS:	 # 让STOP灯只在一直STOP情况下只执行一次
				cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
				if cfg.LIGHT_OPEN_STATUS == 1:
					car_light.open_light()
				else:
					car_light.close_light()
		if cfg.LOOPS > 100:  		# 定时器设定的是0.01秒进入一次，大于100表明自增了100次即1秒时间，一些不需要更新太快的数据显示函数可放这里
			cfg.LOOPS = 0			# 清除LOOPS
			power.show_vol()    	# 电量灯条电量显示
			try:
				oled.disp_cruising_mode()  	# oled显示模式
			except:
				print('oled initialization fail')

	loops = cfg.LOOPS   # 通过赋值给一个中间值来自增
	loops = loops + 1   # 自增
	cfg.LOOPS = loops   # 赋值回去

	loops = cfg.PS2_LOOPS   # 通过赋值给一个中间值来自增
	loops = loops + 1   # 自增
	cfg.PS2_LOOPS = loops   # 赋值回去

	Timer(0.01, status).start()  # 每进入一次需要重新开启定时器


if __name__ == '__main__':
	'''
	主程序入口
	'''
	print("....wifirobots start!...")

	os.system("sudo hciconfig hci0 name XiaoRGEEK")  # 设置蓝牙名称
	time.sleep(0.1)
	os.system("sudo hciconfig hci0 reset")  # 重启蓝牙
	time.sleep(0.3)
	os.system("sudo hciconfig hci0 piscan")  # 恢复蓝牙扫描功能
	time.sleep(0.2)
	print("now bluetooth discoverable")

	servo.restore()  		# 复位舵机
	try:
		oled.disp_default()		# oled显示初始化信息
	except:
		print('oled initialization fail')
# car_light.init_led() 	# 车灯秀
time.sleep(0.1)

threads = []  # 创建一个线程序列
t1 = threading.Thread(target=camera.run, args=())  # 摄像头数据收集处理线程
threads.append(t1)  # 将线程添加到线程队列中
t2 = threading.Thread(target=socket.bluetooth_server, args=())  # 新建蓝牙线程
threads.append(t2)
t3 = threading.Thread(target=socket.tcp_server, args=())  # 新建wifi tcp通信线程
threads.append(t3)
t4 = threading.Thread(target=voice.run, args=())  	# 语音模块线程
threads.append(t4)

ti = threading.Timer(0.1, status)		# 新建一个定时器
ti.start()		# 开启定时器

path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'  # start_mjpg_streamer启动指令
call("%s" % path_sh, shell=True)  # 新开一个进程运行start_mjpg_streamer
time.sleep(1)

for t in threads:
	#print("theads %s ready to start..." % t)
	t.setDaemon(True)  # 将线程设置为守护线程
	t.start()  # 启动线程
	time.sleep(0.05)
# print("theads %s start..." %t)
print("all theads start...>>>>>>>>>>>>")
servo.store()		# 恢复小车保存的舵机角度
go.motor_init()		# 恢复小车保存的电机速度
while True:
	try:
		if cfg.PROGRAM_ABLE:	 # 如果系统程序标志启动
			cfg.PS2_LOOPS = cfg.PS2_LOOPS + 1
			if cfg.PS2_LOOPS > 20:
				ps2.control()
				cfg.PS2_LOOPS = 0
		cruising_mode() 										# 主线程中运行模式切换功能
	except Exception as e:										# 捕获并打印出错信息
		time.sleep(0.1)
		print('cruising_mod error:', e)

