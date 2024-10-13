import gpio_cfg as gpio


def get_left_value():
    return gpio.digital_read(gpio.IR_L)


def get_right_value():
    return gpio.digital_read(gpio.IR_R)


def get_middle_value():
    return gpio.digital_read(gpio.IR_M)


def get_line_left_value():
    return gpio.digital_read(gpio.IRF_L)


def get_line_right_value():
    return gpio.digital_read(gpio.IRF_R)
