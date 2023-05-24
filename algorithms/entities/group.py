class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.participants = []
        self.prio = []

    def get_average_happiness(self):
        sum = 0
        for p in self.participants:
            sum += p.happiness
        if sum == 0:
            return 0
        return sum / len(self.participants)
    
    def priobump(self, student):
        self.prio.remove(student)
        new_prio = [student]
        new_prio.extend(self.prio)
        self.prio = new_prio
        #print(f"Updated {student.name}'s prio in Group{self.name}")

    def get_worst_student(self, prio):
        '''if len(prio) == 0:
            print("FIX THIS ERROR ASAP")
            return
        student = prio[-1]
        if student in self.participants:
            return student
        return self.get_worst_student(prio[:-1])'''
        prio = list(reversed(prio))
        for student in prio:
            if student in self.participants:
                return student