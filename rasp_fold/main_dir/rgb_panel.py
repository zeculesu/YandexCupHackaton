from typing import List

import i2c
import time
import config as cfg

i2c = i2c.I2c()


class RGBPanel:
    def __init__(self):
        self.set_all([cfg.WHITE] * 8)
        time.sleep(1)
        self.turn_off()

    def set_led(self, group: int, num: int, color: int) -> None:
        if 0 < num < 9 and 0 < group < 3 and color < 9:
            sendbuf = [cfg.HEADER, group + 3, num, color, cfg.HEADER]
            i2c.write_data(i2c.mcu_address, sendbuf)
            time.sleep(0.005)

    def set_all(self, colors: List[int]) -> None:
        for i, color in enumerate(colors):
            self.set_led(cfg.RGB_PANEL, i + 1, color)

    def turn_off(self):
        self.set_all([cfg.BLACK] * 8)
