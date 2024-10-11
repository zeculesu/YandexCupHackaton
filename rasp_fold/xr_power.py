"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
import time

"""
@version: python3.7
@Author  : xiaor
@Explain :小车电量相关
@Time    :2020/05/09
@File    :xr_power.py
@Software: PyCharm
"""

from builtins import hex, bytes

from xr_i2c import I2c

i2c = I2c()

from xr_car_light import Car_light
rgb = Car_light()

import xr_config as cfg


class Power():
	def __init__(self):
		pass

	def got_vol(self):
		"""
		获取电池电压信息
		:return:
		"""
		time.sleep(0.005)
		vol_H = i2c.readdata(i2c.mcu_address, 0x05)  	# 读取MCU测得反馈的电池电压值高8位
		if vol_H == None:
			vol_H = 0
		time.sleep(0.005)
		vol_L = i2c.readdata(i2c.mcu_address, 0x06)  	# 读取MCU测得反馈的电池电压值低8位
		if vol_L == None:
			vol_L = 0
		vol = (vol_H << 8) + vol_L  # 高8位和低八位结合, 电池电压放大了100倍
		return vol  # 返回电池电压

	# def show_vol(self, socket):
	def show_vol(self):
		"""
		RGB灯电量显示
		:return:
		"""
		vol = self.got_vol()
		if (370 < vol < 430) or (760 < vol < 860) or (1120 < vol < 1290):  # 70-100%  8 led green
			rgb.set_ledgroup(cfg.POWER_LIGHT, 8, cfg.COLOR['green'])		# 设置电量灯条为绿色
			cfg.POWER = 3		# 电量档位值设置为最高档3
		elif (350 < vol < 370) or (720 < vol < 770) or (1080 < vol < 1120):  	# 30-70% 6 led orange
			rgb.set_ledgroup(cfg.POWER_LIGHT, 6, cfg.COLOR['orange'])
			cfg.POWER = 2		# 电量档位值设置为2
		elif (340 < vol < 350) or (680 < vol < 730) or (1040 < vol < 1080):  	# 10-30% 2 led green
			rgb.set_ledgroup(cfg.POWER_LIGHT, 2, cfg.COLOR['red'])
			cfg.POWER = 1		# 电量档位值设置为1
		elif (vol < 340) or (vol < 680) or (vol < 1040):  # <10% 1 led green
			rgb.set_ledgroup(cfg.POWER_LIGHT, 1, cfg.COLOR['red'])
			cfg.POWER = 0		# 电量档位值设置为0
