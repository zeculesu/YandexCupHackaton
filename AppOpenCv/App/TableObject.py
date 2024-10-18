from Object import Obj
from Owner import Owner

import numpy as np


class TableObj(Obj):
    def __init__(self, is_special: bool = False):
        super().__init__()
        self.is_lower_color = np.array(None) 
        self.is_upper_color = np.array(None)
