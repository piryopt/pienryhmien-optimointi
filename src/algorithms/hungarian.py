import time
import numpy as np
import itertools
from scipy.optimize import linear_sum_assignment
from src.services.user_service import user_service

class Hungarian:

    def __init__(self,groups:dict,students:dict,weights:dict):
        """
        Initiates data structures used in assigning students to groups
        with the hungarian algorithm
        Args:
            groups: dictionary of Group objects, id as key
            students: dictionary of User objects, id as key
            weights: dictionary of weights for group order, priority number as key

        #TODO shuffle students before assignment, keep info so that shuffle is repeatable
        variables:
            self.groups: dictionary of Group objects, id as key
            self.students: dictionary of User objects, matrix row id as key
            self.weights: dictionary of weights for group order
            self.prefs: list of lists, each sublist has a student's list
            of group preferences in order
            self.index_to_group_dict: Maps matrix column to group id
            self.matrix: NxN 2D numpy array where students are represented on rows
            and groups on columns
            self.assigned_groups: dictionary where keys are group ids and values
            are a list of student ids assigned to the group
            self.student_happiness: array with columns representing student id and
            the student's personal ranking of the group they were assigned to
            self.runtime: data on how long it took to run the algorithm
        """

        self.groups = groups
        self.students = students
        self.index_to_student_dict = self.map_student_to_index()
        self.weights = weights
        self.prefs = self.student_preferences()
        self.index_to_group_dict = self.create_group_dict()
        self.matrix = self.create_matrix()
        self.assigned_groups = self.initiate_assigned_groups_dict()
        self.student_happiness = np.zeros((len(self.students),2))
        self.runtime = 0

    def run(self):
        """
        Calls functions in appropriate order to reshape matrix and run algorithm
        Measures how long it takes to run the algorithm
        """
        start = time.time()
        self.reshape_matrix()
        self.profit_matrix_to_cost_matrix()
        self.find_assignment()
        end = time.time()
        self.runtime = end-start 

    def create_group_dict(self):
        """
        Creates a dictionary which maps the column indices of the
        matrix to the group IDs.
        """
        ids = list(itertools.chain.from_iterable([[key]*group.size for key, group in self.groups.items()]))
        return {index:id for (index, id) in zip(list(range(len(ids))), ids)}

    def map_student_to_index(self):
        """
        Takes self.students dictionary of Student objects with id as key
        returns a dictionary of Student objects with keys corresponding to matrix row indeces
        """
        dictionary = {}
        i = 0
        for key, student in self.students.items():
            dictionary[i] = student
            i+=1
        return dictionary

    def create_matrix(self):
        """
        Creates a matrix which has spots in the groups as columns
        and students as the rows. Student key in self.students matches
        the row id due to how the student preferences lists is
        created.
        Fills the matrix with profit numbers based on student's
        group preferences.
        """
        matrix = []
        for student_prefs in self.prefs:
            row = [self.weights[student_prefs.index(v) if v in student_prefs else None] for k,v in self.index_to_group_dict.items()]
            matrix.append(row)

        return np.array(matrix)

    def student_preferences(self):
        """
        Creates a list of lists of group IDs from the student's preferences.
        Students organized by key, which is an id integer starting from 0 and resulting
        preference list is organized in numerical order by key.
        """
        #TODO index_to_student dictionary, in the final product student ID's might not be consecutive numbers
        #in the questionnaire, students might also be shuffled for the algorithm

        prefs = [[group for group in student.selections] for key, student in self.index_to_student_dict.items()]
        return prefs

    def initiate_assigned_groups_dict(self):
        """
        To self.assigned_groups dictionary create an empty list
        for every group key in self.groups
        """
        assigned_groups = {}
        for key, group in self.groups.items():
            assigned_groups[key] = []
        return assigned_groups

    def reshape_matrix(self):
        """
        Makes the matrix square if necessary by padding with zeroes. 
        """
        #TODO if not enough spots for all students and padded with columns,
        # check after assignment who got left out
        #TODO minimum weight (probably =padding number) is not 0, requires
        #changes in the Weights class and tests

        a = np.shape(self.matrix)[0]
        b = np.shape(self.matrix)[1]
        if b > a:
            mat = np.pad(self.matrix,[(0,b-a),(0,0)],mode="constant")
        elif b < a:
            mat = np.pad(self.matrix,[(0,0),(0,a-b)],mode="constant")
        else:
            mat = self.matrix
        self.matrix = mat

    def profit_matrix_to_cost_matrix(self):
        """
        Creates a cost matrix from the profit matrix.
        """
        maximum = np.max(self.matrix)
        self.matrix = self.matrix*-1+maximum

    def find_assignment(self):
        """
        Uses scipy function linear_sum_assignemt to find the assignemt of
        students to groups that incurs minimum cost
        Feeds assigned columns to function col_id_to_group_assignment
        """
        row_id, col_id = linear_sum_assignment(self.matrix)
        self.col_id_to_group_assignment(col_id)

    def col_id_to_group_assignment(self, col_id: list):
        """
        Takes assigned column id to create a dictionary of
        group id's mapped to a list of student id's assigned to
        the group.
        Also creates a table where each row represents a student and
        the number of their group preference where 1 is best.
        Currenty student id = row id, this might change in the future
        Args:
            col_id (list): list of col id's where students assigned
            in order by row id
        """

        for i in range(len(self.prefs)):
            assigned_group = self.index_to_group_dict[col_id[i]]
            self.assigned_groups[assigned_group].append(self.index_to_student_dict[i].id)
            self.student_happiness[i] = [self.index_to_student_dict[i].id, self.prefs[i].index(assigned_group)+1]

    def get_data(self):
        """
        Modifies algorithm data to be ready to Output_data tool and inputs
        data to the tool, returns the resulting data format

        selections: list of lists, inner list has student name, student id
        and the group student was assigned to
        """

        choice, number = np.unique(self.student_happiness[:,1], return_counts=True)
        happiness_data = []
        for i in range(len(choice)):
            happiness_data.append(f"{choice[i]}. valinta: {number[i]}")

        selections = []
        for group in self.assigned_groups:
            for student in self.assigned_groups[group]:
                student_number = user_service.get_student_number(student)
                selections.append([self.students[student].name, student_number, self.groups[group].name])

        return (selections, self.runtime, np.average(self.student_happiness[:,1]), happiness_data)
