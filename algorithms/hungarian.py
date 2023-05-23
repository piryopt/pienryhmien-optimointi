import numpy as np
from entities.group import Group
from entities.user import User
import hospital_data_gen as h

groups = h.generate_groups(3)
students = h.generate_students(12,groups)

WEIGHTS = {0:100,
           1:75,
           2:50,
           3:25,
           4:10,
           5:0,
           6:0,
           7:0,
           8:0,
           9:0
           }


class Hungarian:

    def __init__(self,groups,students):
        self.groups = groups
        self.students = students
        self.index_to_group_dict = {}
        self.matrix = []
        self.prefs = self.student_preferences()

    def create_matrix(self):
        group_sizes = [group.size for group in self.groups]
        total = 0
        for i in range(len(group_sizes)):
            for j in range(group_sizes[i]):
                self.index_to_group_dict[total+j] = i
            total += group_sizes[i]
        
        for student_prefs in self.prefs:
            row = [WEIGHTS[student_prefs.index(v)] for k,v in self.index_to_group_dict.items()]
            self.matrix.append(row)

        self.matrix = np.matrix(self.matrix)

    def student_preferences(self):
        prefs = [[group.id for group in student.selections] for student in self.students]
        return prefs

    def reshape_matrix(self,matrix):
        a = np.shape(matrix)[0]
        b = np.shape(matrix)[1]
        if b > a:
            mat = np.pad(matrix,[(0,b-a),(0,0)],mode="constant")
        elif b < a:
            mat = np.pad(matrix,[(0,0),(0,a-b)],mode="constant")
        else:
            mat = matrix
        return mat
        

#print(profit_matrix)
#cost_matrix = 100 - reshape_matrix(profit_matrix)
#print(cost_matrix)


s = Hungarian(groups,students)
s.create_matrix()
s.reshape_matrix(s.matrix)
print(s.reshape_matrix(s.matrix))


