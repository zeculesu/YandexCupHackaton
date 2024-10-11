import time
import os
import subprocess
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# 获取OLED的实�?
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)

# 初始�?清屏
disp.begin()
disp.clear()
disp.display()

# 创建一幅新的图片，图片大小为oled的尺�?
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# 将图片加载在绘制对象上，相当于加载在画板�?
draw = ImageDraw.Draw(image)

# 画一个黑色的填充框，以清除图�?
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# 字体选择
# 库里默认的字体，在ImageFont里面
default_font = ImageFont.load_default()
# 树莓派里的字体库，可以设置字体大�?
font = ImageFont.truetype('/home/pi/work/python_src/simhei.ttf', 15)


# 获取树莓派温�?
def cpu_temp():
    # 树莓派CPU温度存储在这个文件里，打开文件
    tempFile = open('/sys/class/thermal/thermal_zone0/temp')
    # 读取文件
    cputemp = tempFile.read()
    # 关闭文件
    tempFile.close()
    # 四舍五入保留整数
    tem = round(float(cputemp) / 1000, 1)
    return str(tem)

while True:
    temp = cpu_temp()
    # 画一个黑色的填充框，以清除图�?
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # 绘制文字，text()两个参数是屏幕X、Y轴的距离，屏幕左上角为XY轴的0�?
    draw.text((5, 0), "当前温度: " + temp, font=font, fill=255)
    draw.text((50, 16), "by_小R科技", font=font, fill=255)
      
    # 在oled显示
    disp.image(image)
    time.sleep(1)
    disp.display() 