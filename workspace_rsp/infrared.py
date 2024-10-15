import gpio_cfg as gpio


# 1 означает препятствие, 0 если свободно

def get_left_value() -> bool:
    return not gpio.digital_read(gpio.IR_L)


def get_right_value() -> bool:
    return not gpio.digital_read(gpio.IR_R)


def get_middle_value() -> bool:
    return not gpio.digital_read(gpio.IR_M)


def get_left_line_value() -> bool:
    return not gpio.digital_read(gpio.IRF_L)


def get_right_line_value() -> bool:
    return not gpio.digital_read(gpio.IRF_R)
