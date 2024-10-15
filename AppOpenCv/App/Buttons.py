import Object
import Button

import numpy as np

class Buttons(Object.Obj):
     def __init__(self, color_name: str, lower_color: np.array, higher_color: np.array):
        super().__init__()
        self.is_pushed:    bool = False
        self.is_good:      bool = False
        self.color_name:   str = color_name
        self.lower_color:  np.array = lower_color  # in HSV
        self.higher_color: np.array = higher_color


     def __getitem__(self, color_name: str) -> Button.Button:
        return self.map[color_name]


