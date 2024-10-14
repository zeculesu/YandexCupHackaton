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
@Explain :车灯相关功能
@contact :
@Time    :2020/05/09
@File    :xr_car_light.py
@Software: PyCharm
"""

from builtins import int, range
import xr_config as cfg

import time
from xr_i2c import I2c

i2c = I2c()


class Car_light(object):
	def __init__(self):
		pass

	def set_led(self, group, num, color):
		"""
		设置RGB灯的状态
		:param group:灯组，等于1为电量灯，2为车灯
		:param num:灯的索引
		:param color:设置颜色，在config中COLOR可选对应颜色，只能设置已定义好的颜色
		:return:
		"""
		if 0 < num < 9 and 0 < group < 3 and color < 9:
			sendbuf = [0xff, group + 3, num, color, 0xff]
			i2c.writedata(i2c.mcu_address, sendbuf)
			time.sleep(0.005)
		# print("set_led group%d, LED%d, color%d  :OK \r\n", group, num, color)

	def set_ledgroup(self, group, count, color):
		"""
		设置RGB灯数量的状态
		:param group:灯组，等于1为电量灯，2为车灯
		:param count:灯的数量
		:param color:设置颜色，在config中COLOR可选对应颜色，只能设置已定义好的颜色
		:return:
		"""
		if 0 < count < 9 and 0 < group < 3 and color < 9:
			sendbuf = [0xff, group + 1, count, color, 0xff]
			i2c.writedata(i2c.mcu_address, sendbuf)
			time.sleep(0.005)
		# print("set_led group%d, LED%d, color%d  :OK \r\n", group, count, color)

	def open_light(self):
		"""
		全车灯打开
		:return:
		"""
		# print("车灯全部打开")
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
		time.sleep(0.01)

	def close_light(self):
		"""
		全车灯关闭
		:return:
		"""
		# print("车灯全部关闭")
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.01)

	def left_turn_light(self):
		"""
		左转流水灯
		:return:
		"""
		# print("左转")
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 7, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 8, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.12)

	def right_turn_light(self):
		"""
		右转流水灯
		:return:
		"""
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 2, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 1, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.12)

	def forward_turn_light(self):
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['green'])
		time.sleep(0.12)

	def back_turn_light(self):
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
		time.sleep(0.12)

	def init_led(self):
		"""
		启动状态车灯
		:return:
		"""
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		for j in range(8):
			for i in range(8):
				self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
				time.sleep(0.05)
				self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
				time.sleep(0.05)

			for i in range(4):
				self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
				self.set_led(cfg.CAR_LIGHT, 8 - i, j + 1)
				time.sleep(0.05)

			for i in range(4):
				self.set_led(cfg.CAR_LIGHT, i + 1, cfg.COLOR['black'])
				self.set_led(cfg.CAR_LIGHT, 8 - i, cfg.COLOR['black'])
				time.sleep(0.05)