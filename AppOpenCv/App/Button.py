import Object 

import numpy as np


class Button(Object.Obj):
    def __init__(self, color_name: str, lower_color: np.array, higher_color: np.array):
        super().__init__()
        self.is_pushed:    bool = False
        self.is_good:      bool = False
        self.color_name:   str = color_name
        self.lower_color:  np.array = lower_color  # in HSV
        self.higher_color: np.array = higher_color

        # Calibrate
        self.max_delta_for_static = 10

    def SetVector(self, x, y):
        self.vector = (x, y)
        if (x**2 + y**2)*0.5 > self.max_delta_for_static:
            self.is_dynamic += 1
        else:
            self.is_dynamic = 0
