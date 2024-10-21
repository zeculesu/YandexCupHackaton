import cv2
from ultralytics import YOLO


class AI:
    def __init__(self):
        self.model_path = "C:/Users/UrFU/Desktop/Yandex.StudCamp/RobotCamera.pt"
        self.model = YOLO(self.model_path)

    def live_ai(self, frame):
        results = self.model(frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                class_id_tensor = box.cls[0]
                class_id = int(class_id_tensor.cpu().detach().item())

                class_names = self.model.names  # {id: "class_name"}
                class_name = class_names.get(class_id, "Unknown")

                print(f'Box (x1, y1, x2, y2): ({x1}, {y1}, {x2}, {y2}), Center: ({center_x}, {center_y}), Class ID: [{class_id}], Class Name: [{class_name}]')

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            cv2.imshow('RobotCamera', frame)
            cv2.waitKey(1)
