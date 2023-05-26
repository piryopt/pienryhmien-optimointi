from random import shuffle
from entities.output_data import Output_data
from entities.input_data import Input_data
import datetime

def group_prio(students, students_dict, groups_dict, max_selections):
    '''For the input list students, the function ranks students for each group based on the rankings of selections.'''
    for i in range(max_selections):
        for student_id in students:
            student = students_dict[student_id]
            if i < len(student.selections):
                group_id = student.selections[i]
                group = groups_dict[group_id]
                group.prio.append(student_id)

def hospital_algo(input_data):
    groups_dict = input_data.groups_dict
    students_dict = input_data.students_dict
    max_selections = input_data.max_selections
    max_group_size = input_data.max_group_size

    start = datetime.datetime.now()
    '''Sorting algorithm based on the hospital-residents problem'''
    students = []
    for student_id in students_dict.keys():
        students.append(student_id)
    
    shuffle(students)
    # The list matched is indexed in the same order as the students in the students list. 
    matched = [False for i in range(len(students))]

    # Form prio for each group based on the selections of the students 
    group_prio(students, students_dict, groups_dict, max_selections)

    # Continue until all students have been matched. 
    while False in matched:
        for i, student_id in enumerate(students):
            student = students_dict[student_id]
            if not student.selections or matched[i]: continue
            #print(f"inspecting student: {s.name}")
            # Pick the students best possible group.
            best_group_id = student.selections[0]
            best_group = groups_dict[best_group_id]
            group_participants = best_group.participants
            
            # Add the student to the group
            if not student_id in group_participants:
                group_participants.append((student_id))
                #print(f"added {s.name} to Group{best_group.name}")
                matched[i] = True
            
            # If the group is over-subscribed, kick the worst candidate out.
            if len(group_participants) > max_group_size:
                worst_id = best_group.get_worst_student()
                worst = students_dict[worst_id]
                worst.remove_first_selection()
                group_participants.remove(worst_id)
                #print(f"removed {worst.name} from Group{best_group.name}")
                
                # Update prio for the next best group.
                worst_students_next_group_id = worst.selections[0]
                worst_students_next_group = groups_dict[worst_students_next_group_id]
                worst_students_next_group.priobump(worst_id)

                worst_index = students.index(worst_id)
                matched[worst_index] = False
                

    # Print out the group selections.
    #print()
    overall_happiness = 0
    for g in groups_dict:
        #print(f"Group name: Group{groups_dict[g].name}, Group happiness: {groups_dict[g].get_average_happiness(students_dict)}")
        for student_id in groups_dict[g].participants:
            student = students_dict[student_id]
            overall_happiness += student.happiness
            #print(f"Student name: {student.name}, got his/her {student.happiness}. choice")
        #print()
    #print()
    #print(f"The average happiness of all people is {overall_happiness / len(students)}")
    end = datetime.datetime.now()
    total_time = (end - start)
    avg_happiness = overall_happiness / len(students)
    data = Output_data(groups_dict, total_time, avg_happiness)

    #pie(student_n, group_n, max_selections, students_dict)
    return data
