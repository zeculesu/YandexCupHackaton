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
@Explain :蜂鸣器发声
@contact :
@Time    :2020/05/09
@File    :xr_music.py
@Software: PyCharm
"""
import time
from builtins import range, object, len, int

import xr_gpio as gpio
import xr_config as cfg


class Beep(object):
	def __init__(self):
		# 高音
		self.H1 = 8
		self.H2 = 9
		self.H3 = 10
		self.H4 = 11
		self.H5 = 12
		self.H6 = 13
		self.H7 = 14
		# 低音
		self.L1 = 15
		self.L2 = 16
		self.L3 = 17
		self.L4 = 18
		self.L5 = 19
		self.L6 = 20
		self.L7 = 21
		# 中音
		self.C = 0
		self.D = 1
		self.E = 2
		self.F = 3
		self.G = 4
		self.A = 5
		self.B = 6

		self.tone_all = [
			# '''
			# 二维数组[x][y]，x表示音调，y表示音调中音符的具体频率
			# '''
			# C调
			[1000,  # 0		空音
			 262, 294, 330, 350, 393, 441, 495,    		# 1-7	中音
			 525, 589, 661, 700, 786, 882, 990,    		# H1-H7	高音
			 131, 147, 165, 175, 196, 221, 248     		# L1-L7	低音
			 ],
			# D调
			[1000,  # 0		空音
			 294, 330, 350, 393, 441, 495, 556,    		# 1-7	中音
			 589, 661, 700, 786, 882, 990, 1112,   		# 8-14	高音
			 147, 165, 175, 196, 221, 248, 278     		# 15-21	低音
			 ],
			# E调
			[1000,  # 0		空音
			 330, 350, 393, 441, 495, 556, 624,     	# 1-7	中音
			 661, 700, 786, 882, 990, 1112, 1248,   	# 8-14	高音
			 165, 175, 196, 221, 248, 278, 312      	# 15-21	低音
			 ],
			# F调
			[1000,  # 0		空音
			 350, 393, 441, 495, 556, 624, 661,     	# 1-7	中音
			 700, 786, 882, 935, 1049, 1178, 1322,  	# 8-14	高音
			 175, 196, 221, 234, 262, 294, 330   		# 15-21	低音
			 ],
			# G调
			[1000,  # 0		空音
			 393, 441, 495, 556, 624, 661, 742,  		# 1-7	中音
			 786, 882, 990, 1049, 1178, 1322, 1484, 	# 8-14	高音
			 196, 221, 234, 262, 294, 330, 371  		# 15-21	低音
			 ],
			# A调
			[1000,  # 0		空音
			 441, 495, 556, 589, 661, 742, 833,  		# 1-7	中音
			 882, 990, 1112, 1178, 1322, 1484, 1665,	# 8-14	高音
			 221, 248, 278, 294, 330, 371, 416 	   		# 15-21	低音
			 ],
			# B调
			[1000,  # 0		空音
			 495, 556, 624, 661, 742, 833, 935,  		# 1-7	中音
			 990, 1112, 1178, 1322, 1484, 1665, 1869,   # 8-14	高音
			 248, 278, 294, 330, 371, 416, 467 		    # 15-21	低音
			 ]
		]
		# 生日快乐歌 音符
		self.melody_Happy_birthday = [5, 5,
									  6, 5, self.H1, 7, 5, 5, 6, 5, self.H2, self.H1, 5, 5, self.H5, self.H3, self.H1,
									  7, 6,
									  0, 0, self.H4, self.H4, self.H3, self.H1, self.H2, self.H1]
		# 生日快乐歌 节拍
		self.beet_Happy_birthday = [0.5, 0.5,
									1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 1, 2,
									0.5, 0.5, 0.5, 0.5, 1, 1, 1, 2]

		pass

	def tone(self, tune, beet):
		'''
		播放音符及对应节拍
		:param pin:引脚
		:param tune: 曲调
		:param beet:节拍
		:return:
		'''
		tim = 500000 / tune
		duration_count = beet * 60 * tune / cfg.BEET_SPEED / cfg.CLAPPER
		for i in range(int(duration_count)):
			if tune != 1000:
				gpio.digital_write(gpio.BUZZER, False)
				time.sleep(tim / 500000)
				gpio.digital_write(gpio.BUZZER, True)
				time.sleep(tim / 500000)
			else:
				time.sleep(0.001)

	def play_music(self, major, melody, beet):
		'''
		:param melody:曲谱
		:param beet:节拍
		:return:
		'''
		length = len(melody)
		for i in range(length):
			tone_act = self.tone_all[major][melody[i]]
			self.tone(tone_act, beet[i])
