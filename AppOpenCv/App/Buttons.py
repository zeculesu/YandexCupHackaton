import Object
import Button

import numpy as np

class Buttons(Object.Obj):
    def __init__(self, colors_map: dict[str, tuple[np.array, 2]]):
        self.b_green:  Button = Button.Button('green', colors_map['green'][0], colors_map['green'][1])
        self.b_orange: Button = Button.Button('orange', colors_map['orange'][0], colors_map['orange'][1])
        self.b_blue:   Button = Button.Button('blue', colors_map['blue'][0], colors_map['blue'][1])
        self.b_red:    Button = Button.Button('red', colors_map['red'][0], colors_map['red'][1])

        self.map = {
            "green": self.b_green,
            "orange": self.b_orange,
            "blue": self.b_blue,
            "red": self.b_red,
        }

    def __getitem__(self, color_name: str) -> Button.Button:
        return self.map[color_name]


