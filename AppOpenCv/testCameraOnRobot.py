import numpy as np
import cv2 as cv
import logging

from enum import Enum

from numpy._core.defchararray import index


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
        self.top_left_coords = (0, 0)
        self.top_right_coords = (None, None)
        self.bottom_left_coords = (None, None)
        self.bottom_right_coords = (None, None)


class Boarder:
    pass


def Scale(frame, scale_down=0.7):
    return cv.resize(frame, None, fx=scale_down, fy=scale_down, interpolation=cv.INTER_LINEAR)


def init_field_High(frame_hsv, field):
    black = cv.inRange(frame_hsv, np.array([0, 0, 0]), np.array([200,255,100]))
    sens = 40
    white =  cv.inRange(frame_hsv, np.array([0,0,255-sens]), np.array([255,sens,255]))
    return  white | black
    #return cv.drawContours(frame, contours, -1,(0,0,255),3)


def init_field_robot(frame_hsv, field):
    """ Настройка диапозона детекта цветов """

    """ Диапозоны красного """
    lower_red1 = np.array([0, 200, 200])
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([0, 150, 150])
    upper_red2 = np.array([10, 255, 255])
   
    red_mask1 = cv.inRange(frame_hsv, lower_red1, upper_red1)
    red_mask2 = cv.inRange(frame_hsv, lower_red2, upper_red2)
    
    red_mask = red_mask2 
    
    """ Диапозон для синего """
    lower_blue = np.array([100, 200, 200])
    upper_blue = np.array([128, 255, 255])
    
    blue_mask = cv.inRange(frame_hsv, lower_blue, upper_blue)

    """ Диапозоны для зелёного """
    lower_green = np.array([35, 180, 180])
    upper_green = np.array([85, 255, 255])
    
    green_mask = cv.inRange(frame_hsv, lower_green, upper_green)
    
    """ Объединения маски для всех цветов """
    combined_mask = red_mask | blue_mask | green_mask 
    return combined_mask


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

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
    special_values_count = 2

    values = [ValueObj() for _ in range(values_count - special_values_count)]
    special_values = [ValueObj(True) for _ in range(special_values_count)]

    """ Камеры """
    
    """ Камера с робота """
    camera_robot = "http://192.168.2.156:8080/?action=stream"
    capture_robot = cv.VideoCapture(camera_robot)
    
    """ Камера с высоты """
    camera_high = "Right_1.avi"
    capture_high = cv.VideoCapture(camera_high)
    
    listCamers = [capture_high, capture_robot]
    
    logging.debug("Opened Camers")

    c = 1
    """  """
    while capture_high.isOpened() and capture_robot.isOpened():
        """
            HIGH = IndexCamers == 0
            ROBOT = IndexCamers == 1
        """

        """ Получение и проверка кадров с камер """
        for IndexCamer in [0, 1]:

            logging.debug(f"Start {IndexCamer}")

            ret, frame = listCamers[IndexCamer].read()
            if not ret:
                logging.debug(f"Can't receive frame {listCamers[IndexCamer]} Camera (stream end?). Exiting ...")
                break
            
            logging.debug("кадр получен")

            """ RGB -> HSV """
            frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            """ """
            field_img = None
            if IndexCamer == 0:
                logging.debug("field High")
                field_img = init_field_High(frame_hsv, field)
            elif IndexCamer == 1:
                logging.debug("field Robot")
                field_img = init_field_robot(frame_hsv, field)
            
            kernel = np.ones((6,6),np.uint8)

            """ Морфологическая обработка """
            closed = cv.morphologyEx(field_img, cv.MORPH_CLOSE, kernel)  
            
            """ Нахождение контуров объектов """
            contours = cv.findContours(closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

            for cnt in contours:
                rect = cv.minAreaRect(cnt) 
                box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
                ctr = np.array(box).reshape((-1,1,2)).astype(np.int32) # хуй знает
                #Рисую контур - прямоугольник
                cv.drawContours(frame, (ctr,), -1, (0,255,0) , 4) # рисуем прямоугольник

            """ Вывод камер на экран, с рисовкой """ 
            if IndexCamer == 0:
                cv.imshow('HIGH_CAMERA', Scale(frame))
            elif IndexCamer == 1:
                cv.imshow('ROBOT_CAMERA', Scale(frame))

            if cv.waitKey(1) & 0xFF in (ord('q'), ord('й')):
                break

            c += 1

    cv.destroyAllWindows()
"""
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
"""
