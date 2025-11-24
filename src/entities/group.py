class Group:
    def __init__(self, id, name, size, min_size, participation_limit=None, mandatory=False):
        self.id = id
        self.name = name
        self.participants = []
        self.size = size
        self.min_size = min_size
        self.participation_limit = participation_limit
        self.mandatory = mandatory
