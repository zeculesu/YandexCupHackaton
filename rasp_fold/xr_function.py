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
@Explain :摄像头识别及小车运动功能
@contact :
@Time    :2020/05/09
@File    :xr_function.py
@Software: PyCharm
"""

from builtins import float, object, bytes

import time
import xr_config as cfg

from xr_socket import Socket
socket = Socket()

from xr_motor import RobotDirection
go = RobotDirection()

from xr_car_light import Car_light

car_light = Car_light()


class Function(object):
	def __init__(self):
		pass

	def linepatrol_control(self):
		"""
		摄像头巡线小车运动
		:return:
		"""
		while cfg.CAMERA_MOD == 1:
			dx = cfg.LINE_POINT_TWO - cfg.LINE_POINT_ONE			# 上与下取样点中心坐标差值
			mid = int(cfg.LINE_POINT_ONE + cfg.LINE_POINT_TWO) / 2	# 上与下取样点中心坐标均值

			print("dx==%d" % dx)			# 打印上与下取样点中心坐标差值
			print("mid==%s" % mid)			# 打印上与下取样点中心坐标均值

			if 0 < mid < 260:				# 如果巡线中心点偏左，说明车子右偏离轨道,就需要左转来校正。
				print("turn left")
				go.left()
			elif mid > 420:					# 如果巡线中心点偏右，说明车子左偏离轨道，就需要右转来校正。
				print("turn right")
				go.right()
			else:							# 如果巡线中心点居中情况
				if dx > 45:
					print("turn left")		# 线有右倾斜的趋势
					go.left()
				elif dx < -45:
					print("turn right")		# 线有左倾斜的趋势
					go.right()
				else:
					print("go stright")		# 线在中心位置，并且线处于竖直状态
					go.forward()
			time.sleep(0.007)
			go.stop()
			time.sleep(0.007)

	def qrcode_control(self):
		"""
		二维码检测识别控制小车运动
		:return:
		"""
		cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
		cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
		cfg.LEFT_SPEED = 30		# 设置合适的速度
		cfg.RIGHT_SPEED = 30
		code_status = 0
		while cfg.CAMERA_MOD == 4:
			time.sleep(0.05)
			if cfg.BARCODE_DATE == 'start':		# 检测到起始信号，start的二维码
				#print(cfg.BARCODE_DATE)
				buf = boobs([0xff, 0x13, 0x0a, 0x00, 0xff])
				socket.sendbuf(buf)
				#cfg.LIGHT_STATUS = cfg.TURN_FORWARD
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
				time.sleep(1.5)
				code_status = 1						# code_status
			elif cfg.BARCODE_DATE == 'stop':	# 检测到结束信号，stop的二维码
				#print(cfg.BARCODE_DATE)
				buf = boobs([0xff, 0x13, 0x0a, 0x01, 0xff])
				socket.sendbuf(buf)
				#cfg.LIGHT_STATUS = cfg.STOP
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
				time.sleep(1.5)
				code_status = 0						# code_status

			if code_status:
				if cfg.BARCODE_DATE == 'forward':	# 检测到forward的二维码，小车前进
					#print("forward")
					buf = boobs([0xff, 0x13, 0x0a, 0x02, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_FORWARD
					go.forward()
					time.sleep(2.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'back':	# 检测到back的二维码，小车后退
					#print("back")
					buf = boobs([0xff, 0x13, 0x0a, 0x03, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_BACK
					go.back()
					time.sleep(2.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'left':	# 检测到left的二维码，小车左转
					#print("left")
					buf = boobs([0xff, 0x13, 0x0a, 0x04, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_LEFT
					go.left()
					time.sleep(1.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'right':	# 检测到right的二维码，小车右转
					#print("right")
					buf = boobs([0xff, 0x13, 0x0a, 0x05, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_RIGHT
					go.right()
					time.sleep(1.5)
					go.stop()
					time.sleep(0.5)
				else:
					#print("go.forward")
					cfg.LIGHT_STATUS = cfg.STOP
					#go.forward()
			else:
				go.stop()
				time.sleep(0.05)
		go.stop()
