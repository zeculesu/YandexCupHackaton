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
@Explain :PS2手柄模块
@Time    :2020/05/09
@File    :xr_ps2.py
@Software: PyCharm
"""
import time
import xr_config as cfg
from xr_i2c import I2c

i2c = I2c()

from xr_motor import RobotDirection

go = RobotDirection()

from xr_servo import Servo
servo = Servo()

class PS2(object):
	def __init__(self):
		pass

	def ps2_button(self):
		"""
		获取PS2手柄的按键值
		:return:cfg.PS2_READ_KEY解析后的按键值
		"""
		ps2check = i2c.readdata(i2c.ps2_address, 0x01)		# 获取PS2返回的模式值
		read_key = i2c.readdata(i2c.ps2_address, 0x03)		# 获取PS2返回的按键值
		read_key1 = i2c.readdata(i2c.ps2_address, 0x04)  	# 获取PS2返回的按键值
		cfg.PS2_READ_KEY = 0
		if ps2check == 0x41 or ps2check == 0xC1 or ps2check == 0x73 or ps2check == 0xF3:		# PS2普通模式
			if read_key == 0xef:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_UP']
			elif read_key == 0xbf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_DOWN']
			elif read_key == 0xcf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_LEFT']
			elif read_key == 0xdf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_RIGHT']
			elif read_key1 == 0xef:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_BLUE']
			elif read_key1 == 0xbf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_GREEN']
			elif read_key1 == 0xcf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_RED']
			elif read_key1 == 0xdf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PINK']
		return cfg.PS2_READ_KEY

	def control(self):
		"""
		PS2手柄控制函数
		:return:
		"""

		read_ps2 = self.ps2_button()           # 获取按键值
		add = 5
		if cfg.PS2_LASTKEY != read_ps2 and cfg.PS2_LASTKEY != 0:		# 如果上一次的值不是0并且不等于这次的值，说明按键值有变化并且不为0
			go.stop()		# 按键值有变化时执行一次有且一次停止
			cfg.LIGHT_STATUS = cfg.STOP		# 将按键状态设置为停止
			cfg.PS2_LASTKEY = 0		# 给上一次状态赋值0，避免再次进入而停止

		else:
			if read_ps2 == cfg.PS2_KEY['PSB_PAD_UP']:  # 等于左侧按键上键
				go.forward()
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2	 # 更新上一次的值

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_DOWN']:  # 等于左侧按键下键
				go.back()
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_LEFT']:  # 等于左侧按键左键
				go.left()
				cfg.LIGHT_STATUS = cfg.TURN_LEFT
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_RIGHT']:  # 等于左侧按键右键
				go.right()
				cfg.LIGHT_STATUS = cfg.TURN_RIGHT
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			if read_ps2 == cfg.PS2_KEY['PSB_RED']:  # 等于红色按键
				# print('PSB_RED')
				if (cfg.ANGLE[6] - add) < 180:
					cfg.ANGLE[6] = cfg.ANGLE[6] + add
				else:
					cfg.ANGLE[6] = 180
				servo.set(7, cfg.ANGLE[6])

			elif read_ps2 == cfg.PS2_KEY['PSB_PINK']:  # 等于粉色按键
				# print('PSB_BLUE')
				if (cfg.ANGLE[6] - add) > 0:
					cfg.ANGLE[6] = cfg.ANGLE[6] - add
				else:
					cfg.ANGLE[6] = 0
				servo.set(7, cfg.ANGLE[6])

			elif read_ps2 == cfg.PS2_KEY['PSB_GREEN']:  # 等于绿色按键
				# print('PSB_GREEN')
				if (cfg.ANGLE[7] - add) < 155:
					cfg.ANGLE[7] = cfg.ANGLE[7] + add
				else:
					cfg.ANGLE[7] = 155
				servo.set(8, cfg.ANGLE[7])

			elif read_ps2 == cfg.PS2_KEY['PSB_BLUE']:  # 等于蓝色按键
				# print('PSB_PINK')
				if (cfg.ANGLE[7] - add) > 0:
					cfg.ANGLE[7] = cfg.ANGLE[7] - add
				else:
					cfg.ANGLE[7] = 0
				servo.set(8, cfg.ANGLE[7])
