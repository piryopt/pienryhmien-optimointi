import numpy as np
from entities.group import Group
from entities.user import User
import tools.hospital_data_gen as h
from scipy.optimize import linear_sum_assignment

WEIGHTS = {0:100,
           1:75,
           2:50,
           3:25,
           4:10,
           5:0,
           6:0,
           7:0,
           8:0,
           9:0,
           None: 0
           }


class Hungarian:

    def __init__(self,groups,students):
        self.groups = groups
        self.students = students
        self.index_to_group_dict = {}
        self.matrix = []
        self.prefs = self.student_preferences()

    def create_group_dict(self):
        """
        Creates a dictionary which maps the column indices of the
        matrix to the group IDs.
        """
        group_sizes = [group.size for key,group in self.groups.items()]
        total = 0
        for i in range(len(group_sizes)):
            for j in range(group_sizes[i]):
                self.index_to_group_dict[total+j] = i
            total += group_sizes[i]

    def create_matrix(self):
        """
        Creates a matrix which has spots in the groups as columns
        and students as the rows. Fills the matrix based on student's
        group preferences.
        """
        
        for student_prefs in self.prefs:
            row = [WEIGHTS[student_prefs.index(v) if v in student_prefs else None] for k,v in self.index_to_group_dict.items()]
            self.matrix.append(row)

        self.matrix = np.matrix(self.matrix)

    def student_preferences(self):
        """
        Creates a list of lists of group IDs from the student's preferences.
        """
        prefs = [[group.id for group in student.selections] for key, student in self.students.items()]
        return prefs

    def reshape_matrix(self):
        """
        Makes the matrix square if necessary by padding with zeroes. 
        """
        a = np.shape(self.matrix)[0]
        b = np.shape(self.matrix)[1]
        if b > a:
            mat = np.pad(self.matrix,[(0,b-a),(0,0)],mode="constant")
        elif b < a:
            mat = np.pad(self.matrix,[(0,0),(0,a-b)],mode="constant")
        else:
            mat = self.matrix
        self.matrix = mat

    def profit_matrix_to_nonnegative_cost_matrix(self):
        """
        Creates a cost matrix from the profit matrix.
        """
        maximum = np.max(self.matrix)
        self.matrix = self.matrix*-1+maximum

    def find_assignment(self):
        """
        Uses scipy function linear_sum_assignemt to find the assignemt of
        students to groups that incurs minimum cost
        """
        row_id, col_id = linear_sum_assignment(self.matrix)
