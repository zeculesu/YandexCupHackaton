import time

from rgb_panel import RGBPanel

rgb_panel = RGBPanel()
rgb_panel.set_all([1, 2, 3, 4, 5, 6, 7, 8])
time.sleep(3)
# for i in range(1, 9):
#     rgb_panel.set_led(2, i, 6)
#     time.sleep(1)
#     rgb_panel.turn_off()