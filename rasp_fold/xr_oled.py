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
@Explain :OLED面板显示
@contact :
@Time    :2020/05/09
@File    :xr_oled.py
@Software: PyCharm
"""
import time
import os
import subprocess
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Oled():
	def __init__(self):
		# 获取OLED的实例
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
		# 初始化,清屏
		self.disp.begin()
		self.disp.clear()
		self.disp.display()

		# 创建一幅新的图片，图片大小为oled的尺寸
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))

		# 将图片加载在绘制对象上，相当于加载在画板上
		self.draw = ImageDraw.Draw(self.image)

		# 画一个黑色的填充框，以清除图像
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Draw a black filled box to clear the image.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		self.padding = -2
		self.top = self.padding
		self.bottom = self.height - self.padding
		# Move left to right keeping track of the current x position for drawing shapes.

		# 字体选择
		# 库里默认的字体，在ImageFont里面
		self.font = ImageFont.load_default()
		# 树莓派里的字体库，可以设置字体大小
		self.font1 = ImageFont.truetype('/home/pi/work/python_src/simhei.ttf', 14)
		pass

	def cpu_temp(self):
		'''
		# 获取树莓派温度
		'''
		# 树莓派CPU温度存储在这个文件里，打开文件
		tempFile = open('/sys/class/thermal/thermal_zone0/temp')
		# 读取文件
		cputemp = tempFile.read()
		# 关闭文件
		tempFile.close()
		# 四舍五入保留整数
		tem = round(float(cputemp) / 1000, 1)
		return str(tem)

	def get_network_interface_state(self, interface):
		'''
		获取网口的联网状态，如果是联网状态返回的是up,否则返回down
		'''
		return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]

	def get_ip_address(self, interface):
		'''
		获取网络ip地址
		'''
		if self.get_network_interface_state(interface) == 'down':  # 判断是否联网
			return None
		cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface  # 匹配对应网卡输出的ip信息
		return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

	def get_ip_address_wlan(self, interface):
		'''
		获取网络ip地址
		'''
		if self.get_network_interface_state(interface) == 'down':  # 判断是否联网
			return None
		cmd = "ip a show dev %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | grep -v '169'"  % interface  # 匹配对应网卡输出的ip信息
		return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]




	def draw_row_column(self, row, column, strs):
		'''
		行显示，row代表行号，column代表列号,strs代表要显示的字符串
		'''
		if row == 1:
			self.draw.text((column, self.top), strs, font=self.font, fill=255)
		elif row == 2:
			self.draw.text((column, self.top + 8), strs, font=self.font, fill=255)
		elif row == 3:
			self.draw.text((column, self.top + 16), strs, font=self.font, fill=255)
		elif row == 4:
			self.draw.text((column, self.top + 25), strs, font=self.font, fill=255)

	def disp_default(self):
		'''
		启动后显示的基本信息，第一行显示有线网口ip
		第二行显示无线网口ip
		第三行显示内存使用信息及使用率
		第四行显示SD卡存储信息及使用率
		'''
		# Draw a black filled box to clear the image.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
		cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell=True)
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.1f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell=True)
		cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell=True)

		# Write two lines of text.
		self.draw_row_column(1, 0, "eth0: " + str(self.get_ip_address('eth0')))
		self.draw_row_column(2, 0, "wlan0: " + str(self.get_ip_address('wlan0')))
		self.draw_row_column(3, 0, str(MemUsage.decode('utf-8')))
		self.draw_row_column(4, 0, str(Disk.decode('utf-8')))

		# Display image.

		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.1)

	def disp_cruising_mode(self):
		'''
		进入控制功能后的显示模式
		:return:none
		'''
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		dispmod = cfg.OLED_DISP_MOD[cfg.CRUISING_FLAG]  # 根据选择的模式显示对应的模式
		dispmodlength = len(dispmod) * cfg.OLED_DISP_MOD_SIZE  # 获取字符串长度
		positionmod = (128 - dispmodlength) / 2 - 1  # 字符显示的起始位置

		self.draw.text((0, -2), cfg.LOGO, font=self.font, fill=255)  # 显示LOGO信息
		for line in os.popen("ifconfig wlan0 | awk  '/ether/{print $2 ;exit}' |sed 's/\://g'"):	#获取wlan0的mac地址
			mac = (line[6:12])	# 取mac地址后6位
			mac = 'id:' + mac
		self.draw.text((74, 8), mac, font=self.font, fill=255)  # 显示mac地址后4位信息
		self.draw.text((0, 8), "Dis:" + str(cfg.DISTANCE) + "cm", font=self.font, fill=255)  # 显示距离值
		#self.draw.text((positionmod, 17), dispmod, font=self.font1, fill=255)  # 显示模式

		self.draw.line((0, 8, 128, 8), fill=255)  # 横线

		# draw battery frame
		m = 3  # 电池电量档位数
		n = 3  # 电池每个档位占用的像素单位
		batlength = m * n + 2 + 2 + 2  # m*n表示电芯占用像素，第一个2表示电池框距电芯首尾和值，第二个2表示电池框首尾像素和值，第三个2表示电池头像素值
		x = 128 - batlength - 1  # 电池框左侧起始位置
		y = 0  # 电池框顶部起始位置

		# 画电池框
		self.draw.line((x, y + 2, x + 2, y + 2), fill=255)
		self.draw.line((x + 2, y + 2, x + 2, y), fill=255)
		self.draw.line((x + 2, y, x + batlength, y), fill=255)
		self.draw.line((x + batlength, y, x + batlength, y + 5), fill=255)
		self.draw.line((x + batlength, y + 5, x + 2, y + 5), fill=255)
		self.draw.line((x + 2, y + 5, x + 2, y + 3), fill=255)
		self.draw.line((x + 2, y + 3, x, y + 3), fill=255)
		self.draw.line((x, y + 3, x, y + 2), fill=255)
		# 计算电量级别
		level = cfg.POWER
		# 清空电量
		self.draw.line((x + 3, y + 2, x + batlength - 2, y + 2), fill=0)
		self.draw.line((x + 3, y + 3, x + batlength - 2, y + 3), fill=0)
		# 根据得到的电量档位值重画电量
		self.draw.line((x + batlength - 2 - level * n, y + 2, x + batlength - 2, y + 2), fill=255)
		self.draw.line((x + batlength - 2 - level * n, y + 3, x + batlength - 2, y + 3), fill=255)
		# 将图像信息显示oled上
		ip_address = self.get_ip_address_wlan('wlan0').split("\n")
		#print(ip_address)
		for idx, ip in enumerate(ip_address):
			self.draw_row_column(idx+3,0, "wlan:" + str(ip))
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.05)
