import random

class User:
    def __init__(self, id, name, selections):
        self.id = id
        self.name = name
        self.selections = selections

    def __eq__(self, other):
       return self.id == other.id
    
    def remove_first_selection(self):
        new_selections = self.selections
        new_selections.pop(0)
        self.selections = new_selections
    

class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.participants = []
        self.prio = []

def get_best_selection(student):
    for i, x in enumerate(student.selections_removed):
        if not x:
            return i
        
def get_worst_student(group, prio):
    if len(prio) == 0:
        print("FIX THIS ERROR ASAP")
        return
    ##if prio[-1] in group:
        ##print("FOUND IT")
        ##return prio[-1]
    ##get_worst_student(group, prio[:-1])
    prio = list(reversed(prio))
    for student in prio:
        if student in group:
            return student

def group_prio(students, groups):
    ## make this work with n selections
    max_selections = 3
    ## fix infinite loop caused by the list matched (shuffled students not in sync with it)
    ##random.shuffle(students)
    for i in range(max_selections):
        for s in students:
            group = s.selections[i]
            group.prio.append(s)

def main():
    group0 = Group(0, "group0")
    group1 = Group(1, "group1")
    group2 = Group(2, "group2")

    groups = [group0, group1, group2]

    student0 = User(0, "carl", [group2,group1,group0])
    student1 = User(1, "bob", [group1,group2,group0])
    student2 = User(2, "tom", [group2,group1,group0])
    student3 = User(3, "sarah", [group0,group2,group1])
    student4 = User(4, "james", [group2,group0,group1])
    student5 = User(5, "jessica", [group2,group1,group0])
    student6 = User(6, "timo", [group2,group0,group1])
    student7 = User(7, "aino", [group2,group1,group0])
    student8 = User(8, "anssi", [group1,group2,group0])
    student9 = User(9, "inka", [group1,group0,group2])
    student10 = User(10, "elina", [group0,group1,group2])
    student11 = User(11, "matti", [group0,group2,group1])

    students = [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9, student10, student11]

    matched = [False, False, False, False, False, False, False, False, False, False, False, False]

    max_group_size = 4

    group_prio(students, groups)

    while False in matched:
        for i, s in enumerate(students):
            if not s.selections or matched[i]: continue
            print(f"inspecting student: {s.name}")
            best_group = s.selections[0]
            group_participants = best_group.participants
            ##selection_number = get_best_selection(s)
            ##g = s.selections[selection_number]
            ##group = groups[g].participants
            prio = best_group.prio
            
            if not s in group_participants:
                group_participants.append((s))
                print(f"added {s.name} to {best_group.name}")
                matched[i] = True

            if len(group_participants) > max_group_size:
                worst = get_worst_student(group_participants, prio)
                worst.remove_first_selection()
                group_participants.remove(worst)
                print(f"removed {worst.name} from {best_group.name}")
                matched[worst.id] = False
                print()
                

    print()
    for g in groups:
        print(f"Group name: {g.name}")
        for p in g.participants:
            print(f"Student name: {p.name}")
        print()

if __name__=="__main__":
    main()