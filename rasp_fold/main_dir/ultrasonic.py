import time
import gpio_cfg as gpio


def get_distance():
    time_count = 0
    time.sleep(0.01)
    gpio.digital_write(gpio.TRIG, True)
    time.sleep(0.000015)
    gpio.digital_write(gpio.TRIG, False)
    while not gpio.digital_read(gpio.ECHO):
        pass
    t1 = time.time()
    while gpio.digital_read(gpio.ECHO):
        if time_count < 2000:
            time_count = time_count + 1
            time.sleep(0.000001)
            pass
        else:
            break
    t2 = time.time()
    distance = (t2 - t1) * 340 / 2 * 100
    if distance < 500:
        print("distance is %d" % distance)
        return round(distance, 2)
    else:
        print("distance is -1")  # 如果距离值大于5m,超出检测范围
        return -1
