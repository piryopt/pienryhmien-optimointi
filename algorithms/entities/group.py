class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.participants = []
        self.prio = []

    def get_average_happiness(self):
        '''Returns the average happiness of all users of the group'''
        sum = 0
        for p in self.participants:
            sum += p.happiness
        if sum == 0:
            return 0
        return sum / len(self.participants)
    
    def priobump(self, student):
        '''Prio is increased for the next best group selection of the input student'''
        self.prio.remove(student)
        new_prio = [student]
        new_prio.extend(self.prio)
        self.prio = new_prio
        #print(f"Updated {student.name}'s prio in Group {self.name}")

    def get_worst_student(self):
        '''Returns the student with the worst prio in the participants of the group.'''
        prio = list(reversed(self.prio))
        for student in prio:
            if student in self.participants:
                return student