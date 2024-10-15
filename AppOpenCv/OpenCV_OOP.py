import cv2 as cv
import numpy as np

from art import tprint


class App:
    def __init__(self):
        self.VidCap = VideoCapture('image',"http://192.168.2.156:8080/?action=stream")

    def run(self) -> None:
        """ Run the main event loop """
        
        classes_to_look_for = ['person'] 

        self.VidCap.start_video_object_detection(classes_to_look_for)


class Classe_For_Look:
    def __init__(self):
        with open("../Yolo/Resources/coco.names.txt") as file:
            self.classes = file.read().split('\n')
   

    def GetClasses(self):
        return self.classes


class Yolo:
    def __init__(self, Objects_for_look):
        # Loading YOLO scales from files and setting up the network
        self.Objects_for_look = Objects_for_look
        self.ClassesObject = Classe_For_Look()

        self.net = cv.dnn.readNetFromDarknet("../Yolo/Resources/yolov4-tiny.cfg",
                                     "../Yolo/Resources/yolov4-tiny.weights")
        self.layer_names = self.net.getLayerNames()
        self.out_layers_indexes = self.net.getUnconnectedOutLayers()
        self.out_layers = [self.layer_names[index - 1] for index in self.out_layers_indexes]


    def draw_object_bounding_box(self, image_to_process, index, box):
        """
        Drawing object borders with captions
        :param image_to_process: original image
        :param index: index of object class defined with YOLO
        :param box: coordinates of the area around the object
        :return: image with marked objects
        """

        x, y, w, h = box
        start = (x, y)
        end = (x + w, y + h)
        color = (0, 255, 0)
        width = 2
        final_image = cv.rectangle(image_to_process, start, end, color, width)

        start = (x, y - 10)
        font_size = 1
        font = cv.FONT_HERSHEY_SIMPLEX
        width = 2
        text = self.ClassesObject.GetClasses()[index]
        final_image = cv.putText(final_image, text, start, font,
                              font_size, color, width, cv.LINE_AA)

        return final_image


    def apply_yolo_object_detection(self, image_to_process):
        """
        Recognition and determination of the coordinates of objects on the image
        :param image_to_process: original image
        :return: image with marked objects and captions to them
        """
    
        height, width, _ = image_to_process.shape
        blob = cv.dnn.blobFromImage(image_to_process, 1 / 255, (608, 608), (0, 0, 0), swapRB=True, crop=False) 
        
        self.net.setInput(blob)
        outs = self.net.forward(self.out_layers)
        class_indexes, class_scores, boxes = ([] for i in range(3))
        objects_count = 0

        for out in outs:
            for obj in out:
                scores = obj[5:]
                class_index = np.argmax(scores)
                class_score = scores[class_index]
                if class_score > 0:
                    center_x = int(obj[0] * width)
                    center_y = int(obj[1] * height)
                    obj_width = int(obj[2] * width)
                    obj_height = int(obj[3] * height)
                    box = [center_x - obj_width // 2, center_y - obj_height // 2, obj_width, obj_height]
                    boxes.append(box)
                    class_indexes.append(class_index)
                    class_scores.append(float(class_score))
        
        # Selection
        chosen_boxes = cv.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)
        for box_index in chosen_boxes:
            box_index = box_index
            box = boxes[box_index]
            class_index = class_indexes[box_index]

            # For debugging, we draw objects included in the desired classes
            if self.ClassesObject.GetClasses()[class_index] in self.Objects_for_look:
                objects_count += 1
                image_to_process = self.draw_object_bounding_box(image_to_process, class_index, box)
    
        final_image = image_to_process 
        return final_image


class VideoCapture:
    def __init__ (self, name, index):
        """ Create Video Connect in camera """
        
        self.name = name
        self.IndexCamera = index 

    """
    def start_video_object_detection(self, Objects_for_look) -> None:
        """
        Real-time video capture and analysis
        """
                
        self.YoloFrame = Yolo(Objects_for_look) 

        while True:
            try:
                video_camera_capture = cv.VideoCapture(self.IndexCamera) 
                
                while video_camera_capture.isOpened():
                    ret, frame = video_camera_capture.read()
                    
                    if not ret:
                        print('Не удалось получить кадр')
                        break

                    frame = self.YoloFrame.apply_yolo_object_detection(frame)
                    frame = cv.resize(frame, (1920 // 2, 1080 // 2))

                    cv.imshow("Video Capture", frame)
                    
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break;

                video_camera_capture.release()
                cv.waitKey(0)
                cv.destroyAllWindows()

            except KeyboardInterrupt:
                pass 
    """

if __name__ == '__main__':
    App().run()
