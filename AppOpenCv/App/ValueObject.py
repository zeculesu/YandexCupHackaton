import Object
import numpy as np
import Owner

class ValueObj(Object.Obj):
    def __init__(self, index: int, is_special: bool = False):
        super().__init__()
        self.owner      = Owner.Owner.NOBODY
        self.is_special = False
        self.is_grabbed = False
        self.is_lower_color = np.array(None) 
        self.is_upper_color = np.array(None)
        self.index = index 
        self.max_delta_for_static = 15

    def SetVector(self, x, y):
        self.vector = (x, y)
        if (x**2 + y**2)*0.5 > self.max_delta_for_static:
            self.is_dynamic += 1
        else:
            self.is_dynamic = 0
