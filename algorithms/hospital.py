from tools import hospital_data_gen, piechart, excelreader
from random import shuffle

group_n = 25
student_n = 500
max_group_size = 20
max_selections = 10
excel = 'Kohtitutkivaatyötapaa.xlsx'

def group_prio(students):
    '''For the input list students, the function ranks students for each group based on the rankings of selections.'''
    for i in range(max_selections):
        for s in students:
            group = s.selections[i]
            group.prio.append(s)

def hospital_algo():
    '''Sorting algorithm based on the hospital-residents problem'''
    groups = hospital_data_gen.generate_groups(group_n)
    #groups = excelreader.create_groups(excel)
    students = hospital_data_gen.generate_students(student_n, groups)
    #students = excelreader.create_users(excel, groups)
    
    shuffle(students)
    matched = [False for i in range(len(students))]
    for s in students:
        matched.append((False, s))

    # Form prio for each group based on the selections of the students 
    group_prio(students)

    # Continue until all students have been matched. 
    while False in matched:
        for i, s in enumerate(students):
            if not s.selections or matched[i]: continue
            #print(f"inspecting student: {s.name}")
            # Pick the students best possible group.
            best_group = s.selections[0]
            group_participants = best_group.participants
            
            # Add the student to the group
            if not s in group_participants:
                group_participants.append((s))
                #print(f"added {s.name} to Group{best_group.name}")
                matched[i] = True
            
            # If the group is over-subscribed, kick the worst candidate out.
            if len(group_participants) > max_group_size:
                worst = best_group.get_worst_student()
                worst.remove_first_selection()
                group_participants.remove(worst)
                #print(f"removed {worst.name} from Group{best_group.name}")
                
                # Update prio for the next best group.
                worst_students_next_group = worst.selections[0]
                worst_students_next_group.priobump(worst)

                worst_index = students.index(worst)
                matched[worst_index] = False
                

    # Print out the group selections.
    #print()
    overall_happiness = 0
    for g in groups:
        #print(f"Group name: Group{g.name}, Group happiness: {g.get_average_happiness()}")
        for p in g.participants:
            overall_happiness += p.happiness
            #print(f"Student name: {p.name}, got his/her {p.happiness}. choice")
        #print()
    #print()
    print(f"The average happiness of all people is {overall_happiness / len(students)}")
    piechart.pie(student_n, group_n, max_selections, students)
    

if __name__=="__main__":
    hospital_algo()