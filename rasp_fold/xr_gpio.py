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
@Explain :树莓派GPIO配置文件
@contact :
@Time    :2020/05/09
@File    :xr_gpio.py
@Software: PyCharm
"""

import RPi.GPIO as GPIO

# 设置引脚模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 蜂鸣器引脚
BUZZER = 10

# 设置电机引脚
ENA = 13  	# //L298使能A
ENB = 20  	# //L298使能B
IN1 = 16  	# //电机接口1
IN2 = 19  	# //电机接口2
IN3 = 26  	# //电机接口3
IN4 = 21  	# //电机接口4

# 设置超声波引脚
ECHO = 4  	# 超声波接收脚位
TRIG = 17  	# 超声波发射脚位

# 设置红外引脚
IR_R = 18  	# 小车右侧巡线红外
IR_L = 27  	# 小车左侧巡线红外
IR_M = 22  	# 小车中间避障红外
IRF_R = 25  # 小车跟随右侧红外
IRF_L = 1  # 小车跟随左侧红外

# 引脚初始化使能
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, 1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(100)
ENB_pwm = GPIO.PWM(ENB, 1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(100)

# 红外引脚初始化使能
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 超声波脚初始化使能
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)  			# 超声波模块发射端管脚设置trig
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# 超声波模块接收端管脚设置echo
# 蜂鸣器脚初始化使能
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)			# 蜂鸣器设置为低电平


def digital_write(gpio, status):
	"""
	设置gpio端口为电平
	参数：gpio为设置的端口，status为状态值只能为True(高电平)，False(低电平)
	"""
	GPIO.output(gpio, status)

def digital_read(gpio):
	"""
	读取gpio端口的电平
	"""
	return GPIO.input(gpio)

def ena_pwm(pwm):
	"""
	设置电机调速端口ena的pwm
	"""
	ENA_pwm.ChangeDutyCycle(pwm)

def enb_pwm(pwm):
	"""
	设置电机调速端口enb的pwm
	"""
	ENB_pwm.ChangeDutyCycle(pwm)
