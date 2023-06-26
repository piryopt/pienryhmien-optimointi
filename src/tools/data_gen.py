from src.entities.group import Group
from src.entities.student import Student
from random import sample, randint
from string import ascii_lowercase

'''Functions to generate data for hospitals/recidents algorithm'''

def generate_groups(n: int, group_size: int):
    '''generates groups with a running id number starting from 0
    Name is id
    Returns a list of Group objects'''
    groups = {}
    for i in range(n):
        groups[i] = Group(i, i, group_size)
    return groups

def randomize_groups(groups):
    '''Randomizes given list (of group objects) and returns list'''
    return sample(groups, len(groups))

def generate_random_name():
    '''generates a random string, length between 3 and 6 digits'''
    return ''.join(sample(ascii_lowercase, randint(3,6)))

def generate_students(n: int, groups):
    '''Generates n students
    Running id number starting from 0
    Random names
    Group preferences randomized from given list of groups'''
    students = {}
    selections = []
    for group_id in groups.keys():
        selections.append(group_id)
    for i in range(n):
        students[i] =  Student(i, f"Opiskelija {i}", sample(selections, len(selections)))
    return students
