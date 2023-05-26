from hospital import hospital_algo

class SolutionChecker:

    def __init__(self,groups):
        self.student_lists = [group.participants for group in groups]
        self.students = [student for student_list in self.student_lists for student in student_list]
        self.tally = {}

    def create_tally(self):
        for student in self.students:
            if student.happiness not in self.tally.keys():
                self.tally[student.happiness] = 1
            else:
                self.tally[student.happiness] += 1

    def print_tally(self):
        for i, j in sorted(self.tally.items()):
            print(i,j)


def multiple_runs(n):
    master_tally = {}
    for i in range(n):
        s = SolutionChecker(hospital_algo())
        s.create_tally()
        tally = s.tally
        for k,v in tally.items():
            if k in master_tally.keys():
                master_tally[k] += tally[k]
            else:
                master_tally[k] = tally[k]
    
    for i,j in sorted(master_tally.items()):
        print(i,j/n)
