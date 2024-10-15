import Object 

import numpy as np


class Button(Object.Obj):
    def __init__(self, color_name: str, lower_color: np.array, higher_color: np.array):
        super().__init__()
        self.is_pushed:     bool = False
        self.is_good:       bool = False
        self.color_name:    str = color_name
        self.lower_color:   np.array = lower_color
        self.higher_color:  np.array = higher_color
