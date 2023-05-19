from hospital import Group
from random import sample, randint
from string import ascii_lowercase
from hospital import User
'''Functions to generate data for hospitals/recidents algorithm'''

def generate_groups(n: int):
    '''generates groups with a running id number starting from 0
    Name is id
    Returns a list of Group objects'''
    groups = []
    for i in range(n):
        groups.append(Group(i, i))
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
    students = []
    for i in range(n):
        students.append(User(i, generate_random_name(), randomize_groups(groups)))
    return students