# coding:utf-8
"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :摄像头识别相关功能
@contact :
@Time    :2020/05/09
@File    :xr_camera.py
@Software: PyCharm
"""

from builtins import range, len, int
import os
from subprocess import call
import time
import math
import pyzbar.pyzbar as pyzbar
import xr_config as cfg

from xr_motor import RobotDirection

go = RobotDirection()
import cv2

from xr_servo import Servo

servo = Servo()

from xr_pid import PID


class Camera(object):
    def __init__(self):
        self.fre_count = 1  # 采样数量
        self.px_sum = 0  # 采样点x坐标累计值
        self.cap_open = 0  # 摄像头是否打开标志
        self.cap = None

        self.servo_X = 7
        self.servo_Y = 8

        self.angle_X = 90
        self.angle_Y = 20


        self.X_pid = PID(0.03, 0.09, 0.0005)  # 实例化一个X轴坐标的PID算法PID参数：第一个代表pid的P值，二代表I值,三代表D值
        self.X_pid.setSampleTime(0.005)  # 设置PID算法的周期
        self.X_pid.setPoint(240)  # 设置PID算法的预值点，即目标值，这里160指的是屏幕框的x轴中心点，x轴的像素是320，一半是160

        self.Y_pid = PID(0.035, 0.08, 0.002)  # 实例化一个X轴坐标的PID算法PID参数：第一个代表pid的P值，二代表I值,三代表D值
        self.Y_pid.setSampleTime(0.005)  # 设置PID算法的周期
        self.Y_pid.setPoint(160)  # 设置PID算法的预值点，即目标值，这里160指的是屏幕框的y轴中心点，y轴的像素是320，一半是160

    def linepatrol_processing(self):
        """
        摄像头巡线数据采集
        :return:
        """
        while True:
            if self.cap_open == 0:  # 摄像头没有打开
                try:
                    # self.cap = cv2.VideoCapture(0) # 打开摄像头
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                except Exception as e:
                    print('opencv camera open error:', e)
                self.cap_open = 1  # 标志置1
            else:
                try:
                    ret, frame = self.cap.read()  # 获取摄像头帧数据
                    if ret:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将RGB转换成GRAY颜色空间
                        if cfg.PATH_DECT_FLAG == 0:
                            ret, thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)  # 巡黑色线
                        else:
                            ret, thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)  # 巡白色线
                        for j in range(0, 640, 5):  # X轴方向横向采样，采样点间隔5个像素
                            if thresh1[350, j] == 0:  # 取图像y轴中间偏上值350，对采样点进行二值化判断
                                self.px_sum = self.px_sum + j  # 将符合线颜色的采样点x坐标累计相加
                                self.fre_count = self.fre_count + 1  # 将采样数量累计
                        cfg.LINE_POINT_ONE = self.px_sum / self.fre_count  # 用x坐标累计值/采样数量=符合线颜色坐标点平均值，相当于线x坐标实际位置点
                        self.px_sum = 0  # 清除累计值
                        self.fre_count = 1  # 清除采样数量最低为1
                        for j in range(0, 640, 5):  # X轴方向横向采样，采样点间隔5个像素
                            if thresh1[200, j] == 0:  # 取图像y轴中间偏下值200，对采样点进行二值化判断
                                self.px_sum = self.px_sum + j  # 将符合线颜色的采样点x坐标累计相加
                                self.fre_count = self.fre_count + 1  # 将采样数量累计
                        cfg.LINE_POINT_TWO = self.px_sum / self.fre_count  # 用x坐标累计值/采样数量=符合线颜色坐标点平均值，相当于线x坐标实际位置点
                        self.px_sum = 0  # 清除累计值
                        self.fre_count = 1  # 清除采样数量最低为1
                        print("point1 = %d ,point2 = %d"%(cfg.LINE_POINT_ONE,cfg.LINE_POINT_TWO))
                except Exception as e:  # 捕获并打印出错信息
                    go.stop()  # 退出,停止小车
                    self.cap_open = 0  # 关闭标志
                    self.cap.release()  # 释放摄像头
                    print('linepatrol_processing error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # 如果退出巡线模式
                go.stop()  # 退出巡线,停止小车
                self.cap_open = 0  # 关闭标志
                self.cap.release()  # 释放摄像头
                break  # 退出循环

    def facefollow(self):
        """
        人脸检测及摄像头跟随
        :return:
        """
        time.sleep(3)
        while True:

            if self.cap_open == 0:  # 摄像头没有打开
                try:
                    # self.cap = cv2.VideoCapture(0)	# 打开摄像头
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                    self.cap_open = 1  # 标志置1
                    self.cap.set(3, 320)  # 设置图像的宽为320像素
                    self.cap.set(4, 320)  # 设置图像的高为320像素
                    face_cascade = cv2.CascadeClassifier(
                        '/home/pi/work/python_src/face.xml')  # 人脸识别OpenCV级联检测器，也可以换成其他特征识别器，比如鼻子的
                except Exception as e:
                    print('opencv camera open error:', e)
                    break

            else:
                try:
                    ret, frame = self.cap.read()  # 获取摄像头视频流
                    if ret == 1:  # 判断摄像头是否工作
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 要先将每一帧先转换成灰度图，在灰度图中进行查找
                        faces = face_cascade.detectMultiScale(gray)  # 查找人脸
                        if len(faces) > 0:  # 当视频中有人脸轮廓时
                            print('face found!')
                            for (x, y, w, h) in faces:
                                # 参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
                                cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
                                result = (x, y, w, h)
                                x_middle = result[0] + w / 2  # x轴中心
                                y_middle = result[1] + h / 2  # y轴中心

                                self.X_pid.update(x_middle)  # 将X轴数据放入pid中计算输出值
                                self.Y_pid.update(y_middle)  # 将Y轴数据放入pid中计算输出值
                                # print("X_pid.output==%d"%self.X_pid.output)     #打印X输出
                                # print("Y_pid.output==%d"%self.Y_pid.output)     #打印Y输出
                                self.angle_X = math.ceil(self.angle_X + 1 * self.X_pid.output)  # 更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                                self.angle_Y = math.ceil(
                                    self.angle_Y + 0.8 * self.Y_pid.output)  # 更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                                
                                # if self.angle_X > 180:  # 限制X轴最大角度
                                #     self.angle_X = 180
                                # if self.angle_X < 0:  # 限制X轴最小角度
                                #     self.angle_X = 0
                                # if self.angle_Y > 180:  # 限制Y轴最大角度
                                #     self.angle_Y = 180
                                # if self.angle_Y < 0:  # 限制Y轴最小角度
                                #     self.angle_Y = 0
                                self.angle_X = min(180, max(0, self.angle_X))
                                self.angle_Y = min(180, max(0, self.angle_Y))
                                print("angle_X: %d" % self.angle_X)  #打印X轴舵机角度
                                print("angle_Y: %d" % self.angle_Y)  # 打印Y轴舵机角度
                                servo.set(self.servo_X, self.angle_X)  # 设置X轴舵机
                                servo.set(self.servo_Y, self.angle_Y)  # 设置Y轴舵机
                    # cv2.imshow("capture", frame)  # 显示图像
                except Exception as e:  # 捕获并打印出错信息
                    go.stop()  # 退出,停止小车
                    self.cap_open = 0  # 关闭标志
                    self.cap.release()  # 释放摄像头
                    print('facefollow error:', e)
            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # 如果退出人脸识别模式
                go.stop()  # 退出,停止小车
                self.cap_open = 0  # 关闭标志
                self.cap.release()  # 释放摄像头
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'  # 结束摄像头视频流命令
                # # call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头人脸检测时使用opencv占用摄像头
                # try:
                #     call("%s" % path_sh, shell=True)  # 启动shell命令结束摄像头视频流，一会摄像头颜色检测时使用opencv占用摄像头
                # except Exception as e:
                #     print(e.message)
                time.sleep(2)
                break  # 退出循环

    def colorfollow(self):
        """
        颜色检测摄像头跟随
        :return:
        """
        while True:
            if self.cap_open == 0:  # 摄像头没有打开
                # self.cap = cv2.VideoCapture(0)		# 打开摄像头
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # 标志置1
                self.cap.set(3, 320)  # 设置图像的宽为320像素
                self.cap.set(4, 320)  # 设置图像的高为320像素
            else:
                try:
                    ret, frame = self.cap.read()  # 获取摄像头视频流
                    if ret == 1:  # 判断摄像头是否工作
                        frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯滤波GaussianBlur() 让图片模糊
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 将图片的色域转换为HSV的样式 以便检测
                        mask = cv2.inRange(hsv, cfg.COLOR_LOWER[cfg.COLOR_INDEX],
                                           cfg.COLOR_UPPER[cfg.COLOR_INDEX])  # 设置阈值，去除背景 保留所设置的颜色

                        mask = cv2.erode(mask, None, iterations=2)  # 显示腐蚀后的图像
                        mask = cv2.GaussianBlur(mask, (3, 3), 0)  # 高斯模糊
                        res = cv2.bitwise_and(frame, frame, mask=mask)  # 图像合并

                        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 边缘检测

                        if len(cnts) > 0:  # 通过边缘检测来确定所识别物体的位置信息得到相对坐标
                            cnt = max(cnts, key=cv2.contourArea)
                            (x, y), radius = cv2.minEnclosingCircle(cnt)
                            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)  # 画出一个圆
                            # print(int(x), int(y))

                            self.X_pid.update(x)  # 将X轴数据放入pid中计算输出值
                            self.Y_pid.update(y)  # 将Y轴数据放入pid中计算输出值
                            # print("X_pid.output==%d"%X_pid.output)		#打印X输出
                            # print("Y_pid.output==%d"%Y_pid.output)		#打印Y输出
                            self.angle_X = math.ceil(
                                self.angle_X + 1 * self.X_pid.output)  # 更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                            self.angle_Y = math.ceil(
                                self.angle_Y + 0.8 * self.Y_pid.output)  # 更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                            # print("angle_X-----%d" % self.angle_X)	#打印X轴舵机角度
                            # print("angle_Y-----%d" % self.angle_Y)	#打印Y轴舵机角度
                            if self.angle_X > 180:  # 限制X轴最大角度
                                self.angle_X = 180
                            if self.angle_X < 0:  # 限制X轴最小角度
                                self.angle_X = 0
                            if self.angle_Y > 180:  # 限制Y轴最大角度
                                self.angle_Y = 180
                            if self.angle_Y < 0:  # 限制Y轴最小角度
                                self.angle_Y = 0
                            servo.set(self.servo_X, self.angle_X)  # 设置X轴舵机
                            servo.set(self.servo_Y, self.angle_Y)  # 设置Y轴舵机
                except Exception as e:  # 捕获并打印出错信息
                    go.stop()  # 退出,停止小车
                    self.cap_open = 0  # 关闭标志
                    self.cap.release()  # 释放摄像头
                    print('colorfollow error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # 如果退出摄像头颜色检测跟随模式
                go.stop()  # 退出,停止小车
                self.cap_open = 0  # 关闭标志
                self.cap.release()  # 释放摄像头
                break  # 退出循环

    def decodeDisplay(self, image):
        """
        二维码识别
        :param image:摄像头数据帧
        :return:image 识别后的图像数据帧
        """
        barcodes = pyzbar.decode(image)
        if barcodes == []:
            cfg.BARCODE_DATE = None
            cfg.BARCODE_TYPE = None
        else:
            for barcode in barcodes:
                # 提取条形码的边界框的位置
                # 画出图像中条形码的边界框
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 条形码数据为字节对象，所以如果我们想在输出图像上
                # 画出来，就需要先将它转换成字符串
                cfg.BARCODE_DATE = barcode.data.decode("utf-8")
                cfg.BARCODE_TYPE = barcode.type

                # 绘出图像上条形码的数据和条形码类型
                text = "{} ({})".format(cfg.BARCODE_DATE, cfg.BARCODE_TYPE)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            .5, (0, 0, 125), 2)

            # 向终端打印条形码数据和条形码类型
        # print("[INFO] Found {} barcode: {}".format(cfg.BARCODE_TYPE, cfg.BARCODE_DATE))
        return image

    def qrcode_detection(self):
        """
        摄像头二维码识别运动
        :return:
        """
        while True:
            if self.cap_open == 0:  # 摄像头没有打开
                # self.cap = cv2.VideoCapture(0)	# 打开摄像头
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # 标志置1
            else:
                try:
                    ret, frame = self.cap.read()  # 获取摄像头视频流
                    if ret == 1:  # 判断摄像头是否工作
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转为灰度图像
                        img = self.decodeDisplay(gray)  # 识别二维码
                # cv2.imshow("qrcode", img)	# 显示在窗口
                except Exception as e:  # 捕获并打印出错信息
                    go.stop()  # 退出,停止小车
                    self.cap_open = 0  # 关闭标志
                    self.cap.release()  # 释放摄像头
                    print('qrcode_detection error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # 如果退出摄像头二维码检测模式
                go.stop()  # 退出,停止小车
                self.cap_open = 0  # 关闭标志
                self.cap.release()  # 释放摄像头
                break  # 退出循环

    def run(self):
        """
        摄像头模式切换
        :return:
        """
        while True:
            if cfg.CAMERA_MOD == 1:  # 摄像头巡线模式
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # 将当前速度保存
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.LEFT_SPEED = 45  # 摄像头巡线时速度调低
                cfg.RIGHT_SPEED = 45
                self.linepatrol_processing()
            elif cfg.CAMERA_MOD == 2:  # 摄像头人脸检测跟随
                self.facefollow()
            elif cfg.CAMERA_MOD == 3:  # 摄像头颜色检测跟随
                self.colorfollow()
            elif cfg.CAMERA_MOD == 4:  # 摄像头二维码检测
                self.qrcode_detection()
            else:
                pass
            time.sleep(0.05)
