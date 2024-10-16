from Log_manager import Logs

import VideoCamera as Camera
import result_type as ResType
import numpy as np
import cv2 as cv
import Buttons
import Button
import Field
import Robot
import Rectangle

import logging


class App:
    def __init__(self):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.info("Create Logs")
        
        self.VideoCameraOnRobot = Camera.VideoCamera('../../../Left_1.avi')
        self.VideoCameraOnHigh = Camera.VideoCamera('../../../Right_1.avi')

        button_colors_map = {
            "green": (np.array([50,100,140]), np.array([83,170,240])),  # fix
            "blue": (np.array([90,158,124]), np.array([138,255,255])),
            "red": (np.array([157, 92, 175]), np.array([185, 241, 252])),
            "orange": (np.array([0, 100, 207]), np.array([40, 254, 247])),  # fix
        }
        self.buttons = Buttons.Buttons(button_colors_map)

        self.Field = Field.Field()
        self.enemy_Robot = Robot.Robot()
        self.out_Robot = Robot.Robot()

        self.values_count = 3
        self.special_values_count = 1

    def GetFieldContour(self, contours):
        max_area = -1
        max_ctr = None

        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)

            ctr = np.array(box).reshape((-1, 1, 2)).astype(np.int32)
            area = Rectangle.Rectangle(ctr).area

            if area > max_area:
                max_area = area
                max_ctr = ctr

        return max_ctr

    def GetWhiteAndBlack(self, frame_hsv):
        black = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([200,255,100]))
        sensity = 40  # ну так работает 
        white = cv.inRange(frame_hsv, np.array([0,0,255-sensity]), np.array([255,sensity,255]))
        return  white | black

    def InitializeField(self, frame_hsv, field):
        field_img = self.GetWhiteAndBlack(frame_hsv)
        closing = cv.morphologyEx(field_img, cv.MORPH_CLOSE, np.ones((10, 10), np.uint8))

        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        field.contour = self.GetFieldContour(contours)

        min_x = int(field.contour[:, :, 0:1].min())
        max_x = int(field.contour[:, :, 0:1].max())
        min_y = int(field.contour[:, :, 1:2].min())
        max_y = int(field.contour[:, :, 1:2].max())

        field.top_left_coords = (min_x, min_y)
        field.bottom_right_coords = (max_x, max_y)
        field.top_right_coords = (max_x, min_y)
        field.bottom_left_coords = (min_x, max_y)

    def DetectContours(self, frame_hsv, lower_color, higher_color, min_area, max_area, kernel):
        object_frame = cv.inRange(frame_hsv, lower_color, higher_color)
        closing = cv.morphologyEx(object_frame, cv.MORPH_CLOSE, np.ones((kernel, kernel), np.uint8))
        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        new_contours = []
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            ctr = np.array(box).reshape((-1, 1, 2)).astype(np.int32)
            area = Rectangle.Rectangle(ctr).area

            if min_area <= area <= max_area:
                new_contours.append(ctr)
        
        return new_contours
    
    def CalculateDistance(self, A, B):
        return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5
    
    def Scale(self, frame, scale_down=0.7):
        return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)

    def DetectPairButton(self, frame_hsv, buttons, color_name_1, color_name_2, frame):
        min_area = 300
        max_area = 500
        kernel = 30

        b1 = self.DetectContours(frame_hsv, 
                            buttons[color_name_1].lower_color, 
                            buttons[color_name_1].higher_color, 
                            min_area, 
                            max_area, 
                            kernel)
        b2 = self.DetectContours(frame_hsv, 
                            buttons[color_name_2].lower_color, 
                            buttons[color_name_2].higher_color, 
                            min_area, 
                            max_area, 
                            kernel)

        max_dist = 7
        min_dist = 20

        qq = []
        pp = []

        t = 0
        for cnt1 in b1:
            center1 = Rectangle.Rectangle(cnt1).center
            for cnt2 in b2:
                center2 = Rectangle.Rectangle(cnt2).center

                if min_dist <= self.CalculateDistance(center1, center2) <= max_dist:
                    qq.append(cnt1)
                    pp.append(cnt2)
                    cv.drawContours(frame, (cnt1,), -1, (120,0,120) , 4)
                    cv.drawContours(frame, (cnt2,), -1, (0,120,120) , 4)
                    t += 1

        if t == 0:
            #cv.imshow('frame', Scale(frame))
            #cv.waitKey(0)
            print("Couldnt find any")
        elif t != 1:
            cv.imshow('frame', self.Scale(frame))
            cv.waitKey(0)
            print("Too mcuh")

    def run(self) -> ResType.result_type[int, str]:
        self.logger.info("Start Application")
        
        listCamer = [self.VideoCameraOnRobot, self.VideoCameraOnHigh] 

        while self.VideoCameraOnRobot.IsOpen() and self.VideoCameraOnHigh.IsOpen():
            for index in [0, 1]:
                ret, frame = listCamer[index].read()

                if not ret:
                    self.logger.error(f"Not ret in {listCamer[index]}")
                    return ResType.result_type(ResType.Error(f"Not ret in {listCamer[index]}"))
                
                frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                
                if listCamer[index].getFrameCount == 1:
                    self.InitializeField(frame_hsv, self.Field)

                self.DetectPairButton(frame_hsv, self.buttons, 'blue', 'red', frame)
                self.DetectPairButton(frame_hsv, self.buttons, 'blue', 'green', frame)

                cv.drawContours(frame, (self.Field.contour,), -1, (0, 255, 0), 4)
                cv.imshow(f'frame {index}', self.Scale(frame))

                if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
                    break
                
                listCamer[index].raiseCount
                
        return ResType.result_type(ResType.Ok(200))    


if __name__ == "__main__":
    App().run()
