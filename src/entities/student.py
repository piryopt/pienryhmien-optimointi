class Student:
    def __init__(self, id, name, selections, rejections, not_available=False):
        self.id = id
        self.name = name
        self.selections = selections
        self.rejections = rejections
        self.not_available = not_available
