from matplotlib import pyplot as plt

def pie(student_n, group_n, max_selections, students):
    happiness_counter = [0 for i in range(max_selections + 1)]
    for i, s in enumerate(students):
        happiness_counter[s.happiness] += 1
    labels = []
    data = []
    for i, h in enumerate(happiness_counter):
        if h != 0:
            labels.append(str(i) + ". choice")
            data.append(happiness_counter[i])
            print(f"{i}. choice: {h}")

    plt.figure(figsize =(10, 7))
    plt.pie(data, labels = labels, autopct='%1.1f%%', wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'})
    plt.title(f"Students: {student_n}, groups: {group_n}, student group selections: {max_selections}")

    plt.show()

