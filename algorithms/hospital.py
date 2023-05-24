from tools import hospital_data_gen, piechart

group_n = 50
student_n = 1000
max_group_size = 20
max_selections = 10

def group_prio(students):
    # Make this work with n selections Currently only accepts the size of groups. Doesn't take into account
    # different amount of choices between users.
    # fix infinite loop caused by the list matched (shuffled students not in sync with it)
    for i in range(max_selections):
        for s in students:
            group = s.selections[i]
            group.prio.append(s)

def hospital_algo():
    groups = hospital_data_gen.generate_groups(group_n)

    students = hospital_data_gen.generate_students(student_n, groups)
    '''students = []
    for i in range(student_n):
        s = User(i, "user" + str(i), [])
        for g in groups:
            s.selections.append(g)
        students.append(s)'''
            

    matched = [False for i in range(len(students))]

    # Form prio for each group based on the selections of the students 
    group_prio(students)

    # Continue until all students have been matched. 
    while False in matched:
        for i, s in enumerate(students):
            if not s.selections or matched[i]: continue
            # Pick the students best possible group.
            #print(f"inspecting student: {s.name}")
            best_group = s.selections[0]
            group_participants = best_group.participants
            prio = best_group.prio
            
            # Add the student to the group
            if not s in group_participants:
                group_participants.append((s))
                #print(f"added {s.name} to Group{best_group.name}")
                matched[i] = True
            
            # If the group is over-subscribed, kick the worst candidate out.
            if len(group_participants) > max_group_size:
                worst = best_group.get_worst_student(prio)
                worst.remove_first_selection()
                group_participants.remove(worst)
                #print(f"removed {worst.name} from Group{best_group.name}")
                
                # Update prio for the next best group of the worst candidate.
                worst_students_next_group = worst.selections[0]
                worst_students_next_group.priobump(worst)

                matched[worst.id] = False
                print()
                

    # Print out the group selections.
    print()
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