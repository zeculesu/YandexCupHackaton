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
@Explain :电机控制
@contact :
@Time    :2020/05/09
@File    :xr_motor.py
@Software: PyCharm
"""
from builtins import float, object

import os
import xr_gpio as gpio
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class RobotDirection(object):
	def __init__(self):
		pass

	def set_speed(self, num, speed):
		"""
		设置电机速度，num表示左侧还是右侧，等于1表示左侧，等于右侧，speed表示设定的速度值（0-100）
		"""
		# print(speed)
		if num == 1:  # 调节左侧
			gpio.ena_pwm(speed)
		elif num == 2:  # 调节右侧
			gpio.enb_pwm(speed)

	def motor_init(self):
		"""
		获取机器人存储的速度
		"""
		print("获取机器人存储的速度")
		speed = cfgparser.get_data('motor', 'speed')
		cfg.LEFT_SPEED = speed[0]
		cfg.RIGHT_SPEED = speed[1]
		print(speed[0])
		print(speed[1])

	def save_speed(self):
		speed = [0, 0]
		speed[0] = cfg.LEFT_SPEED
		speed[1] = cfg.RIGHT_SPEED
		cfgparser.save_data('motor', 'speed', speed)

	def m1m2_forward(self):
		# 设置电机组M1、M2正转
		gpio.digital_write(gpio.IN1, True)
		gpio.digital_write(gpio.IN2, False)

	def m1m2_reverse(self):
		# 设置电机组M1、M2反转
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, True)

	def m1m2_stop(self):
		# 设置电机组M1、M2停止
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, False)

	def m3m4_forward(self):
		# 设置电机组M3、M4正转
		gpio.digital_write(gpio.IN3, True)
		gpio.digital_write(gpio.IN4, False)

	def m3m4_reverse(self):
		# 设置电机组M3、M4反转
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, True)

	def m3m4_stop(self):
		# 设置电机组M3、M4停止
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, False)

	def forward(self):
		"""
		设置机器人运动方向为前进
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_forward()

	def back(self):
		"""
		#设置机器人运动方向为后退
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_reverse()

	def left(self):
		"""
		#设置机器人运动方向为左转
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_forward()

	def right(self):
		"""
		#设置机器人运动方向为右转
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_reverse()

	def stop(self):
		"""
		#设置机器人运动方向为停止
		"""
		self.set_speed(1, 0)
		self.set_speed(2, 0)
		self.m1m2_stop()
		self.m3m4_stop()
