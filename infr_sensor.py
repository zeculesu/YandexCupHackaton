import xr_gpio as gpio

for i in range(3):
    dist = input()
    print(gpio.digital_read(gpio.IR_L))
    print(gpio.digital_read(gpio.IR_M))
    print(gpio.digital_read(gpio.IR_R))
