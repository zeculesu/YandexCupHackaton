import cv2 as cv
from ultralytics import YOLO
import move_n_grab_algo
from sender import Sender
import torch
torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False

class AI:
    def __init__(self):
        self.model_path = "/Users/macbookpro/Yandex.Disk.localized/best1.pt"
        self.model = YOLO(self.model_path)
        self.sender = Sender("192.168.2.156", 4141)
        self.sender.try_connection()

    def live_ai(self, frame, scenario):
        results = self.model(frame)
        commands = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id_tensor = box.cls[0]
                class_id = int(class_id_tensor.cpu().detach().item())

                class_names = self.model.names  # {id: "class_name"}
                class_name = class_names.get(class_id, "Unknown")



                if scenario == 0 and class_id in [2, 3]:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.putText(frame, class_name, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)



                    commands = move_n_grab_algo.push_button(center_x, center_y)
        cv.imshow('Live AI', frame)
        cv.waitKey(1)

        for command in commands:
            self.sender.send_command(command)

                # Вывод координат всех вершин прямоугольника
                # print(f'Box (x1, y1, x2, y2): ({x1}, {y1}, {x2}, {y2}), '
                #       f'Vertices: (Top-Left: ({x1}, {y1}), Top-Right: ({x2}, {y1}), '
                #       f'Bottom-Left: ({x1}, {y2}), Bottom-Right: ({x2}, {y2})), '
                #       f'Center: ({center_x}, {center_y}), Class ID: [{class_id}], Class Name: [{class_name}]')



