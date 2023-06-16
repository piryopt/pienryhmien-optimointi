from matplotlib import pyplot as plt

def pie(student_n, group_n, max_selections, students_dict):
    '''Takes in the amount of students, amount of groups, maximum amount of
    allowed selections and the list of students. Returns a piechart that diplays
    how many students got their n:th choice'''
    happiness_counter = [0 for i in range(max_selections + 1)]
    for student_id in students_dict:
        happiness_counter[students_dict[student_id].happiness] += 1
    labels = []
    data = []
    for i, happiness in enumerate(happiness_counter):
        if happiness != 0:
            labels.append(str(i) + ". choice")
            data.append(happiness_counter[i])
            print(f"{i}. choice: {happiness}")

    plt.figure(figsize =(10, 7))
    plt.pie(data, labels = labels, autopct='%1.1f%%', wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'})
    plt.title(f"Students: {student_n}, groups: {group_n}, student group selections: {max_selections}")

    plt.show()
