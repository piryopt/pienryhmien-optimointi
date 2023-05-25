from random import shuffle
import datetime

group_n = 500
student_n = 10000
max_group_size = 20
max_selections = 10
excel = 'Kohtitutkivaatyötapaa.xlsx'

def group_prio(students, students_dict, groups_dict):
    '''For the input list students, the function ranks students for each group based on the rankings of selections.'''
    for i in range(max_selections):
        for student_id in students:
            student = students_dict[student_id]
            group_id = student.selections[i]
            group = groups_dict[group_id]
            group.prio.append(student_id)

def hospital_algo(groups_dict, students_dict):
    start = datetime.datetime.now()
    '''Sorting algorithm based on the hospital-residents problem'''
    #groups_dict = hospital_data_gen.generate_groups(group_n)
    #groups_dict = excelreader.create_groups(excel)
    #students_dict = hospital_data_gen.generate_students(student_n, groups_dict)
    #students_dict = excelreader.create_users(excel, groups_dict)

    students = []
    for student_id in students_dict.keys():
        students.append(student_id)
    
    shuffle(students)
    # The list matched is indexed in the same order as the students in the students list. 
    matched = [False for i in range(len(students))]

    # Form prio for each group based on the selections of the students 
    group_prio(students, students_dict, groups_dict)

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
        #print(f"Group name: Group{g.name}, Group happiness: {g.get_average_happiness()}")
        for student_id in groups_dict[g].participants:
            student = students_dict[student_id]
            overall_happiness += student.happiness
            #print(f"Student name: {p.name}, got his/her {p.happiness}. choice")
        #print()
    #print()
    print(f"The average happiness of all people is {overall_happiness / len(students)}")
    end = datetime.datetime.now()
    print(end - start)
    #piechart.pie(student_n, group_n, max_selections, students_dict)
