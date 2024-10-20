import numpy as np
import cv2 as cv

from enum import Enum

class Obj:
    def __init__(self):
        self.is_visible: bool = False
        self.x:          int = None
        self.y:          int = None
        self.is_dynamic: bool = False
        self.vector:     list[int] = [None, None]

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

def Scale(frame, scale_down=0.7):
    return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)

def GetWhiteAndBlack(frame_hsv):
    black = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([200,255,100]))
    sensity = 40  # ну так работает 
    white = cv.inRange(frame_hsv, np.array([0,0,255-sensity]), np.array([255,sensity,255]))
    return  white | black

def GetFieldCountor(contours):
    max_area = -1
    max_box = None
    
    for cnt in contours:
        rect = cv.minAreaRect(cnt) 
        area = int(rect[1][0] * rect[1][1])
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
                
        if area > max_area:
            max_area = area
            max_box = box

    return np.array(max_box).reshape((-1,1,2)).astype(np.int32) 

def InitializeField(frame, field):
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    field_img = GetWhiteAndBlack(frame_hsv)
    closing = cv.morphologyEx(field_img, cv.MORPH_CLOSE, np.ones((10,10),np.uint8))  # делает линию сплошной
    contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    
    field.contour = field_contour = GetFieldCountor(contours)

    min_x = int(field_contour[:, :, 0:1].min())
    max_x = int(field_contour[:, :, 0:1].max())
    min_y = int(field_contour[:, :, 1:2].min())
    max_y = int(field_contour[:, :, 1:2].max())

    field.top_left_coords = (min_x, min_y)
    field.bottom_right_coords = (max_x, max_y)
    field.top_right_coords = (max_x, min_y)
    field.bottom_left_coords = (min_x, max_y)




def main():
    colors_map = {
        "green": (np.array([78,158,124]), np.array([138,255,255])),
        "blue": (np.array([90,158,124]), np.array([138,255,255])),
        "red": (np.array([0, 100, 20]), np.array([10, 255, 255])),
        "orange": (np.array([0, 100, 45]), np.array([225, 250, 255])),
    }

    buttons = Buttons(colors_map)
    field = Field()
    enemy_robot = Robot()
    our_robot = Robot()

    values_count = 3
    special_values_count = 1

    values = [ValueObj() for _ in range(values_count - special_values_count)]
    special_values = [ValueObj(True) for _ in range(special_values_count)]

    video_name = "Left_1.avi"
    capture = cv.VideoCapture(video_name)
    frame_counter = 1


    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if frame_counter == 1:
            InitializeField(frame, field)
            
        cv.drawContours(frame, (field.contour,), -1, (0,255,0) , 4) # рисуем прямоугольник
        cv.imshow('frame', Scale(frame))

        if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
            break
    
        frame_counter += 1
        

 
main()




while False:
    # Получаю изображение
    

    # Кастаю в хсв
    

    #Скейлю изначальное изображение
    frame_scaled = Scale(frame)

    # Оставляю только нужный цвет
    blue_mask = Scale(cv.inRange(frame_hsv, low_blue, high_blue))

    # Размножаю белые точки, чтоб лучше определять роботов
    kernel = np.ones((30,30),np.uint8)
    closing = cv.morphologyEx(blue_mask, cv.MORPH_CLOSE, kernel)

    # Нахожу контуры
    contours = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    
    areas = []
    # Для каждого контура
    for cnt in contours:

        # Вписываю в прямоугольник
        rect = cv.minAreaRect(cnt) 
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        ctr = np.array(box).reshape((-1,1,2)).astype(np.int32) # хуй знает

        center = (int(rect[0][0]),int(rect[0][1]))
        area = int(rect[1][0]*rect[1][1])

        # Настройки текста
        font = cv.FONT_HERSHEY_SIMPLEX
        org = center
        fontScale = 1
        color_red = (0, 255, 0)
        color_interesting = (255, 0, 255)
        thickness = 2

        if area < 300:
            frame_scaled = cv.putText(frame_scaled, 'B', org, font, 
                   fontScale, color_red, thickness, cv.LINE_AA)
        else:
            frame_scaled = cv.putText(frame_scaled, 'R', org, font, 
                   fontScale, color_interesting, thickness, cv.LINE_AA)

        # Рисую контур - прямоугольник
        cv.drawContours(frame_scaled, (ctr,), -1, (0,255,0) , 4) # рисуем прямоугольник
        areas.append(area)

    print(tuple(sorted(areas)))

    # Показываю картинку
    cv.imshow('frame', frame_scaled)

    if (tuple(sorted(areas))[-1] < 3000):
        cv.imwrite("C:\\Aram\\UrFU\\FromVideo\\screen.png", frame_scaled)
        break


    if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
        break
    

    c += 1





