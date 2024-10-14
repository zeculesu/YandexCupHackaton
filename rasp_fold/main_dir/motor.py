from time import sleep
import config as cfg
import gpio_cfg as gpio


class MotorController(object):
    def forward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_forward()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def backward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_reverse()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def right_on_place(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_reverse()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def left_on_place(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_forward()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def right_forward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_stop()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def right_backward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_stop()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def left_forward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m3m4_forward()
        self.m1m2_stop()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def left_backward(self, n):
        self.set_both_speed(cfg.DEFAULT_SPEED, cfg.DEFAULT_SPEED)
        self.m3m4_reverse()
        self.m1m2_stop()
        sleep(cfg.STEP_TIME * n)
        self.stop()

    def m1m2_reverse(self):
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, True)

    def m1m2_forward(self):
        gpio.digital_write(gpio.IN1, True)
        gpio.digital_write(gpio.IN2, False)

    def m1m2_stop(self):
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, False)

    def m3m4_stop(self):
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, False)

    def m3m4_forward(self):
        gpio.digital_write(gpio.IN3, True)
        gpio.digital_write(gpio.IN4, False)

    def m3m4_reverse(self):
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, True)

    def set_speed(self, num, speed):
        if num == 1:
            gpio.ena_pwm(speed)
        elif num == 2:
            gpio.enb_pwm(speed)

    def set_both_speed(self, left_speed, right_speed):
        self.set_speed(1, left_speed)
        self.set_speed(2, right_speed)

    def stop(self):
        self.set_speed(1, 0)
        self.set_speed(2, 0)
        self.m1m2_stop()
        self.m3m4_stop()
