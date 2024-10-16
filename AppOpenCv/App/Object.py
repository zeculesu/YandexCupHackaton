class Obj:
    def __init__(self):
        self.is_visible: bool = False
        self.x:          int = None
        self.y:          int = None
        self.is_dynamic: int = 0
        self.vector:     tuple[int] = (0, 0)
        self.contour:    np.array = None

    # CALIBRATE
    def IsDynamic(self):
        return self.is_dynamic > 5
