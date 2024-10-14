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
@Explain :控制舵机
@contact :
@Time    :2020/05/09
@File    :XiaoR_servo.py
@Software: PyCharm
"""
from builtins import hex, eval, int, object
from xr_i2c import I2c
import os

i2c = I2c()
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class Servo(object):
	"""
	舵机控制类
	"""
	def __init__(self):
		pass

	def angle_limit(self, angle):
		"""
		对舵机角度限幅，防止舵机堵转烧毁
		"""
		if angle > cfg.ANGLE_MAX:  # 限制最大角度值
			angle = cfg.ANGLE_MAX
		elif angle < cfg.ANGLE_MIN:  # 限制最小角度值
			angle = cfg.ANGLE_MIN
		return angle

	def set(self, servonum, servoangle):
		"""
		设置舵机角度
		:param servonum:舵机号
		:param servoangle:舵机角度
		:return:
		"""
		angle = self.angle_limit(servoangle)
		buf = [0xff, 0x01, servonum, angle, 0xff]
		try:
			i2c.writedata(i2c.mcu_address, buf)
		except Exception as e:
			print('servo write error:', e)

	def store(self):
		"""
		存储舵机角度
		:return:
		"""
		cfgparser.save_data("servo", "angle", cfg.ANGLE)

	def restore(self):
		"""
		恢复舵机角度
		:return:
		"""
		cfg.ANGLE = cfgparser.get_data("servo", "angle")
		for i in range(0, 8):
			cfg.SERVO_NUM = i + 1
			cfg.SERVO_ANGLE = cfg.ANGLE[i]
			self.set(i + 1, cfg.ANGLE[i])
