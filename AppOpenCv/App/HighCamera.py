import numpy as np
import cv2 as cv
from Buttons import Buttons
from Button import Button
from Field import Field
from Robot import Robot
from Rectangle import Rectangle
from Base import Base
from Owner import Owner

from Log_manager import Logs
import logging



class HighCamera:
    def __init__(self, path):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.info("Create Logs for high camera")

        button_colors_map = {
        "green": (np.array([50,100,140]), np.array([83,170,240])),  
        "blue": (np.array([90,158,124]), np.array([138,255,255])),
        "red": (np.array([157, 92, 175]), np.array([185, 241, 252])),
        "orange": (np.array([0, 100, 207]), np.array([40, 254, 247])),  
        }

        #  buttons init
        self.buttons = Buttons(button_colors_map)
        self.buttons['green'].is_good = True
        self.buttons['blue'].is_good = True

        #  field, bases, robots init; CONFIG
        self.field = Field()
        self.red_base = Base(Owner.ENEMY)
        self.green_base = Base(Owner.WE)

        #  setting the video
        video_name = path
        self.capture = cv.VideoCapture(video_name)
        self.frame_counter = 1

    def Scale(self, frame, scale_down=0.7):
        return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)

    def CalculateDistance(self, A, B):
        return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

    def GetRectangleFromContour(self, contour) -> Rectangle:
        rect = cv.minAreaRect(contour) 
        box = cv.boxPoints(rect)
        new_contour = np.array(box).reshape((-1,1,2)).astype(np.int32)
        return Rectangle(new_contour)

    """ Initialize field funcs"""
    def GetMaxAreaContour(self, contours):
        max_area = -1
        result_contour = None
        
        for cnt in contours:
            rectangle = self.GetRectangleFromContour(cnt)
            if rectangle.area > max_area:
                max_area = rectangle.area
                result_contour = rectangle.contour

        return result_contour

    def GetWhiteAndBlack(self, frame_hsv):
        # CALIBRATE
        black_lower = np.array([0, 0, 0])
        black_higher = np.array([200,255,100])

        # CALIBRATE
        sensity = 40 # ну так работает 
        white_lower = np.array([0,0,255-sensity])
        white_higher = np.array([255,sensity,255])

        black = cv.inRange(frame_hsv, black_lower, black_higher)
        white = cv.inRange(frame_hsv, white_lower, white_higher)

        return  white | black

    def InitializeField(self, frame_hsv):
        # CALIBRATE
        kernel = 10

        field_img = self.GetWhiteAndBlack(frame_hsv)
        closing = cv.morphologyEx(field_img, cv.MORPH_CLOSE, np.ones((kernel,kernel),np.uint8))  # делает линию сплошной
        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        
        self.field.contour = self.GetMaxAreaContour(contours)

        min_x = int(self.field.contour[:, :, 0:1].min())
        max_x = int(self.field.contour[:, :, 0:1].max())
        min_y = int(self.field.contour[:, :, 1:2].min())
        max_y = int(self.field.contour[:, :, 1:2].max())

        self.field.top_left_coords = (min_x, min_y)
        self.field.bottom_right_coords = (max_x, max_y)
        self.field.top_right_coords = (max_x, min_y)
        self.field.bottom_left_coords = (min_x, max_y)

    def SelectContoursByRatio(self, contours, ratio, eps=0.1):
        if ratio > 1:
            raise Exception("SelectContoursByRatio : ratio should be not greater than 1.0")
        selected_contours = []

        for cnt in contours:
            rectangle = self.GetRectangleFromContour(cnt)
            if ratio - eps <= rectangle.ratio <= ratio + eps:
                selected_contours.append(rectangle.contour)
        return selected_contours

    def InitializeBase(self, frame_hsv):
        # CALIBRATE
        lower_green = np.array([50, 100,100])
        higher_green = np.array([100, 180, 180])

        lower_red_1 = np.array([170,50,50])
        higher_red_1 = np.array([180,255,255])

        lower_red_2 = np.array([0,50,50])
        higher_red_2 = np.array([10,255,255])

        # CALIBRATE
        min_area = 8000
        max_area = 15000
        kernel = 30

        # CALIBRATE
        ratio = 0.7
        eps = 0.15

        contours = self.DetectContours(frame_hsv, ((lower_green, higher_green),), min_area, max_area, kernel)
        if not contours:
            raise Exception("InitializeBase : No contours by DetectContours. Check min_area, max_area, colors")

        contours = self.SelectContoursByRatio(contours, ratio, eps=eps)
        if not contours:
            raise Exception("InitializeBase : No contours by SelectContoursByRatio")

        result_contour = self.GetMaxAreaContour(contours)

        if result_contour is None:
            raise Exception("InitializeBase : No contours were found in area-range of", min_area, max_area)

        self.green_base.contour = result_contour


        contours = self.DetectContours(frame_hsv, ((lower_red_1, higher_red_1), (lower_red_2, higher_red_2)),
                                        min_area, max_area, kernel)  

        contours = self.SelectContoursByRatio(contours, ratio, eps=eps)
        if not contours:
            raise Exception("InitializeBase : No contours by SelectContoursByRatio")

        result_contour = self.GetMaxAreaContour(contours)

        if result_contour is None:
            raise Exception("InitializeBase : No contours were found in area-range of", min_area, max_area)

        self.red_base.contour = result_contour

    """ General functions """
    #colors -> tuple((lower_color_1, higher_color_1), (ower_color_2, higher_color_2), ...)
    def DetectContours(self, frame_hsv, color_pairs, min_area, max_area, kernel):
        objects_frame = cv.inRange(frame_hsv, color_pairs[0][0], color_pairs[0][1])
        for i in range(1, len(color_pairs)):
            objects_frame |= cv.inRange(frame_hsv, color_pairs[i][0], color_pairs[i][1])

        closing = cv.morphologyEx(objects_frame, cv.MORPH_CLOSE, np.ones((kernel,kernel),np.uint8)) 
        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        new_contours = []
        for cnt in contours:
            rectangle = self.GetRectangleFromContour(cnt)
            if min_area <= rectangle.area <= max_area:
                new_contours.append(rectangle.contour)

        return new_contours

    """ Update buttons (in pairs) """
    def UpdatePairButton(self, frame_hsv, color_name_1, color_name_2, frame):
        min_area = 300
        max_area = 500
        kernel = 30

        #  Как близко могут находится соседние кнопки
        max_dist = 70
        min_dist = 20
       
        button_contour_1 = self.DetectContours(frame_hsv, 
                            ((self.buttons[color_name_1].lower_color, self.buttons[color_name_1].higher_color),), 
                            min_area, 
                            max_area, 
                            kernel)
        button_contour_2 = self.DetectContours(frame_hsv, 
                            ((self.buttons[color_name_2].lower_color, self.buttons[color_name_2].higher_color),), 
                            min_area, 
                            max_area, 
                            kernel)

        selected_pair_contours = []


        """ Выбираем только те пары, которые находятся рядом с другом другом """
        for contour_1 in button_contour_1:
            center_1 = Rectangle(contour_1).center

            for contour_2 in button_contour_2:
                center_2 = Rectangle(contour_2).center

                if min_dist <= self.CalculateDistance(center_1, center_2) <= max_dist:
                    selected_pair_contours.append((contour_1, contour_2))

        if len(selected_pair_contours) == 0:
            self.buttons[color_name_1].is_visible = False
            self.buttons[color_name_2].is_visible = False
            return 

        
        best_pair = selected_pair_contours[0]
        best_pair_delta = 99999999

        """ Выбираем самую релевантную пару - которая ближе всего к прошлому положению """
        if self.buttons[color_name_1].x is not None:
            for pair in selected_pair_contours:
                contour_1, contour_2 = pair
                center_1 = Rectangle(contour_1).center
                center_2 = Rectangle(contour_2).center

                delta_1 = ((center_1[0] - self.buttons[color_name_1].x)**2 + (center_1[1] - self.buttons[color_name_1].y)**2)**0.5
                delta_2 = ((center_2[0] - self.buttons[color_name_2].x)**2 + (center_2[1] - self.buttons[color_name_2].y)**2)**0.5

                delta = delta_1 + delta_2

                if delta < best_pair_delta:
                    best_pair_delta = delta
                    best_pair = pair

        if best_pair_delta > 200 and self.buttons[color_name_1].x is not None:
            self.buttons[color_name_1].is_visible = False
            self.buttons[color_name_2].is_visible = False
            return 

        if best_pair_delta < 25:
            self.buttons[color_name_1].is_visible = True
            self.buttons[color_name_2].is_visible = True
            self.buttons[color_name_1].is_dynamic = 0
            self.buttons[color_name_2].is_dynamic = 0
            return

        center_1 = Rectangle(best_pair[0]).center
        center_2 = Rectangle(best_pair[1]).center

        if self.buttons[color_name_1].x is not None:
            self.buttons[color_name_1].SetVector(center_1[0] - self.buttons[color_name_1].x,
                                                    center_1[1] - self.buttons[color_name_1].y)

            self.buttons[color_name_2].SetVector(center_2[0] - self.buttons[color_name_2].x,
                                                    center_2[1] - self.buttons[color_name_2].y)
        
        if (not self.buttons[color_name_1].is_dynamic) or (not self.buttons[color_name_2].is_dynamic):
            self.buttons[color_name_1].is_dynamic = self.buttons[color_name_2].is_dynamic = 0


        self.buttons[color_name_1].is_visible = True
        self.buttons[color_name_1].x = center_1[0]
        self.buttons[color_name_1].y = center_1[1]
        self.buttons[color_name_1].contour = best_pair[0]

        self.buttons[color_name_2].is_visible = True
        self.buttons[color_name_2].x = center_2[0]
        self.buttons[color_name_2].y = center_2[1]
        self.buttons[color_name_2].contour = best_pair[1]

    """ Rendering contours and frame """
    def ShowButtons(self, frame):
        for color in self.buttons.map:
            button = self.buttons[color]
            contour_color = (0, 0, 0)
            if button.is_good:
                contour_color = (255, 255, 255)
            if button.IsDynamic():
                contour_color = (128, 64, 190)

            cv.drawContours(frame, (button.contour,), -1, contour_color, 4)

    def ShowField(self, frame):
        contour_color = (0,255,0)
        cv.drawContours(frame, (self.field.contour,), -1, contour_color, 4)

    def ShowFrame(self, frame):
        cv.imshow('frame', self.Scale(frame))
        return not (cv.waitKey(1) & 0xFF == ord('q'))

    def ShowBases(self, frame):
        green_base_contour_color = (102,255,70)
        red_base_contour_color = (255,255,102)

        cv.drawContours(frame, (self.green_base.contour,), -1, green_base_contour_color, 4)
        cv.drawContours(frame, (self.red_base.contour,), -1, red_base_contour_color, 4)

    def ShowPolygon(self, frame):
        self.ShowField(frame)
        self.ShowButtons(frame)
        self.ShowBases(frame)
        return self.ShowFrame(frame)

    """ Getting frame, already modified """
    def GetFrame(self, capture):
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
        return self.FixFishEye(frame)

    def FixFishEye(self, frame):
        h, w = frame.shape[:2]
        mtx = camera_matrix = np.array([[1182.719, 0, 927.03],
                [0, 1186.236, 609.52],
                [0, 0, 1]], dtype=np.float32)

        dist_coeffs = np.array([-0.5, 0.3, 0, 0, 0], dtype=np.float32)
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist_coeffs, (w,h), 1, (w,h))

        frame = cv.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)
        x, y, w, h = roi

        return frame[y:y+h, x:x+w]

    def MakeIteration(self):
        if not self.capture.isOpened():
            return False

        frame = self.GetFrame(self.capture)
        if frame is None:
            return False

        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        if self.frame_counter == 1:  
            self.InitializeField(frame_hsv)
            self.InitializeBase(frame_hsv)

        if self.frame_counter % 10 == 0:
            self.UpdatePairButton(frame_hsv, 'blue', 'red', frame)
            self.UpdatePairButton(frame_hsv, 'orange', 'green', frame)

        if not self.ShowPolygon(frame):
            return False

        self.frame_counter += 1

        return True

    def run(self):
        while self.MakeIteration():
            pass