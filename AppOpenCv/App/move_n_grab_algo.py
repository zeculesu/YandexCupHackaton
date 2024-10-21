import config as cfg
from time import sleep



def push_button(x, y):
    commands = []
    if x <= 235:
        commands.append(cfg.MOTOR_LEFT_ON_PLACE)
    elif x > 245:
        commands.append(cfg.MOTOR_RIGHT_ON_PLACE)
    elif y > 260:
        commands.append(cfg.MOTOR_BACKWARD)
    elif y < 240:
        commands.append(cfg.MOTOR_FORWARD)
    else:
        commands.append(cfg.MANIPULATOR_SET_THROW_POSITION)
        commands.append(cfg.MANIPULATOR_DEFAULT_POSITION)
    return commands
