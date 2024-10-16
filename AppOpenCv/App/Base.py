from Field import Field
from Owner import Owner

class Base(Field):
    def __init__(self, owner: Owner = Owner.ENEMY):
        super().__init__()
        self.owner = owner