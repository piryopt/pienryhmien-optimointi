
class User:
    def __init__(self, id, name, selections):
        self.id = id
        self.name = name
        self.selections = selections
        self.happiness = 1

    def __eq__(self, other):
       return self.id == other.id
    
    ## This might cause problems when we want to inspect the rankings of choices of the user. 
    def remove_first_selection(self):
        new_selections = self.selections
        new_selections.pop(0)
        self.selections = new_selections
        self.happiness += 1
    
class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.participants = []
        self.prio = []

    def get_average_happiness(self):
        sum = 0
        for p in self.participants:
            sum += p.happiness
        return sum / len(self.participants)

def get_best_selection(student):
    for i, x in enumerate(student.selections_removed):
        if not x:
            return i
        
def get_worst_student(group, prio):
    if len(prio) == 0:
        print("FIX THIS ERROR ASAP")
        return
    student = prio[-1]
    if student in group:
        return student
    return get_worst_student(group, prio[:-1])
    ## Leaving this for now if problems arise with the recursive function
    ##prio = list(reversed(prio))
    ##for student in prio:
        ##if student in group:
            ##return student

def group_prio(students):
    ## Make this work with n selections Currently only accepts the size of groups. Doesn't take into account
    ## different amount of choices between users.
    max_selections = 5
    ## fix infinite loop caused by the list matched (shuffled students not in sync with it)
    ##random.shuffle(students)
    for i in range(max_selections):
        for s in students:
            group = s.selections[i]
            group.prio.append(s)

import hospital_data_gen

def main():
    groups = hospital_data_gen.generate_groups(100)

    students = hospital_data_gen.generate_students(1000, groups)

    matched = [False for i in range(len(students))]

    max_group_size = 10

    group_prio(students)

    ## Continue until all students have been matched. 
    while False in matched:
        for i, s in enumerate(students):
            if not s.selections or matched[i]: continue
            print(f"inspecting student: {s.name}")
            ## Pick the students best possible group.
            best_group = s.selections[0]
            group_participants = best_group.participants
            prio = best_group.prio
            
            # Add the student to the group
            if not s in group_participants:
                group_participants.append((s))
                print(f"added {s.name} to {best_group.name}")
                matched[i] = True
            
            ## If the group is over-subscribed, kick the worst candidate out.
            if len(group_participants) > max_group_size:
                worst = get_worst_student(group_participants, prio)
                worst.remove_first_selection()
                group_participants.remove(worst)
                print(f"removed {worst.name} from {best_group.name}")
                matched[worst.id] = False
                print()
                

    ## Print out the group selections.
    print()
    for g in groups:
        print(f"Group name: Group{g.name}, Group happiness: {g.get_average_happiness()}")
        for p in g.participants:
            print(f"Student name: {p.name}, got his/her {p.happiness}. choice")
        print()
    return groups

if __name__=="__main__":
    main()