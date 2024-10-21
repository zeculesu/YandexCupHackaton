class Field:
    def __init__(self):
        self.top_left_coords = (None, None)
        self.top_right_coords = (None, None)
        self.bottom_left_coords = (None, None)
        self.bottom_right_coords = (None, None)
        self.contour = None

    def Contains(self, center):
        x, y = center

        return ((self.top_left_coords[0] <= x <= self.top_right_coords[0]) and
               (self.top_left_coords[1] <= y <= self.bottom_left_coords[1]))  

    def GetCenter(self):
        return ((self.top_left_coords[0] + self.bottom_right_coords[0]) // 2,   
                (self.top_left_coords[1] + self.bottom_right_coords[1]) // 2)
