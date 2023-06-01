from random import shuffle
from entities.output_data import Output_data
from tools.piechart import pie
import datetime
import time

class Hospital:
    def __init__(self, input_data):
        self.groups_dict = input_data.groups_dict
        self.students_dict = input_data.students_dict
        self.max_selections = input_data.max_selections
        self.max_group_size = input_data.max_group_size

    def group_prio(self, students):
        '''For the input list students, the function ranks students for each group based on the rankings of selections.'''
        for i in range(self.max_selections):
            for student_id in students:
                student = self.students_dict[student_id]
                if i < len(student.selections):
                    group_id = student.selections[i]
                    group = self.groups_dict[group_id]
                    group.prio.append(student_id)

    def hospital_algo(self):
        '''Sorting algorithm based on the hospital-residents problem'''
        start = time.time()
        students = []
        for student_id in self.students_dict.keys():
            students.append(student_id)
        
        shuffle(students)
        # The list matched is indexed in the same order as the students in the students list. 
        matched = [False for i in range(len(students))]

        # Form prio for each group based on the selections of the students 
        self.group_prio(students)

        # Continue until all students have been matched. 
        while False in matched:
            for i, student_id in enumerate(students):
                student = self.students_dict[student_id]
                if not student.selections or matched[i]: continue
                #print(f"inspecting student: {s.name}")
                # Pick the students best possible group.
                best_group_id = student.selections[0]
                best_group = self.groups_dict[best_group_id]
                group_participants = best_group.participants
                
                # Add the student to the group
                if not student_id in group_participants:
                    group_participants.append((student_id))
                    #print(f"added {s.name} to Group{best_group.name}")
                    matched[i] = True
                
                # If the group is over-subscribed, kick the worst candidate out.
                if len(group_participants) > self.max_group_size:
                    worst_id = best_group.get_worst_student()
                    worst = self.students_dict[worst_id]
                    worst.remove_first_selection()
                    group_participants.remove(worst_id)
                    #print(f"removed {worst.name} from Group{best_group.name}")
                    
                    # Update prio for the next best group.
                    worst_students_next_group_id = worst.selections[0]
                    worst_students_next_group = self.groups_dict[worst_students_next_group_id]
                    worst_students_next_group.priobump(worst_id)

                    worst_index = students.index(worst_id)
                    matched[worst_index] = False
                    
        # Print out the group selections.
        #print()
        overall_happiness = 0
        for g in self.groups_dict:
            #print(f"Group name: Group{groups_dict[g].name}, Group happiness: {groups_dict[g].get_average_happiness(students_dict)}")
            for student_id in self.groups_dict[g].participants:
                student = self.students_dict[student_id]
                overall_happiness += student.happiness
                #print(f"Student name: {student.name}, got his/her {student.happiness}. choice")
            #print()
        #print()
        #print(f"The average happiness of all people is {overall_happiness / len(students)}")

        avg_happiness = overall_happiness / len(students)
        end = time.time()
        total_time = (end - start)

        #Get data of 
        happiness_counter = [0 for i in range(self.max_selections + 1)]
        for s in self.students_dict:
            happiness_counter[self.students_dict[s].happiness] += 1
        happiness_data = []
        for i, h in enumerate(happiness_counter):
            if h != 0:
                happiness_data.append(f"{i}. choice: {h}")

        selections = []
        for g in self.groups_dict:
            group_participants = self.groups_dict[g].participants
            group_name = self.groups_dict[g].name
            for s_id in group_participants:
                student = self.students_dict[s_id]
                selections.append([student.name, s_id, group_name])

        data = Output_data(selections, total_time, avg_happiness, happiness_data)

        #pie(len(self.students_dict), len(self.groups_dict), self.max_selections, self.students_dict)
        return data
