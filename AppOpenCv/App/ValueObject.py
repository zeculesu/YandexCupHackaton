import Object
import Owner

class ValueObj(Object.Obj):
    def __init__(self, is_special: bool = False):
        super().__init__()
        self.owner      = Owner.Owner.NOBODY
        self.is_special = False
        self.is_grabbed = False
