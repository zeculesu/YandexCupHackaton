import numpy as np
import cv2 as cv

from Buttons import Buttons
from Button import Button
from Field import Field
from Robot import Robot
from Rectangle import Rectangle
from Base import Base
from Owner import Owner
from ValueObject import ValueObj
from TableObject import TableObj 
from Boarder import Boarder
from Bucket import Bucket

from Log_manager import Logs
import logging

import queue


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
        self.walls = Boarder()
        self.table = TableObj() 
        self.listBuckets = [Bucket(), Bucket()]

        #  value objects
        self.listValueObjects = [ValueObj(0), ValueObj(1)]

        #  setting the video
        video_name = path
        self.capture = cv.VideoCapture(video_name)
        self.frame_counter = 1

        #  path constructor
        self.map_img = None
        self.added_dots = []
        self.p = 9


    


    # Debug boy
    def Lol(self, path):
        frame = cv.imread(path)
        frame = self.FixFishEye(frame)
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        self.InitializeField(frame_hsv)
        self.InitializeBase(frame_hsv)
        self.InitializeWalls(frame_hsv, frame)
        self.UpdatePairButton(frame_hsv, 'blue', 'red', frame)
        self.UpdatePairButton(frame_hsv, 'orange', 'green', frame)


    """ Helper funcs """
    def Scale(self, frame, scale_down=0.7):
        return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)

    def CalculateDistance(self, A, B):
        return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

    def GetRectangleFromContour(self, contour) -> Rectangle:
        rect = cv.minAreaRect(contour) 
        box = cv.boxPoints(rect)
        new_contour = np.array(box).reshape((-1,1,2)).astype(np.int32)
        return Rectangle(new_contour)

    def ShowContours(self, contours, frame):
        new_frame = frame.copy()
        cv.drawContours(new_frame, contours, -1, (120, 60, 150), 4)
        cv.imshow('frame', self.Scale(new_frame))
        cv.waitKey(0)

    def ShowContour(self, contour, frame):
        new_frame = frame.copy()
        cv.drawContours(new_frame, (contour,), -1, (80, 100, 150), 5)
        cv.imshow('frame', self.Scale(new_frame))
        cv.waitKey(0)

    #color_pairs -> tuple((lower_color_1, higher_color_1), (lower_color_2, higher_color_2), ...)
    def DetectContours(self, frame_hsv, color_pairs, min_area, max_area, kernel, show=False, frame=None):
        objects_frame = cv.inRange(frame_hsv, color_pairs[0][0], color_pairs[0][1])
        for i in range(1, len(color_pairs)):
            objects_frame |= cv.inRange(frame_hsv, color_pairs[i][0], color_pairs[i][1])

        closing = cv.morphologyEx(objects_frame, cv.MORPH_CLOSE, np.ones((kernel,kernel),np.uint8))

        if show:
            cv.imshow('frame', self.Scale(closing))
            cv.waitKey(0)

        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        new_contours = []
        for cnt in contours:
            rectangle = self.GetRectangleFromContour(cnt)
            if min_area <= rectangle.area <= max_area:
                new_contours.append(rectangle.contour)

        return new_contours 
    

    """ Path constructor """
    def DrawStatic(self, frame, color, thikness=0):
        field_cnt_scaled = self.field.contour.copy()
        for i in range(len(field_cnt_scaled)):
            field_cnt_scaled[i] = np.divide(field_cnt_scaled[i], self.p)

        cv.drawContours(frame, (field_cnt_scaled,), 0, color, thikness)
        #cv.imshow('frame', self.Scale(self.map_img, scale_down=int(self.p / 1.3)))
        #cv.waitKey(0)

        for line in self.walls.lines:
            cv.line(frame, (line[0][0] // self.p, line[0][1] // self.p) , (line[1][0] // self.p, line[1][1] // self.p), color, thikness+1)

        new_table_cnt = self.table.contour.copy()
        for i in range(len(field_cnt_scaled)):
            new_table_cnt[i] = np.divide(new_table_cnt[i], self.p)
        cv.drawContours(frame, (new_table_cnt,), -1, color, thikness)
        #cv.imshow('frame', self.Scale(self.map_img, scale_down=int(self.p / 1.3)))
        #cv.waitKey(0)

        for bucket in self.listBuckets:
            a, b, c, d = bucket.top_left_coords, bucket.top_right_coords, bucket.bottom_right_coords, bucket.bottom_left_coords
            a = a[0] // self.p, a[1] // self.p
            b = b[0] // self.p, b[1] // self.p
            c = c[0] // self.p, c[1] // self.p
            d = d[0] // self.p, d[1] // self.p

            cv.line(frame, a, b, color, thikness+1)
            cv.line(frame, b, c, color, thikness+1)
            cv.line(frame, c, d, color, thikness+1)
            cv.line(frame, d, a, color, thikness+1)

    def DrawDynamic(self, frame, color, thikness=0):
        for b_color in self.buttons.map:
            button = self.buttons[b_color]

            if button.contour is not None:
                new_but_contour =  button.contour.copy()
                for i in range(len(new_but_contour)):
                    new_but_contour[i] = np.divide(new_but_contour[i], self.p)
                
                cv.drawContours(frame, (new_but_contour,), -1, color, thikness * 2)

        # robot
        # ...

        # value objects
        for i in range(len(self.listValueObjects)):
            if self.listValueObjects[i].contour is not None:
                cnt1 = self.listValueObjects[i].contour.copy()
                for i in range(len(cnt1)):
                    cnt1[i] = np.divide(cnt1[i], self.p)

                cv.drawContours(frame, (cnt1,), -1, color, thikness)




    def MakeMapImage(self, frame):
        a_ = (frame.shape[0] + 200) + (self.p - ((frame.shape[0] + 200) % self.p))
        b_ = (frame.shape[1]) + (self.p - (frame.shape[1] % self.p))

        a__ = a_ // self.p
        b__ = b_ // self.p


        self.map_img = np.zeros((a__, b__, frame.shape[2]))
        white = (255, 255, 255)
        purple = (254, 0, 254)

        self.DrawStatic(self.map_img, purple, 6)
        self.DrawDynamic(self.map_img, purple, 6)

        self.DrawStatic(self.map_img, white, 0)
        self.DrawDynamic(self.map_img, white, 0)

        
        cv.imshow('frame', self.Scale(self.map_img, scale_down=int(self.p / 1.3)))
        cv.waitKey(0)
    

    def CanBe(self, s, t, v):
        return True

    # v - 0, 1, 2, 3, 4, 5, 6, 7 -> t, tr, t, br, b, bl, l, tl 
    def MakePath(self, s, t, v):
        robot_w = 50
        robot_h = 30

        robot_w = (robot_w + self.p - 1) // self.p
        robot_h = (robot_h + self.p - 1) // self.p

        s = s[1], s[0]
        t = t[1], t[0]


        n, m =  self.map_img.shape[0], self.map_img.shape[1]
        # 131 208
        #print(n, m)
        dists = [[10**9 for _ in range(m)] for _ in range(n)]
        prevs = [[None for _ in range(m)] for _ in range(n)]
        used = [[False for _ in range(m)] for _ in range(n)]


        dists[s[0]][s[1]] = 0

        q = queue.PriorityQueue()
        q.put((0, s[0], s[1], v))
        
        def GetK(x, y):
            m = {
                255: 10**4,
                254: 10**2,
                0: 1,
            }

            return m[self.map_img[to_x][to_y][0]]

        while not q.empty():
            c_cur, x, y, v = q.get()
            used[x][y] = True;

            if dists[x][y] < c_cur:
                continue

            top_cost = 1
            right_cost = 1
            left_cost = 1
            bottom_cost = 1

            if v == 't':
                right_cost = left_cost = 3
                bottom_cost = 5
            elif v == 'b':
                right_cost = left_cost = 3
                top_cost = 5
            elif v == 'r':
                top_cost = bottom_cost = 3
                left_cost = 5
            elif v == 'l':
                top_cost = bottom_cost = 3
                right_cost = 5

            #print(x, y)
            to_x, to_y = x, y - 1
            k = 1
            if to_y >= 0 and not used[to_x][to_y]:
                k = GetK(to_x, to_y)

                if dists[to_x][to_y] > dists[x][y] + top_cost*k:
                    dists[to_x][to_y] = dists[x][y] + top_cost*k
                    prevs[to_x][to_y] = (x, y)
                    q.put((dists[to_x][to_y], to_x, to_y, 't'))

            to_x, to_y = x, y + 1
            if to_y < self.map_img.shape[1] and not used[to_x][to_y]:
                k = GetK(to_x, to_y)


                if dists[to_x][to_y] > dists[x][y] + bottom_cost*k:
                    dists[to_x][to_y] = dists[x][y] + bottom_cost*k
                    prevs[to_x][to_y] = (x, y)
                    q.put((dists[to_x][to_y], to_x, to_y, 'b'))

            to_x, to_y = x + 1, y
            if to_x < self.map_img.shape[0] and not used[to_x][to_y]:
                k = GetK(to_x, to_y)


                if dists[to_x][to_y] > dists[x][y] + right_cost*k:
                    dists[to_x][to_y] = dists[x][y] + right_cost*k
                    prevs[to_x][to_y] = (x, y)
                    q.put((dists[to_x][to_y], to_x, to_y, 'r'))

            to_x, to_y = x - 1, y
            if to_x >= 0 and not used[to_x][to_y]:
                k = GetK(to_x, to_y)


                if dists[to_x][to_y] > dists[x][y] + left_cost*k:
                    dists[to_x][to_y] = dists[x][y] + left_cost*k
                    prevs[to_x][to_y] = (x, y)
                    q.put((dists[to_x][to_y], to_x, to_y, 'l'))


        path = [t]

        x, y = t
        while prevs[x][y] != None:
            x, y = prevs[x][y]
            path.append((x, y))

        for i in range(len(path) - 1, -1, -1):
            x, y = path[i]
            self.map_img[x][y] = (255, 0, 0)
            #print(self.map_img[to_x][to_y] )

        self.map_img[s[0]][s[1]] = (10, 255, 10)
        self.map_img[t[0]][t[1]] = (10, 255, 10)

        cv.imshow('frame', self.Scale(self.map_img, scale_down=int(self.p / 1.3)))
        cv.waitKey(0)

        return path




    """ Initialize field """
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

    def InitializeField(self, frame_hsv, frame):
        # CALIBRATE
        kernel = 10

        field_img = self.GetWhiteAndBlack(frame_hsv)
        closing = cv.morphologyEx(field_img, cv.MORPH_CLOSE, np.ones((kernel,kernel),np.uint8))  # делает линию сплошной
        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        
        if not contours:
            self.logger.critical("Initialize : Field : no contours : check colors")

        self.field.contour = self.GetMaxAreaContour(contours)

        #self.ShowContours(contours, frame) # <- for debug - color, area selection

        if self.field.contour is None:
            self.logger.critical("Initialize : Field : no contours with max area")

        min_x = int(self.field.contour[:, :, 0:1].min())
        max_x = int(self.field.contour[:, :, 0:1].max())
        min_y = int(self.field.contour[:, :, 1:2].min())
        max_y = int(self.field.contour[:, :, 1:2].max())

        self.field.top_left_coords = (min_x, min_y)
        self.field.bottom_right_coords = (max_x, max_y)
        self.field.top_right_coords = (max_x, min_y)
        self.field.bottom_left_coords = (min_x, max_y)

        self.logger.info("Initialize : Field : DONE")

    """ Initialize bases """
    def SelectContoursByRatio(self, contours, ratio, eps=0.1):
        if ratio > 1:
            raise Exception("SelectContoursByRatio : ratio should be not greater than 1.0")
        selected_contours = []

        for cnt in contours:
            rectangle = self.GetRectangleFromContour(cnt)
            if ratio - eps <= rectangle.ratio <= ratio + eps:
                selected_contours.append(rectangle.contour)
        return selected_contours

    def InitializeBases(self, frame_hsv, frame):
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
            self.logger.critical("Initialize : Base : green : No contours by DetectContours. Check min_area, max_area, colors")
            return
        #self.ShowContours(contours, frame) # <- for debug - green color, area selection


        contours = self.SelectContoursByRatio(contours, ratio, eps=eps)
        if not contours:
            self.logger.critical("Initialize : Base : green : No contours by SelectContoursByRatio. Check ratio, eps")
            return
        #self.ShowContours(contours, frame) # <- for debug - ratio, eps selection

        contours = [cnt for cnt in contours if self.field.Contains(Rectangle(cnt).center)]
        if not contours:
            self.logger.critical("Initialize : Base : green : No contours in the field")
            return
        #self.ShowContours(contours, frame) # <- for debug - check field

        result_contour = self.GetMaxAreaContour(contours)

        if result_contour is None:
            self.logger.critical("Initialize : Base : green : No contours by GetMaxAreaContour. Check contours")

        self.green_base.contour = result_contour
        rect = self.GetRectangleFromContour(result_contour)

        (x,y,w,h) = cv.boundingRect(result_contour)
        min_x, max_x = x, x+w
        min_y, max_y = y, y+h

        self.green_base.top_left_coords = (min_x, min_y)
        self.green_base.top_right_coords = (max_x, min_y)
        self.green_base.bottom_right_coords = (max_x, max_y)
        self.green_base.bottom_left_coords = (min_x, max_y)

        self.logger.info("Initialize : Base : green : DONE")

        contours = self.DetectContours(frame_hsv, ((lower_red_1, higher_red_1), (lower_red_2, higher_red_2)),
                                        min_area, max_area, kernel)  

        if not contours:
            self.logger.critical("Initialize : Base : red : No contours by DetectContours. Check min_area, max_area, colors")
            return
        #self.ShowContours(contours, frame) # <- for debug - red color, area selection


        contours = self.SelectContoursByRatio(contours, ratio, eps=eps)
        if not contours:
            self.logger.critical("Initialize : Base : red : No contours by SelectContoursByRatio. Check ratio, eps")
            return
        #self.ShowContours(contours, frame) # <- for debug - ratio, eps selection

        contours = [cnt for cnt in contours if self.field.Contains(Rectangle(cnt).center)]
        if not contours:
            self.logger.critical("Initialize : Base : red : No contours in the field")
            return
        #self.ShowContours(contours, frame) # <- for debug - check field

        result_contour = self.GetMaxAreaContour(contours)

        if result_contour is None:
            self.logger.critical("Initialize : Base : red : No contours by GetMaxAreaContour. Check contours")
            return

        self.red_base.contour = result_contour
        rect = self.GetRectangleFromContour(result_contour)
        (x,y,w,h) = cv.boundingRect(result_contour)
        min_x, max_x = x, x+w
        min_y, max_y = y, y+h

        self.red_base.top_left_coords = (min_x, min_y)
        self.red_base.top_right_coords = (max_x, min_y)
        self.red_base.bottom_right_coords = (max_x, max_y)
        self.red_base.bottom_left_coords = (min_x, max_y)

        self.logger.info("Initialize : Base : red : DONE")

    """ Initialize walls """
    def InitializeNormalWalls(self, frame_hsv, frame):
        # NEED TO INIT FIELD

        top_left = self.field.top_left_coords
        top_right = self.field.top_right_coords
        bottom_left = self.field.bottom_left_coords
        bottom_right = self.field.bottom_right_coords

        min_x = min(top_left[0], bottom_left[0])
        max_x = max(top_right[0],bottom_right[0])
        min_y = min(top_right[1], top_left[1])
        max_y = max(bottom_right[1], bottom_left[1])

        step_x = (max_x - min_x) // 20
        step_y = (max_y - min_y) // 20

        rect_1_coords = (min_x + step_x*4, min_y + step_y * 2)
        rect_2_coords = (rect_1_coords[0] + step_x * 9, rect_1_coords[1])
        rect_3_coords = (rect_2_coords[0], rect_1_coords[1] + step_y * 13)
        rect_4_coords = (rect_1_coords[0], rect_3_coords[1])

        x_len = int(step_x * 3.0)
        y_len = int(step_y * 4.0)
        #x_len = int(step_x * 4.0)
        #y_len = int(step_y * 5.0)

        class Rect:
            def __init__(self, coords, x_len, y_len):
                self.A = (x, y) = coords
                self.B = (x + x_len, y)
                self.C = (x + x_len, y + y_len)
                self.D = (x, y + y_len)
                self.x_len = x_len
                self.y_len = y_len

            def HasPoint(self, coords):
                x, y = coords
                return (self.A[0] <= x <= self.A[0] + self.x_len) and (self.A[1] <= y <= self.A[1] + self.y_len)

        rects = []

        def draw_rect(rect_coords):
            x, y = rect_coords
            cv.line(frame, (x, y), (x, y + y_len), (255, 104, 150), 3)
            cv.line(frame, (x, y), (x + x_len, y), (255, 104, 150), 3)
            cv.line(frame, (x + x_len, y), (x + x_len, y + y_len), (255, 104, 150), 3)
            cv.line(frame, (x, y + y_len), (x + x_len, y + y_len), (255, 104, 150), 3)

        for rect_coords in (rect_1_coords, rect_2_coords, rect_3_coords, rect_4_coords):
            #draw_rect(rect_coords)    # <- debug
            #cv.imshow('frame', self.Scale(frame)) # <- debug - рисует секторы, в которых ищутся углы стен
            #cv.waitKey(0)             # <- debug
            rects.append(Rect(rect_coords, x_len, y_len))

        # 1 2
        # 4 3

        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        frame_hsv = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([255, 255, 70]))

        kernel = 5

        closing = cv.morphologyEx(frame_hsv, cv.MORPH_CLOSE, np.ones((kernel,kernel), np.uint8)) 
        dilation = cv.dilate(closing, np.ones((kernel,kernel), np.uint8), iterations=2)
        closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, np.ones((kernel,kernel), np.uint8)) 

        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        #self.ShowContours(contours, frame) # <- debug - рисует контуры стен + белые квадраты, если есть

        contour_color = (150, 104, 150)

        selected_contours = []

        class Edge:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.xy = (self.x, self.y)
                

        top_left_edge = None
        bottom_right_edge = None

        connections = []

        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            # 30k - 70k
            # Не больше 75 тысяч, Больше 40 тысяч  (48000)
            # 30k / 4 = 8k
            if cv.contourArea(cnt) < 8000:
                continue

            dots = []

            if rects[0].HasPoint((x, y)):
                cv.drawContours(frame, (cnt,), -1, contour_color, 4)
                top_left_edge = Edge(x + 15, y + 15)
                cv.circle(frame, (x + 15, y + 15), 7, (104, 29, 59), -1)
                dots.append(1)

            if rects[1].HasPoint((x + w, y)):
                cv.drawContours(frame, (cnt,), -1, contour_color, 4)
                cv.circle(frame, (x + w - 10, y + 10), 7, (104, 29, 59), -1)
                dots.append(2)

            if rects[2].HasPoint((x + w, y + h)):
                cv.drawContours(frame, (cnt,), -1, contour_color, 4)
                bottom_right_edge = Edge(x + w - 30, y + h - 20)

                cv.circle(frame, (x + w - 30, y + h - 20), 7, (104, 29, 59), -1)
                dots.append(3)

            if rects[3].HasPoint((x, y + h)):
                cv.drawContours(frame, (cnt,), -1, contour_color, 4)
                
                cv.circle(frame, (x + 30, y + h - 20), 7, (104, 29, 59), -1)
                dots.append(4)

            if dots:
                connections.append(dots)
        

        # Если есть один островок
        solo = None

        for i in range(len(connections)):
            if len(connections[i]) == 1:
                solo = connections[i][0]

        for i in range(len(connections)):
            if len(connections[i]) == 4 and solo is not None:
                connections[i].remove(solo)

        lines = []

        if top_left_edge is None:
            self.logger.critical("Initialize : Walls : top_left_edge : check rectangles places")
            return lines, None, None

        if bottom_right_edge is None:
            self.logger.critical("Initialize : Walls : bottom_right_edge : check rectangles places")
            return lines, None, None

        if len(connections) == 1 and len(connections[0]) == 4:
            return lines, top_left_edge, bottom_right_edge

        gorizontal_line_length = abs(int((bottom_right_edge.x - top_left_edge.x) * 0.3055555555555556))  
        vertical_line_length = abs(int((top_left_edge.y - bottom_right_edge.y) / 3)) 
            
        def AreConnected(i1, i2):
            for one in connections:
                if (i1 in one) and (i2 in one):
                    return True
            return False

        def ConnectOnHorizontal(lines, left_coords, right_coords, i1, i2):
            f = AreConnected(i1, i2)

            if f:
                lines.append(  (left_coords, right_coords)  )
            else:
                lines.append((  left_coords, (left_coords[0] + gorizontal_line_length, left_coords[1])   ))
                lines.append((  (right_coords[0] - gorizontal_line_length, right_coords[1]) , right_coords ))

        def ConnectOnVerticalLine(lines, top_coords, bottom_coords, i1, i2):
            f = AreConnected(i1, i2)

            if f:
                lines.append(  (top_coords, bottom_coords)  )
            else:
                lines.append((  top_coords, (top_coords[0], top_coords[1] + vertical_line_length)   ))
                lines.append((  (bottom_coords[0], bottom_coords[1] - vertical_line_length) , bottom_coords ))

        ConnectOnHorizontal(lines, top_left_edge.xy, (bottom_right_edge.x, top_left_edge.y), 1, 2)
        ConnectOnHorizontal(lines, (top_left_edge.x, bottom_right_edge.y), bottom_right_edge.xy, 3, 4)

        ConnectOnVerticalLine(lines, top_left_edge.xy, (top_left_edge.x, bottom_right_edge.y), 1, 4)
        ConnectOnVerticalLine(lines, (bottom_right_edge.x, top_left_edge.y), bottom_right_edge.xy, 2, 3)

        return lines, top_left_edge, bottom_right_edge

    def InitializeWalls(self, frame_hsv, frame):
        # NEED FIELD INIT

        new_frame = frame.copy()
        lines, top_left_edge, bottom_right_edge = self.InitializeNormalWalls(frame_hsv, new_frame)
        if lines:
            self.walls.lines = lines
            self.logger.info("Initialize : Walls : DONE")
            return

        top_left = self.field.top_left_coords
        top_right = self.field.top_right_coords
        bottom_left = self.field.bottom_left_coords
        bottom_right = self.field.bottom_right_coords
        min_x = min(top_left[0], bottom_left[0])
        max_x = max(top_right[0],bottom_right[0])
        min_y = min(top_right[1], top_left[1])
        max_y = max(bottom_right[1], bottom_left[1])

        step_x = (max_x - min_x) // 20
        step_y = (max_y - min_y) // 20

        rect_1_coords = (min_x + step_x*4, min_y + step_y * 2)
        rect_2_coords = (rect_1_coords[0] + step_x * 9, rect_1_coords[1])
        rect_3_coords = (rect_2_coords[0], rect_1_coords[1] + step_y * 13)
        rect_4_coords = (rect_1_coords[0], rect_3_coords[1])

        mid_1 = ( (rect_1_coords[0] + rect_2_coords[0]) // 2  , (rect_1_coords[1] + rect_2_coords[1]) // 2  )
        mid_2 = ( (rect_1_coords[0] + rect_4_coords[0]) // 2  , (rect_1_coords[1] + rect_4_coords[1]) // 2  )
        mid_3 = ( (rect_2_coords[0] + rect_3_coords[0]) // 2  , (rect_2_coords[1] + rect_3_coords[1]) // 2  )
        mid_4 = ( (rect_3_coords[0] + rect_4_coords[0]) // 2  , (rect_3_coords[1] + rect_4_coords[1]) // 2  )

        rect_1_coords = mid_1
        rect_2_coords = mid_2
        rect_3_coords = mid_3
        rect_4_coords = mid_4

        x_len = int(step_x * 3)
        y_len = int(step_y * 4)

        class Rect:
            def __init__(self, coords, x_len, y_len):
                self.A = (x, y) = coords
                self.B = (x + x_len, y)
                self.C = (x + x_len, y + y_len)
                self.D = (x, y + y_len)
                self.x_len = x_len
                self.y_len = y_len

            def HasPoint(self, coords):
                x, y = coords
                return (self.A[0] <= x <= self.A[0] + self.x_len) and (self.A[1] <= y <= self.A[1] + self.y_len)

        mids = [mid_1, mid_2, mid_3, mid_4]

        index = None
        all_dead = False
        for i in range(len(mids)):
            new_frame = frame.copy()
            coords = mids[i]

            cv.rectangle(new_frame, coords, (coords[0] + x_len, coords[1] + y_len), (255,255,255), -1)
            
            lines, top_left_edge, bottom_right_edge = self.InitializeNormalWalls(cv.cvtColor(new_frame, cv.COLOR_BGR2HSV), new_frame)
            if not lines:
                if index is not None:
                    all_dead = True
                else:
                    index = i + 1

        lines = []

        gorizontal_line_length = abs(int((bottom_right_edge.x - top_left_edge.x) * 0.3055555555555556))  
        vertical_line_length = abs(int((top_left_edge.y - bottom_right_edge.y) / 3)) 
        ban_line = ((-100, -100), (-100, -100))

        x_min, y_min = top_left_edge.x, top_left_edge.y
        x_max, y_max = bottom_right_edge.x, bottom_right_edge.y

        def ConnectOnHorizontal(lines, left_coords, right_coords):
            lines.append((  left_coords, (left_coords[0] + gorizontal_line_length, left_coords[1])   ))
            lines.append((  (right_coords[0] - gorizontal_line_length, right_coords[1]) , right_coords ))

        def ConnectOnVerticalLine(lines, top_coords, bottom_coords):
            lines.append((  top_coords, (top_coords[0], top_coords[1] + vertical_line_length)   ))
            lines.append((  (bottom_coords[0], bottom_coords[1] - vertical_line_length) , bottom_coords ))

        lines.append(((x_min, y_min), (x_max, y_min)))
        lines.append(((x_min, y_min), (x_min, y_max)))
        lines.append(((x_max, y_min), (x_max, y_max)))
        lines.append(((x_min, y_max), (x_max, y_max)))

        if not all_dead:
            if index == 1:
                ban_line = ((x_min, y_min), (x_max, y_min))
                ConnectOnHorizontal(lines, top_left_edge.xy, (bottom_right_edge.x, top_left_edge.y))
                # первый со вторым hor
            elif index == 2:
                ban_line = ((x_min, y_min), (x_min, y_max))
                ConnectOnVerticalLine(lines, top_left_edge.xy, (top_left_edge.x, bottom_right_edge.y))
                # первый с четвертым vert
            elif index == 3:
                ban_line = ((x_max, y_min), (x_max, y_max))
                ConnectOnVerticalLine(lines, (bottom_right_edge.x, top_left_edge.y), bottom_right_edge.xy)
                # второй с третьим vert
            elif index == 4:
                ban_line = ((x_min, y_max), (x_max, y_max))
                ConnectOnHorizontal(lines, (top_left_edge.x, bottom_right_edge.y), bottom_right_edge.xy)
                # третий с четвертым hor
            if ban_line in lines:
                lines.remove(ban_line)

        self.walls.lines = lines
        self.logger.info("Initialize : Walls : DONE")

    def InitializeBucket(self, Base, frame_hsv, frame):
        if (self.listBuckets[0].top_right_coords[0] is None):
            Bucket = self.listBuckets[0]
        else:
            Bucket = self.listBuckets[1]

        # Coord. Base
        Top_base_l = Base.top_left_coords
        Top_base_r = Base.top_right_coords

        bottom_base_l = Base.bottom_left_coords
        bottom_base_r = Base.bottom_right_coords

        ratio = 0.309

        # Coord. Field
        Top_field_l = self.field.top_left_coords
        Top_field_r = self.field.top_right_coords

        bottom_field_l = self.field.bottom_left_coords
        bottom_field_r = self.field.bottom_right_coords

        Eps = 150

        # if left site Vertical
        if (abs(Top_base_l[0] - Top_field_l[0]) < Eps and abs(bottom_base_l - bottom_field_l) < Eps):
            delta_x = Top_base_r[0] - Top_base_l[0]
            delta_y = Top_base_l[1] - bottom_base_l[1]

            ratio_x = 0.333
            ratio_y = 0.309

            # Top left
            coord_x = Top_base_l[0]
            coord_y = Top_base_l[1] - ratio_y * delta_y

            Bucket.top_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket left site vertical, TOP LEFT : {(coord_x, coord_y)}")

            # Top right
            coord_x = Top_base_r[0] - ratio_x * delta_x
            coord_y = Top_base_r[1] - ratio_y * delta_y

            Bucket.top_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket left site vertical, TOP RIGHT : {(coord_x, coord_y)}")

            #  Bottom left
            coord_x = bottom_base_l[0]
            coord_y = bottom_base_l[1] + ratio_y * delta_y

            Bucket.bottom_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket left site vertical, BOTTOM LEFT : {(coord_x, coord_y)}")

            # Bottom right
            coord_x = bottom_base_r[0] - ratio_x * delta_x
            coord_y = bottom_base_r[1] - ratio_y * delta_y

            Bucket.bottom_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket left site Vertical, BOTTOM RIGHT : {(coord_x, coord_y)}")

        # if top site Gorizont
        elif (abs(Top_base_l[1] - Top_field_l[1]) < Eps and abs(Top_base_r[1] - Top_field_r[1]) < Eps):
            delta_x = Top_base_l[0] - Top_base_r[0]
            delta_y = Top_base_l[1] - bottom_base_l[1]

            ratio_x = 0.309
            ratio_y = 0.333

            # Top right
            coord_x = Top_base_r[0] - ratio_x * delta_x
            coord_y = Top_base_r[1]

            Bucket.top_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket top site Gorizont, TOP RIGHT : {(coord_x, coord_y)}")

            # Top left
            coord_x = Top_base_l[0] + ratio_x * delta_x
            coord_y = Top_base_l[1]

            Bucket.top_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket top site Gorizont, TOP LEFT : {(coord_x, coord_y)}")

            # Bottom left
            coord_x = bottom_base_l[0] + ratio_x * delta_x
            coord_y = bottom_base_l[1] + ratio_y * delta_y

            Bucket.bottom_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket top site gorizont, BOTTOM LEFT : {(coord_x, coord_y)}")

            # Bottom right
            coord_x = bottom_base_r[0] - ratio_x * delta_x
            coord_y = bottom_base_r[1] + ratio_y * delta_y

            Bucket.bottom_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket top site gorizont, BOTTOM RIGHT : {(coord_x, coord_y)}")

        # if right site Vertical
        elif (abs(Top_base_r[0] - Top_base_r[0]) < Eps and abs(bottom_base_r[0] - bottom_field_r[0]) < Eps):
            delta_x = Top_base_r[0] - Top_base_l[0]
            delta_y = Top_base_r[1] - bottom_base_r[1]

            ratio_x = 0.333
            ratio_y = 0.309

            # Top right
            coord_x = Top_base_r[0]
            coord_y = Top_base_r[1] - ratio_y * delta_y


            Bucket.top_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket right site Vertical, TOP RIGHT : {(coord_x, coord_y)}")

            # Top left
            coord_x = Top_base_l[0] + ratio_x * delta_x
            coord_y = Top_base_l[1] - ratio_y * delta_y

            Bucket.top_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket right site Vertical, TOP LEFT : {(coord_x, coord_y)}")

            # Bottom left
            coord_x = bottom_base_l[0] + ratio_x * delta_x
            coord_y = bottom_base_l[1] + ratio_y * delta_y

            Bucket.bottom_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket right site Vertical, BOTTOM LEFT : {(coord_x, coord_y)}")

            # Bottom right
            coord_x = bottom_base_r[0]
            coord_y = bottom_base_r[1] + ratio_y * delta_y

            Bucket.bottom_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket right site vertical, BOTTOM RIGHT : {(coord_x, coord_y)}")

        # if bottom site Gorizont
        elif (abs(bottom_base_r[1] - bottom_field_r[1]) < Eps and abs(bottom_base_l[1] -
                                                                      bottom_field_l[1]) < Eps):

            delta_x = Top_base_r[0] - Top_base_l[0]
            delta_y = Top_base_l[1] - bottom_base_l[1]

            ratio_x = 0.309
            ratio_y = 0.333

            # Top right
            coord_x = Top_base_r[0] - ratio_x * delta_x
            coord_y = Top_base_r[1] - ratio_y * delta_y

            Bucket.top_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket bottom site Gorizont, TOP RIGHT : {(coord_x, coord_y)}")

            # Top left
            coord_x = Top_base_l[0] + ratio_x * delta_x
            coord_y = Top_base_l[1] - ratio_y * delta_y

            Bucket.top_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket bottom site Gorizont, TOP LEFT : {(coord_x, coord_y)}")

            # Bottom left
            coord_x = bottom_base_l[0] + ratio_x * delta_x
            coord_y = bottom_base_l[1]

            Bucket.bottom_left_coords = (coord_x, coord_y)
            self.logger.debug("Bucket bottom site Gorizont, BOTTOM LEFT : {(coord_x, coord_y)}")

            # Bottom right
            coord_x = bottom_base_r[0] - ratio_x * delta_x
            coord_y = bottom_base_r[1]

            Bucket.bottom_right_coords = (coord_x, coord_y)
            self.logger.debug("Bucket bottom site Gorizont, BOTTOM RIGHT : {(coord_x, coord_y)}")

        Bucket.top_right_coords = tuple(map(int, Bucket.top_right_coords))
        Bucket.top_left_coords = tuple(map(int, Bucket.top_left_coords))
        Bucket.bottom_right_coords = tuple(map(int, Bucket.bottom_right_coords))
        Bucket.bottom_left_coords = tuple(map(int, Bucket.bottom_left_coords))

    """ Initialize ValueObjects """
    def InitializeValueObject(self, index, frame_hsv, frame):
        #CALIBRATE
        lower_bound = np.array([0, 178, 130])
        upper_bound = np.array([179, 255, 255])

        value_object = self.listValueObjects[index]

        value_object.is_lower_color = lower_bound
        value_object.is_upper_color = upper_bound

        #CALIBRATE
        min_area = 200
        max_area = 800 
        kernel = 30
        
        contours = self.DetectContours(frame_hsv, ((lower_bound,
                                                     upper_bound),),min_area, max_area, kernel)
        if not contours:
            self.logger.critical(f"Initialize : ValueObj : {index} : no contours by DetectContours : Check min_area, max_area, colors")
            return
        #self.ShowContours(contours, frame) # <- debug - Selection by color, area

        result_contour = None
        min_delta = 700
        max_delta = 0

        if index == 0:
            field_center = self.field.GetCenter()
            for cnt in contours:
                center = Rectangle(cnt).center
                if (not self.field.Contains(center)) or (self.red_base.Contains(center)) or (self.green_base.Contains(center)):
                    continue

                delta = self.CalculateDistance(center, field_center)
                if delta > max_delta and self.field.Contains(center):
                    result_contour = cnt  
                    max_delta = delta

        else:
            for cnt in contours:
                center = Rectangle(cnt).center
                if (not self.field.Contains(center)) or (self.red_base.Contains(center)) or (self.green_base.Contains(center)):
                    continue

                delta = self.CalculateDistance(center, (self.listValueObjects[0].x, self.listValueObjects[0].y))
                if delta > min_delta and self.field.Contains(center):
                    result_contour = cnt
                    delta = min_delta  


        if result_contour is None:
            self.logger.critical(f"Initialize : ValueObj : {index} : Check min delta")
        else:
            value_object.contour = result_contour 
            center = Rectangle(result_contour).center
            
            value_object.x = center[0]
            value_object.y = center[1]
            self.logger.info(f"Initialize : ValueObj : {index} : DONE")

    """ Initialize Table """
    def InitializeTable(self, frame_hsv, frame):
        lower_bound = np.array([0, 0, 0])
        upper_bound = np.array([255, 255, 120])
        
        self.table.is_lower_color = lower_bound
        self.table.is_upper_color = upper_bound

        #CALIBRATE
        min_area = 30000
        max_area = 120000
        kernel = 8

        #CALIBRATE
        ratio = 0.8
        eps = 0.2
        
        frame_hsv = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([255, 255, 120]))
        closing = cv.morphologyEx(frame_hsv, cv.MORPH_CLOSE, np.ones((kernel,kernel), np.uint8)) 

        #cv.imshow('frame', self.Scale(closing)) # <- debug
        #cv.waitKey(0) # <- debug

        contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        contours = [cnt for cnt in contours if min_area <= self.GetRectangleFromContour(cnt).area <= max_area]

        if not contours:
            self.logger.warning("Initialize : Table : No countors by DetectContours : check min_area, max_area, colors")
            return
        #self.ShowContours(contours, frame) # debug <- contours by color, area
        
        contours = self.SelectContoursByRatio(contours, ratio, eps=eps)
        if not contours:
            self.logger.warning("Initialize : Table : No countours by SelectContoursByRatio : check ratio, eps")
            return
        #self.ShowContours(contours, frame) # debug <- contours by ratio

        center_of_the_field = self.field.GetCenter()
        best_dist_to_center = 100000000
        result_contour = None

        for cnt in contours:
            center = self.GetRectangleFromContour(cnt).center
            delta = self.CalculateDistance(center, center_of_the_field)

            if delta < best_dist_to_center:
                best_dist_to_center = delta
                result_contour = cnt

        if best_dist_to_center > 1000:
            self.logger.critical("Initialize : Table : contour center is too far : check contours")
            return


        rect = self.GetRectangleFromContour(result_contour)

        self.table.contour = result_contour
        self.table.top_left_coords = rect.A
        self.table.top_right_coords = rect.B
        self.table.bottom_right_coords = rect.C
        self.table.bottom_left_coords = rect.D

        self.logger.info("Initialize : Table : DONE")

    """ Initialize + Button buttons (in pairs) """
    def UpdatePairButton(self, frame_hsv, color_name_1, color_name_2, frame):
        min_area = 300
        max_area = 500
        kernel = 30

        #  Как близко могут находится соседние кнопки
        max_dist = 70
        min_dist = 20
       
        button_contours_1 = self.DetectContours(frame_hsv, 
                            ((self.buttons[color_name_1].lower_color, self.buttons[color_name_1].higher_color),), 
                            min_area, 
                            max_area, 
                            kernel)

        button_contours_2 = self.DetectContours(frame_hsv, 
                            ((self.buttons[color_name_2].lower_color, self.buttons[color_name_2].higher_color),), 
                            min_area, 
                            max_area, 
                            kernel)

        selected_pair_contours = []


        """ Выбираем только те пары, которые находятся рядом с другом другом """
        for contour_1 in button_contours_1:
            center_1 = Rectangle(contour_1).center

            if (not self.field.Contains(center_1)) or (self.red_base.Contains(center_1)) or (self.green_base.Contains(center_1)):
                continue

            for contour_2 in button_contours_2:
                center_2 = Rectangle(contour_2).center

                if (not self.field.Contains(center_2)) or (self.red_base.Contains(center_2)) or (self.green_base.Contains(center_2)):
                    continue

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


    """ Update ValueObjects """
    def UpdateValueObjects(self, index: int, frame_hsv, frame):
        if self.listValueObjects[index].contour is None:
            #self.logger.critical(f"Update : ValueObj : index : is not initialized")
            return

        min_area = 100
        max_area = 500
        kernel = 30

        Object = self.listValueObjects[index]

        contours = self.DetectContours(frame_hsv, ((Object.is_lower_color,
                                                   Object.is_upper_color),), 
                                    min_area,
                                    max_area,
                                    kernel)
       
        if not contours:
            Object.is_visible = False
            Object.contour = None
            self.logger.info(f"Update : ValueObj : {index} : no contours by DetectContours : check colors, min_area, max_area : {self.frame_counter}")
            return
        #self.ShowContours(contours, frame) # <- debug - color, min_area, max_area
        
        """ Delete noises in red_base """
        best_contours = []
        for contour in contours:
            center = Rectangle(contour).center 
            
            if not (self.red_base.Contains(center)):
                best_contours.append(contour)
        #self.ShowContours(best_contours, frame) # <- debug

        """ Select by min delta of distance + reject too big delta """
        min_delta_center = 1500 
        Contour_this_object = None        
       
        for contour in best_contours:
            center = Rectangle(contour).center
            cur_delta = self.CalculateDistance(center, (Object.x, Object.y))
            if min_delta_center > cur_delta:
                min_delta_center = cur_delta
                Contour_this_object = contour
        #self.ShowContour(Contour_this_object, frame) # <- debug
        
        if Contour_this_object is None:
            Object.is_visible = False;
            self.logger.warning(f"Update : ValueObj : {index} : not visible : {self.frame_counter}")
            return

        center = Rectangle(Contour_this_object).center

        new_x = center[0]
        new_y = center[1]
        
        if Object.x is not None:
            Old_x = Object.x
            Old_y = Object.y

            if abs(Old_x - new_x) > Object.max_delta_for_static or abs(Old_y - new_y) > Object.max_delta_for_static:
                Object.is_dynamic = True
                Object.is_grabbed = True
                Object.vector = (new_x - Old_x, new_y - Old_y)
                self.logger.warning(f"Update : ValueObj : {index} : is dynamic : {self.frame_counter}")
            else:
                Object.is_dynamic = False
                Object.is_grabbed = False    
         

        Object.x = new_x
        Object.y = new_y
        Object.contour = Contour_this_object


    """ Rendering elements """
    def ShowButtons(self, frame):
        for color in self.buttons.map:
            button = self.buttons[color]
            contour_color = (0, 0, 0)
            if button.is_good:
                contour_color = (255, 255, 255)
            if button.IsDynamic():
                contour_color = (128, 64, 190)

            if button.contour is not None:
                cv.drawContours(frame, (button.contour,), -1, contour_color, 4)

    def ShowField(self, frame):
        contour_color = (0,255,0)
        if self.field.contour is not None:
            cv.drawContours(frame, (self.field.contour,), -1, contour_color, 4)

    def ShowTable(self, frame):
        if self.table.contour is not None:
            cv.drawContours(frame, (self.table.contour,), -1, (0,255,0), 4) 

    def ShowFrame(self, frame):
        cv.imshow('frame', self.Scale(frame))
        return not (cv.waitKey(10) & 0xFF == ord('q'))

    def ShowBases(self, frame):
        green_base_contour_color = (102,255,70)
        red_base_contour_color = (255,255,102)

        if self.green_base.contour is not None:
            cv.drawContours(frame, (self.green_base.contour,), -1, green_base_contour_color, 4)
        if self.red_base.contour is not None:
            cv.drawContours(frame, (self.red_base.contour,), -1, red_base_contour_color, 4)

    def ShowValueObject(self, frame):
        red_value_object_contour_color = (255,255,255)
        
        if self.listValueObjects[0].contour is not None:
            cv.drawContours(frame, (self.listValueObjects[0].contour,), -1, red_value_object_contour_color,
                        2)

        if self.listValueObjects[1].contour is not None:
            cv.drawContours(frame, (self.listValueObjects[1].contour,), -1, red_value_object_contour_color,
                        2)

    def ShowWalls(self, frame):
        for line in self.walls.lines:
            cv.line(frame, line[0], line[1], (123, 92, 200), 3)

    def ShowBuckets(self, frame):
        contour_color = (0,255,0)

        for bucket in self.listBuckets:
            a, b, c, d = bucket.top_left_coords, bucket.top_right_coords, bucket.bottom_right_coords, bucket.bottom_left_coords
            cv.line(frame, a, b, contour_color, 10)
            cv.line(frame, b, c, contour_color, 10)
            cv.line(frame, c, d, contour_color, 10)
            cv.line(frame, d, a, contour_color, 10)


    def ShowPolygon(self, frame):
        self.ShowField(frame)
        self.ShowButtons(frame)
        self.ShowBases(frame)
        self.ShowValueObject(frame)
        self.ShowWalls(frame)
        self.ShowTable(frame)
        self.ShowBuckets(frame)
        return self.ShowFrame(frame)


    """ Getting frame, already modified """
    def GetFrame(self, capture):
        ret, frame = capture.read()
        if not ret:
            self.logger.critical("Can't receive frame (stream end?). Exiting ...")
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


    """ Iteration logic """
    def MakeIteration(self):
        if not self.capture.isOpened():
            self.logger.critical(f"Make iteration : capture is not opened : {self.frame_counter}")
            return False

        frame = self.GetFrame(self.capture)
        if frame is None:
            self.logger.critical(f"Make iteration : could not get the frame : {self.frame_counter}")
            return False

        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        if self.frame_counter == 1:  
            self.InitializeField(frame_hsv, frame)
            self.ShowField(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.InitializeBases(frame_hsv, frame)
            self.ShowBases(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.InitializeWalls(frame_hsv, frame)
            self.ShowWalls(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.InitializeValueObject(0, frame_hsv, frame)
            self.ShowValueObject(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.InitializeValueObject(1, frame_hsv, frame)
            self.ShowValueObject(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.InitializeBucket(self.green_base, frame_hsv, frame)
            self.InitializeBucket(self.red_base, frame_hsv, frame)
            self.ShowBuckets(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.UpdatePairButton(frame_hsv, 'blue', 'red', frame)
            self.UpdatePairButton(frame_hsv, 'orange', 'green', frame)

            self.InitializeTable(frame_hsv, frame)
            self.ShowTable(frame)
            cv.imshow('frame', self.Scale(frame))
            #cv.waitKey(0)

            self.MakeMapImage(frame)

        self.UpdatePairButton(frame_hsv, 'blue', 'red', frame)
        self.UpdatePairButton(frame_hsv, 'orange', 'green', frame)

        if self.frame_counter % 20 == 0:
            self.UpdatePairButton(frame_hsv, 'blue', 'red', frame)
            self.UpdatePairButton(frame_hsv, 'orange', 'green', frame)

            self.UpdateValueObjects(0, frame_hsv, frame)
            self.UpdateValueObjects(1, frame_hsv, frame)

            self.MakeMapImage(frame)
            self.MakePath((70, 30), (140, 60), 't')


        if not self.ShowPolygon(frame):
            return False

        self.IncreaseFrameCounter()

        return True

    def IncreaseFrameCounter(self):
        self.frame_counter += 1

    def run(self):
        while self.MakeIteration():
            pass
