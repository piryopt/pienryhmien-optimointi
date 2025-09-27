import itertools
import numpy as np
from flask_babel import gettext
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
            weights: dictionary of weights for algorithm, priority number as key

        variables:
            self.groups: dictionary of Group objects, id as key
            self.students: dictionary of Student objects, id as key
            self.index_to_student_dict: dictionary of Student objects with matrix row id as key
            self.weights: dictionary of weights for group order
            self.index_to_group_dict: Maps matrix column to group id
            self.matrix: NxN 2D numpy array where students are represented on rows
            and groups on columns
            self.assigned_groups: dictionary where keys are group ids and values
            are initially empty lists, then lists of student ids assigned to the group
            self.student_happiness: array with columns representing student id and
            the student's personal ranking of the group they were assigned to
        """

        self.groups = groups
        self.students = students
        self.index_to_student_dict = self.map_student_to_index()
        self.weights = weights
        self.index_to_group_dict = self.create_group_dict()
        self.matrix = self.create_matrix()
        self.assigned_groups = {key:[] for key, group in self.groups.items()}
        self.student_happiness = np.zeros((len(self.students),2))
       
    def run(self):
        """
        Calls functions in appropriate order to process matrix to correct form
        for the algorith and to run algorithm
        Measures how long it takes to run the algorithm
        """
        self.reshape_matrix()
        self.profit_matrix_to_cost_matrix()
        self.find_assignment()

    def map_student_to_index(self):
        """
        Takes self.students dictionary of Student objects with id as key
        returns a dictionary of Student ids with keys corresponding to matrix
        row indeces
        """
        ids = [key for key, student in self.students.items()]
        return dict(zip(list(range(len(ids))), ids))

    def create_group_dict(self):
        """
        Creates a dictionary which maps the column indices of the matrix to the group IDs.
        """
        ids = list(itertools.chain.from_iterable([[key]*group.size for key, group in self.groups.items()]))
        return dict(zip(list(range(len(ids))), ids))

    def create_matrix(self):
        """
        Creates a matrix which has spots in the groups as columns and students as
        the rows. Keys for students in the index_to_student_dict match matrix row ids
        Fills the matrix with profit numbers based on student's group preferences.

        If the group is not in student preferences or rejections it is filled with
        default weight that is >0. This is important for cases where not all groups
        are ranked or when a non-group is added to choices (more answers than
        available spaces)
        """
        matrix = []
        mandatory_base_weight = 100000  # Very high base weight for mandatory groups
        mandatory_penalty = 1000        # Penalty for lower ranking
        mandatory_low_weight = 50000    # Lower, but still high, for not ranked/rejected

        # Count how many mandatory spots have been assigned for each group
        group_spot_counter = {group_id: 0 for group_id, group in self.groups.items() if group.mandatory}
        group_spot_indices = {group_id: [] for group_id, group in self.groups.items() if group.mandatory}
        # Build a list of column indices for each mandatory group
        for col_idx, group_id in self.index_to_group_dict.items():
            if self.groups[group_id].mandatory:
                group_spot_indices[group_id].append(col_idx)

        n_students = len(self.students)
        n_spots = len(self.index_to_group_dict)

        # Build the matrix row by row
        for student_idx, (student_id, student) in enumerate(self.students.items()):
            row = []
            for col_idx in range(n_spots):
                group_id = self.index_to_group_dict[col_idx]
                group = self.groups[group_id]
                # If this is a mandatory group
                if group.mandatory:
                    # For the first min_size spots, use high weights
                    mandatory_spots = group_spot_indices[group_id]
                    spot_number = mandatory_spots.index(col_idx)
                    if spot_number < group.min_size:
                        if group_id in student.selections:
                            rank = student.selections.index(group_id)
                            row.append(mandatory_base_weight - rank * mandatory_penalty)
                        elif group_id in student.rejections:
                            row.append(mandatory_low_weight)
                        else:
                            row.append(mandatory_low_weight)
                    else:
                        # After min_size spots, use normal weights
                        if group_id in student.selections:
                            row.append(self.weights[student.selections.index(group_id)])
                        elif group_id in student.rejections:
                            row.append(0)
                        else:
                            row.append(self.weights[-1])
                else:
                    # Non-mandatory group: normal weights
                    if group_id in student.selections:
                        row.append(self.weights[student.selections.index(group_id)])
                    elif group_id in student.rejections:
                        row.append(0)
                    else:
                        row.append(self.weights[-1])
            matrix.append(row)
        return np.array(matrix)

    def reshape_matrix(self):
        """
        Makes the matrix square if necessary by padding with zeroes.
        Padding by adding columns is technically unnescessary as the app should
        check that there are not more students than available spaces 
        """
        rows, cols = np.shape(self.matrix)
        if cols > rows:
            self.matrix = np.pad(self.matrix,[(0,cols-rows),(0,0)],mode="constant", constant_values=self.weights[-1])
        elif cols < rows:
            self.matrix = np.pad(self.matrix,[(0,0),(0,rows-cols)],mode="constant", constant_values=self.weights[-1])

    def profit_matrix_to_cost_matrix(self):
        """
        Creates a cost matrix from the profit matrix by making each number
        negative and then adding the original matrix maximum to each number
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
        Takes assigned column ids to create a dictionary of
        group id's as keys to a list of student id's assigned to
        the group.
        Updates student happiness array where each row represents a student
        and the number of their group preference where 1 is best.
        If student is placed in a group outside of their group preference
        their happiness is set to len(self.weights)-1, which is equal to
        number of possible choices + 1
        Args:
            col_id (list): list of col id's where students assigned
            in order by row id
        """
        for i in range(len(self.students)):
            assigned_group = self.index_to_group_dict[col_id[i]]
            student_id = self.index_to_student_dict[i]
            self.assigned_groups[assigned_group].append(student_id)
            if assigned_group in self.students[student_id].selections:
                happiness = self.students[student_id].selections.index(assigned_group)+1
            else:
                happiness = len(self.weights)-1
            self.student_happiness[i] = [student_id, happiness]

    def get_data(self):
        """
        Returns a collection of data on the group selections
        """
        return self.get_selections_data()

    def get_selections_data(self):
        """
        Summarizes the group selections to a list of lists where each sublist
        is in the form [student name, student ID, group name]
        """
        selections = []
        for group_id in self.assigned_groups:
            for student_id in self.assigned_groups[group_id]:
                email = user_service.get_email(student_id)
                selections.append([[student_id, self.students[student_id].name], email, [group_id, self.groups[group_id].name]])
        return selections

    def get_happiness_data_strings(self):
        """
        Summarizes self.student_happiness to string format
        """
        choice, number = np.unique(self.student_happiness[:,1], return_counts=True)
        happiness_strings = []
        for i in range(len(choice)):
            msg = gettext('valintaansa sijoitetut käyttäjät')
            happiness_strings.append(f"{int(choice[i])}. " + msg + f": {number[i]}")
        return happiness_strings
