import RPi.GPIO as GPIO

# 设置引脚模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 蜂鸣器引脚
BUZZER = 10

# 设置电机引脚
ENA = 13  # //L298使能A
ENB = 20  # //L298使能B
IN1 = 16  # //电机接口1
IN2 = 19  # //电机接口2
IN3 = 26  # //电机接口3
IN4 = 21  # //电机接口4

# 设置超声波引脚
ECHO = 4  # 超声波接收脚位
TRIG = 17  # 超声波发射脚位

# 设置红外引脚
IR_R = 18  # 小车右侧巡线红外
IR_L = 27  # 小车左侧巡线红外
IR_M = 22  # 小车中间避障红外
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
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)  # 超声波模块发射端管脚设置trig
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 超声波模块接收端管脚设置echo
# 蜂鸣器脚初始化使能
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)  # 蜂鸣器设置为低电平


def digital_write(gpio, status):
    GPIO.output(gpio, status)


def digital_read(gpio):
    return GPIO.input(gpio)


def ena_pwm(pwm):
    ENA_pwm.ChangeDutyCycle(pwm)


def enb_pwm(pwm):
    ENB_pwm.ChangeDutyCycle(pwm)
