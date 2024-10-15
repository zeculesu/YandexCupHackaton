import time
from builtins import object, len
import smbus


class I2c(object):
    def __init__(self):
        self.mcu_address = 0x18
        self.ps2_address = 0x19
        self.device = smbus.SMBus(1)
        pass

    def write_data(self, address, values):
        try:
            self.device.write_i2c_block_data(address, values[0], values[1:len(values)])
            time.sleep(0.005)
        except Exception:
            pass

    def read_data(self, address, index):
        try:
            value = self.device.read_byte_data(address, index)
            time.sleep(0.005)
            return value
        except Exception:
            pass
