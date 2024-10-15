import time
from typing import List

import config as cfg
import i2c

i2c = i2c.I2c()


class RGBPanel:
    def __init__(self):
        self.set_all([cfg.WHITE] * 8)
        time.sleep(1)
        self.turn_off()
        self.show_vol()

    def set_led(self, group: int, num: int, color: int) -> None:
        # group - rgb panel or rgb power
        if 0 < num < 9 and 0 < group < 3 and color < 9:
            sendbuf = [cfg.HEADER, group + 3, num, color, cfg.HEADER]
            i2c.write_data(i2c.mcu_address, sendbuf)
            time.sleep(0.005)

    def set_ledgroup(self, group, count, color):
        if 0 < count < 9 and 0 < group < 3 and color < 9:
            sendbuf = [0xff, group + 1, count, color, 0xff]
            i2c.write_data(i2c.mcu_address, sendbuf)
            time.sleep(0.005)

    def set_all(self, colors: List[int]) -> None:
        for i, color in enumerate(colors):
            self.set_led(cfg.RGB_PANEL, i + 1, color)

    def turn_off(self) -> None:
        self.set_all([cfg.BLACK] * 8)

    def show_vol(self):
        vol = self.got_vol()
        if (370 < vol < 430) or (760 < vol < 860) or (1120 < vol < 1290):  # 70-100%  8 led green
            self.set_ledgroup(cfg.RGB_POWER, 8, cfg.GREEN)
            # cfg.POWER = 3
        elif (350 < vol < 370) or (720 < vol < 770) or (1080 < vol < 1120):  # 30-70% 6 led orange
            self.set_ledgroup(cfg.RGB_POWER, 6, cfg.YELLOW)
            # cfg.POWER = 2
        elif (340 < vol < 350) or (680 < vol < 730) or (1040 < vol < 1080):  # 10-30% 2 led green
            self.set_ledgroup(cfg.RGB_POWER, 2, cfg.RED)
            # cfg.POWER = 1
        elif (vol < 340) or (vol < 680) or (vol < 1040):  # <10% 1 led green
            self.set_ledgroup(cfg.RGB_POWER, 1, cfg.RED)
            # cfg.POWER = 0

    def got_vol(self):
        time.sleep(0.005)
        vol_h = i2c.read_data(i2c.mcu_address, 0x05)
        if vol_h is None:
            vol_h = 0
        time.sleep(0.005)
        vol_l = i2c.read_data(i2c.mcu_address, 0x06)
        if vol_l is None:
            vol_l = 0
        vol = (vol_h << 8) + vol_l
        return vol
