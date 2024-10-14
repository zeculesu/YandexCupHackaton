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
@Explain :socket数据接收发送
@Time    :2020/05/09
@File    :xr_socket.py
@Software: PyCharm
"""
from builtins import range, str, eval, hex, int, object, type, abs, Exception, repr, bytes, len

import os
import time
import xr_config as cfg

from subprocess import call

from xr_motor import RobotDirection
go = RobotDirection()

from xr_servo import Servo
servo = Servo()

from xr_car_light import Car_light
car_light = Car_light()

from xr_music import Beep
beep = Beep()


class Socket:
	def __init__(self):
		self.rec_flag = 0  # 0xff字节接收标志
		self.count = 0  # 数据接收计数器标志
		self.client = None

	def sendbuf(self, buf):
		time.sleep(0.2)
		# print('TCP_CLIENT:%s++++++++BT_CLIENT:%s' % (cfg.TCP_CLIENT, cfg.BT_CLIENT))
		if cfg.TCP_CLIENT != False:
				try:
					cfg.TCP_CLIENT.send(buf)
					time.sleep(0.005)
					print('tcp send ok!!!')
				except Exception as e:  # 发送出错
					print('tcp send error:', e)  # 打印出错信息

		if cfg.BT_CLIENT != False:
				try:
					cfg.BT_CLIENT.send(buf)
					time.sleep(0.005)
					print('bluetooth send ok!!!')
				except Exception as e:  # 发送出错
					print('bluetooth send error:', e)  # 打印出错信息

	def load_server(self, server, servername):
		"""
		socket服务函数
		参数：self实例类，参数server要启动的服务，buf接收的数据，servername要启动的服务类型名称
		"""
		while True:
			time.sleep(0.1)
			print("waitting for %s connection..." % servername, "\r")

			if servername == 'bluetooth':  # 如果选择的是bluetooth通信
				cfg.BT_CLIENT = False		#启动蓝牙的服务的时候先把蓝牙服务关闭
				cfg.BT_CLIENT, socket_address = server.accept()  # 初始化socket，并创建一个客户端和地址
				client = cfg.BT_CLIENT
				time.sleep(0.1)
				print(str(socket_address[0]) + " %s connected!" % servername + "\r")  # 打印客户端和地址

			elif servername == 'tcp':  # 如果选择的是wifi通信
				cfg.TCP_CLIENT = False	#启动tcp的服务的时候先把tcp服务关闭
				cfg.TCP_CLIENT, socket_address = server.accept()  # 初始化socket，并创建一个客户端和地址
				client = cfg.TCP_CLIENT
				time.sleep(0.1)
				print(str(socket_address[0]) + "%s connected!" % servername + "\r")  # 打印客户端和地址

			while True:
				try:
					data = client.recv(cfg.RECV_LEN)  # cfg.RECV_LEN一次接收的字符长度
					#print(data)
					if len(data) < cfg.RECV_LEN:  # 不符合接收长度标准
						#print('data len %d:'%len(data))
						break
					if data[0] == 0xff and data[len(data) - 1] == 0xff:  # 如果包头和包尾是0xff则符合小二科技通信协议
						buf = []  # 定义一个列表
						for i in range(1, 4):  # 获取协议包中间3位的数据
							buf.append(data[i])  # 往buf中添加数据
						self.communication_decode(buf)  # 运行串口解析数据
				except Exception as e:  # 接收出错
					time.sleep(0.1)
					print('socket received error:', e)  # 打印出错信息

			client.close()		# 关闭客户端
			client = None
			go.stop()
		go.stop()
		server.close()

	def communication_decode(self, buffer):
		"""
		数据解析函数，根据socket过滤出来的数据即小R科技通信协议按位解析成对应的功能及动作
		协议格式---------------------0xff		0xXX		0xXX		0xXX		0xff
		表示含义---------------------包头		类型位	    控制位		数据位		包尾
		socket过滤后的数据buffer[]---		   buffer[0]   buffer[1]   buffer[2]
		"""
		print(buffer)
		if buffer[0] == 0x00:  # buffer[0]表示类型位，等于0x00表示这个数据包为电机控制指令的数据包
			if buffer[1] == 0x01:  # buffer[1]表示控制位，等于0x01表示为前进的数据包
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:	# 判断超声波避障和红外防跌落状态是否为无障碍物或正常路面无断落边缘的状态，这个俩个标志默认为1，这样可保证其前方有障碍物或者防跌落中有断落边缘时不会前进
					go.forward()  # 前进

			elif buffer[1] == 0x02:
				go.back()  # 后退

			elif buffer[1] == 0x03:
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:
					cfg.LIGHT_STATUS = cfg.TURN_LEFT
					go.left()  # 左转

			elif buffer[1] == 0x04:
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:
					cfg.LIGHT_STATUS = cfg.TURN_RIGHT
					go.right()  # 右转

			elif buffer[1] == 0x00:
				cfg.LIGHT_STATUS = cfg.STOP
				go.stop()  # 停止

			else:
				go.stop()

		elif buffer[0] == 0x01:  # 控制舵机指令
			cfg.SERVO_NUM = buffer[1]  # 获取舵机号
			cfg.SERVO_ANGLE = buffer[2]  # 获取舵机角度
			if abs(cfg.SERVO_ANGLE - cfg.SERVO_ANGLE_LAST) > 2:  # 限制舵机重复下发角度
				cfg.ANGLE[cfg.SERVO_NUM-1] = cfg.SERVO_ANGLE
				servo.set(cfg.SERVO_NUM, cfg.SERVO_ANGLE)

		elif buffer[0] == 0x02:  # 调节电机速度
			if buffer[1] == 0x01:  # 调节左侧电机速度
				cfg.LEFT_SPEED = buffer[2]
				go.set_speed(1, cfg.LEFT_SPEED)	 # 设置左侧速度
				go.save_speed()

			elif buffer[1] == 0x02:  # 调节右侧电机速度
				cfg.RIGHT_SPEED = buffer[2]
				go.set_speed(2, cfg.RIGHT_SPEED)  # 设置右侧速度
				go.save_speed()

		elif buffer[0] == 0x06:  # 设置颜色检测跟随功能中的跟随颜色
			if buffer[1] == 0x01:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['red']		# 设置颜色检测颜色区间为红色
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['red'])	 # 设置车灯为红色，提示作用
			elif buffer[1] == 0x02:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['green']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['green'])
			elif buffer[1] == 0x03:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['blue']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
			elif buffer[1] == 0x04:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['violet']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['violet'])
			elif buffer[1] == 0x05:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['orange']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['orange'])
			time.sleep(1)

		elif buffer[0] == 0x13:
			if buffer[1] == 0x01 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['irfollow']  	 # 进入红外跟随模式

			elif buffer[1] == 0x02 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']: 	 # 进入红外巡线模式
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['trackline']

			elif buffer[1] == 0x03 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']: 	 # 进入红外防跌落模式
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoiddrop']

			elif buffer[1] == 0x04 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  	 # 进入超声波避障模式
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoidbyragar']

			elif buffer[1] == 0x05 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  	 # 进入超声波距离app显示
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['send_distance']

			elif buffer[1] == 0x06 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:		 # 进入超声走迷宫
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				servo.set(1, 165)
				servo.set(2, 15)
				servo.set(3, 90)
				servo.set(4, 90)
				servo.set(7, 90)
				servo.set(8, 0)
				cfg.MAZE_TURN_TIME = buffer[2]*10
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['maze']

			elif buffer[1] == 0x07:
				cfg.PROGRAM_ABLE = True
				servo.set(1, 165)
				servo.set(2, 15)
				servo.set(3, 90)
				servo.set(4, 90)
				servo.set(7, 90)
				servo.set(8, 0)
				if buffer[2] == 0x00:  	 # 摄像头巡线调试模式，即正常开启视频传输模式
					go.stop()  # 停止
					cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # 将保存的速度复位
					cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
					cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_normal']
					cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_normal']
					car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])	 # 从颜色检测识别跟随模式中退出需要关闭车灯

				elif buffer[2] == 0x01:  # 摄像头巡线模式
					cfg.PROGRAM_ABLE = False
					cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
					cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
					cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_linepatrol']
					cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_linepatrol']
					# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'	# 结束摄像头视频流命令
					#call("%s" % path_sh, shell=True)	 # 启动shell命令结束摄像头视频流，一会摄像头巡线时使用opencv占用摄像头
					time.sleep(2)
			elif buffer[1] == 0x08:	 # 摄像头人脸检测跟随模式
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['facefollow']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['facefollow']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # 结束摄像头视频流命令
				#call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头人脸检测时使用opencv占用摄像头
				# try:
				# 	call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头颜色检测时使用opencv占用摄像头
				# except Exception as e:
				# 	print(e.message)
				time.sleep(2)

			elif buffer[1] == 0x09:	 # 摄像头颜色检测跟随模式
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['colorfollow']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['colorfollow']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # 结束摄像头视频流命令
				#call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头颜色检测时使用opencv占用摄像头
				time.sleep(2)

			elif buffer[1] == 0x0A:	 # 摄像头二维码检测识别
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED

				cfg.CRUISING_FLAG = cfg.CRUISING_SET['qrcode_detection']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['qrcode_detection']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # 结束摄像头视频流命令
				#call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头颜色检测时使用opencv占用摄像头
				time.sleep(2)
			elif buffer[1] == 0x0B:  # light
				car_light.init_led()  # 车灯秀

			elif buffer[1] == 0x00:		# 正常模式
				cfg.PROGRAM_ABLE = True
				cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # 将保存的速度复位
				cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
				cfg.AVOIDDROP_CHANGER = 1
				cfg.AVOID_CHANGER = 1
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']
				print("CRUISING_FLAG正常模式 %d " % cfg.CRUISING_FLAG)

		elif buffer == [0x31, 0x00, 0x00]:  # 查询电量信息
			buf = bytes([0xff, 0x31, 0x01, cfg.POWER, 0xff])
			self.sendbuf(buf)

		elif buffer[0] == 0x32:  # 存储角度
			servo.store()

		elif buffer[0] == 0x33:  # 读取角度
			servo.restore()

		elif buffer[0] == 0x40:  # 开关灯模式 FF040000FF开灯  FF040100FF关灯
			if buffer[1] == 0x00:
				car_light.open_light()  # 车灯全部打开，白色
				cfg.LIGHT_OPEN_STATUS = 1
			elif buffer[1] == 0x01:
				car_light.close_light()  # 车灯全部关闭，黑色
				cfg.LIGHT_OPEN_STATUS = 0
			else:
				lednum = buffer[1]  # 获取灯数量指令信息
				ledcolor = buffer[2]  # 获取灯颜色指令信息

				if lednum < 10:  # 多灯模式电亮
					car_light.set_ledgroup(cfg.CAR_LIGHT, lednum - 1, ledcolor)
				elif 9 < lednum < 18:  # 单灯模式电亮
					car_light.set_led(cfg.CAR_LIGHT, lednum - 9, ledcolor)

		elif buffer[0] == 0x41:
			if buffer[1] == 0x00:
				tune = buffer[2]
				cfg.TUNE = tune
			# beep.tone(beep.tone_all)
			elif buffer[1] == 0x01:  # 接收的是低音
				beet1 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet1 + 14], 0.5)
			elif buffer[1] == 0x02:  # 接收的是中音
				beet2 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet2], 0.5)
			elif buffer[1] == 0x03:  # 接收的是高音
				beet3 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet3 + 7], 0.5)

		elif buffer == [0xef, 0xef, 0xee]:
			print("Heartbeat Packet!")

		elif buffer[0] == 0xfc:  # FFFC0000FF  shutdown
			os.system("sudo shutdown -h now")

		else:
			print("error command!")

	def bluetooth_server(self):
		"""
		启动蓝牙接收服务
		参数：第一个参数表示要启动的服务，第二个参数表示要启动的服务名称
		"""
		# print("load bluetooth_server")
		self.load_server(cfg.BT_SERVER, 'bluetooth')

	def tcp_server(self):
		"""
		启动tcp接收服务
		参数：第一个参数表示要启动的服务，第二个参数表示要启动的服务名称
		"""
		# print("load tcp_server")
		self.load_server(cfg.TCP_SERVER, 'tcp')
