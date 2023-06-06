class Group:
    def __init__(self, id, name,size):
        self.id = id
        self.name = name
        self.participants = []
        self.prio = []
        self.size = size

    def get_average_happiness(self, students_dict):
        '''Returns the average happiness of all users of the group'''
        sum = 0
        for p in self.participants:
            sum += students_dict[p].happiness
        if sum == 0:
            return 0
        return sum / len(self.participants)
