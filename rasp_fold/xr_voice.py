# # coding:utf-8
# """
# 树莓派WiFi无线视频小车机器人驱动源码
# 作者：Sence
# 版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
# 本代码可以自由修改，但禁止用作商业盈利目的！
# 本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
# """
# """
# @version: python3.7
# @Author  : xiaor
# @Explain :语音模块
# @Time    :2020/05/09
# @File    :xr_voice.py
# @Software: PyCharm
# """
import serial
import time
import xr_config as cfg


class Voice(object):
	def __init__(self):
		self.ser = serial.Serial("/dev/ttyS0", 9600)
		pass

	def run(self):
		while True:
			while self.ser.inWaiting() > 0:
				time.sleep(0.05)
				n = self.ser.inWaiting()
				myout = self.ser.read(n)
				self.get_voice(myout)
				dat = int.from_bytes(myout, byteorder='big')
				print('%#x' % dat)

			time.sleep(0.5)

	def get_voice(self, data):
		cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
		if len(data) < cfg.RECV_LEN:  # 不符合接收长度标准
			# print('data len %d:'%len(data))
			return cfg.VOICE_MOD
		if data[0] == 0xff and data[len(data) - 1] == 0xff:  # 如果包头和包尾是0xff则符合小二科技通信协议
			buf = []  # 定义一个列表
			for i in range(1, 4):  # 获取协议包中间3位的数据
				buf.append(data[i])  # 往buf中添加数据
			if buf[0] == 0xf5 and buf[1] == 0x01:
				if buf[2] == 0x01:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
				elif buf[2] == 0x02:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['openlight']
				elif buf[2] == 0x03:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['closelight']
				elif buf[2] == 0x06:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['forward']
				elif buf[2] == 0x07:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['back']
				elif buf[2] == 0x08:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['left']
				elif buf[2] == 0x09:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['right']
				elif buf[2] == 0x0A:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['stop']
				elif buf[2] == 0x0B:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['nodhead']
				elif buf[2] == 0x0C:
					cfg.VOICE_MOD = cfg.VOICE_MOD_SET['shakehead']
		return cfg.VOICE_MOD

if __name__ == "__main__":
	ser = Voice()
	while True:
		print("run voice ctl")
		ser.run()