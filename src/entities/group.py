class Group:
    def __init__(self, id, name, size, min_size, mandatory=False):
        self.id = id
        self.name = name
        self.participants = []
        self.size = size
        self.min_size = min_size
        self.mandatory = mandatory
