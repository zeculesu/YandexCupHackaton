import numpy as np
import cv2 as cv

from enum import Enum


"""

Current tasks

1) Придумать шаги изменения векторов в количестве итераций
    если делать слишком часто, то дельта всегда будет очень маленькой, нужна хотя бы 1 секунда
    придется добавить это во все обжекты

2) Наложить защиту на кнопки 
    а) Ничего не нашло - оставляем коорды, is_visible = False
    б) Что-то нашло - как поймем что это то, что нам надо ->
        I - Небольшая дельта 
        II - Вне робота 
        Тогда обновляем координаты

3) Подсвечивать определенным образом кнопки, которые надо нажать и не надо нажать

4) Обнаружение робота через его гусеницы - ОНИ ВСЕГДА ПАРАЛЛЕЛЬНЫ, МЕЖДУ НИМИ
КОНСТАНТНОЕ РАССТОЯНИЕ - МОЖНО ВЫСЧИТЫВАТЬ УГОЛ

Если дельта очен очень большая, тогда кнопки пропали из видимости и при этом задетектился робот


"""

def Scale(frame, scale_down=0.7):
    return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)

def CalculateDistance(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

class Obj:
    def __init__(self):
        self.is_visible: bool = False
        self.x:          int = None
        self.y:          int = None
        self.is_dynamic: bool = False
        self.vector:     tuple[int] = (0, 0)
        self.contour:    np.array = None
        self.vector_updating_frequency = 1
        self.max_delta_for_static = 10

    def SetVector(self, x, y):
        self.vector = (x, y)
        if (x**2 + y**2)*0.5 > self.max_delta_for_static:
            self.is_dynamic = True
        else:
            self.is_dynamic = False

class Owner(Enum):
    ENEMY = -1
    NOBODY = 0
    WE = 1

class ValueObj(Obj):
    def __init__(self, is_special: bool = False):
        super().__init__()
        self.owner            = Owner.NOBODY
        self.is_special: bool = False
        self.is_grabbed: bool = False

class Robot(Obj):
    def __init__(self):
        super().__init__()

class Button(Obj):
    def __init__(self, color_name: str, lower_color: np.array, higher_color: np.array):
        super().__init__()
        self.is_pushed:    bool = False
        self.is_good:      bool = False
        self.color_name:   str = color_name
        self.lower_color:  np.array = lower_color  # in HSV
        self.higher_color: np.array = higher_color

class Buttons:
    def __init__(self, colors_map: dict[str, tuple[np.array, 2]]):
        self.b_green:  Button = Button('green', colors_map['green'][0], colors_map['green'][1])
        self.b_orange: Button = Button('orange', colors_map['orange'][0], colors_map['orange'][1])
        self.b_blue:   Button = Button('blue', colors_map['blue'][0], colors_map['blue'][1])
        self.b_red:    Button = Button('red', colors_map['red'][0], colors_map['red'][1])

        self.map = {
            "green": self.b_green,
            "orange": self.b_orange,
            "blue": self.b_blue,
            "red": self.b_red,
        }

    def __getitem__(self, color_name: str) -> Button:
        return self.map[color_name]

class Field:
    def __init__(self):
        self.top_left_coords = (None, None)
        self.top_right_coords = (None, None)
        self.bottom_left_coords = (None, None)
        self.bottom_right_coords = (None, None)
        self.contour = None
        
class Boarder:
    pass

class Rectangle:
    def __init__(self, ctr):
        a, b, c, d = ctr
        vertexes = [a, b, c, d] = a[0], b[0], c[0], d[0]
        self.A = sorted(vertexes, key=lambda t: (t[0], t[1]))[0]
        self.B = sorted(vertexes, key=lambda t: (t[1], -t[0]))[0]
        self.C = sorted(vertexes, key=lambda t: (-t[0], -t[1]))[0]
        self.D = sorted(vertexes, key=lambda t: (-t[1], t[0]))[0]
        self.area = int(CalculateDistance(self.A, self.B) * CalculateDistance(self.B, self.C))
        self.center = (self.A[0] + (self.B[0] - self.A[0]) // 2, 
                       self.A[1] + (self.C[1] - self.B[1]) // 2)

""" Initialize field funcs"""
def GetWhiteAndBlack(frame_hsv):
    black = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([200,255,100]))
    sensity = 40  # ну так работает 
    white = cv.inRange(frame_hsv, np.array([0,0,255-sensity]), np.array([255,sensity,255]))
    return  white | black

def GetFieldCountor(contours):
    max_area = -1
    max_ctr = None
    
    for cnt in contours:
        rect = cv.minAreaRect(cnt) 
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        ctr = np.array(box).reshape((-1,1,2)).astype(np.int32)
        area = Rectangle(ctr).area

        if area > max_area:
            max_area = area
            max_ctr = ctr

    return max_ctr

def InitializeField(frame_hsv, field):
    field_img = GetWhiteAndBlack(frame_hsv)
    closing = cv.morphologyEx(field_img, cv.MORPH_CLOSE, np.ones((10,10),np.uint8))  # делает линию сплошной
    contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    
    field.contour = GetFieldCountor(contours)

    min_x = int(field.contour[:, :, 0:1].min())
    max_x = int(field.contour[:, :, 0:1].max())
    min_y = int(field.contour[:, :, 1:2].min())
    max_y = int(field.contour[:, :, 1:2].max())

    field.top_left_coords = (min_x, min_y)
    field.bottom_right_coords = (max_x, max_y)
    field.top_right_coords = (max_x, min_y)
    field.bottom_left_coords = (min_x, max_y)

""" General functions """
def DetectContours(frame_hsv, lower_color, higher_color, min_area, max_area, kernel):
    objects_frame = cv.inRange(frame_hsv, lower_color, higher_color)
    closing = cv.morphologyEx(objects_frame, cv.MORPH_CLOSE, np.ones((kernel,kernel),np.uint8)) 
    contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    new_contours = []
    for cnt in contours:
        rect = cv.minAreaRect(cnt) 
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        ctr = np.array(box).reshape((-1,1,2)).astype(np.int32)

        area = Rectangle(ctr).area

        if min_area <= area <= max_area:
            new_contours.append(ctr)

    return new_contours

""" Buttons detection (in pairs) """
def DetectPairButton(frame_hsv, buttons, color_name_1, color_name_2, frame):
    min_area = 300
    max_area = 500
    kernel = 30

    b1 = DetectContours(frame_hsv, 
                        buttons[color_name_1].lower_color, 
                        buttons[color_name_1].higher_color, 
                        min_area, 
                        max_area, 
                        kernel)
    b2 = DetectContours(frame_hsv, 
                        buttons[color_name_2].lower_color, 
                        buttons[color_name_2].higher_color, 
                        min_area, 
                        max_area, 
                        kernel)

    max_dist = 70
    min_dist = 20

    qq = []
    pp = []

    t = 0
    for cnt1 in b1:
        center1 = Rectangle(cnt1).center
        for cnt2 in b2:
            center2 = Rectangle(cnt2).center

            if min_dist <= CalculateDistance(center1, center2) <= max_dist:
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
        cv.imshow('frame', Scale(frame))
        cv.waitKey(0)
        print("Too mcuh")


def main():
    button_colors_map = {
        "green": (np.array([50,100,140]), np.array([83,170,240])),  
        "blue": (np.array([90,158,124]), np.array([138,255,255])),
        "red": (np.array([157, 92, 175]), np.array([185, 241, 252])),
        "orange": (np.array([0, 100, 207]), np.array([40, 254, 247])),  
    }

    buttons = Buttons(button_colors_map)

    field = Field()
    enemy_robot = Robot()
    our_robot = Robot()

    values_count = 3
    special_values_count = 1

    values = [ValueObj() for _ in range(values_count - special_values_count)]
    special_values = [ValueObj(True) for _ in range(special_values_count)]

    video_name = "Right_1.avi"
    capture = cv.VideoCapture(video_name)
    frame_counter = 1


    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        if frame_counter == 1:  
            InitializeField(frame_hsv, field)

        DetectPairButton(frame_hsv, buttons, 'blue', 'red', frame)
        DetectPairButton(frame_hsv, buttons, 'orange', 'green', frame)

        cv.drawContours(frame, (field.contour,), -1, (0,255,0) , 4) # рисуем прямоугольник
        cv.imshow('frame', Scale(frame))

        if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
            break
    
        frame_counter += 1
        

if __name__ == '__main__':
    main()




# while False:
#     # Получаю изображение
    

#     # Кастаю в хсв
    

#     #Скейлю изначальное изображение
#     frame_scaled = Scale(frame)

#     # Оставляю только нужный цвет
#     blue_mask = Scale(cv.inRange(frame_hsv, low_blue, high_blue))

#     # Размножаю белые точки, чтоб лучше определять роботов
#     kernel = np.ones((30,30),np.uint8)
#     closing = cv.morphologyEx(blue_mask, cv.MORPH_CLOSE, kernel)

#     # Нахожу контуры
#     contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    
#     areas = []
#     # Для каждого контура
#     for cnt in contours:

#         # Вписываю в прямоугольник
#         rect = cv.minAreaRect(cnt) 
#         box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
#         ctr = np.array(box).reshape((-1,1,2)).astype(np.int32) # хуй знает

#         center = (int(rect[0][0]),int(rect[0][1]))
#         area = area = CalculateRectangleArea(ctr)

#         # Настройки текста
#         font = cv.FONT_HERSHEY_SIMPLEX
#         org = center
#         fontScale = 1
#         color_red = (0, 255, 0)
#         color_interesting = (255, 0, 255)
#         thickness = 2

#         if area < 300:
#             frame_scaled = cv.putText(frame_scaled, 'B', org, font, 
#                    fontScale, color_red, thickness, cv.LINE_AA)
#         else:
#             frame_scaled = cv.putText(frame_scaled, 'R', org, font, 
#                    fontScale, color_interesting, thickness, cv.LINE_AA)

#         # Рисую контур - прямоугольник
#         cv.drawContours(frame_scaled, (ctr,), -1, (0,255,0) , 4) # рисуем прямоугольник
#         areas.append(area)

#     print(tuple(sorted(areas)))

#     # Показываю картинку
#     cv.imshow('frame', frame_scaled)

#     if (tuple(sorted(areas))[-1] < 3000):
#         cv.imwrite("C:\\Aram\\UrFU\\FromVideo\\screen.png", frame_scaled)
#         break


#     if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
#         break
    

#     c += 1




