from entities.group import Group
from entities.user import User
from random import sample, randint
from string import ascii_lowercase

'''Functions to generate data for hospitals/recidents algorithm'''

def generate_groups(n: int):
    '''generates groups with a running id number starting from 0
    Name is id
    Returns a list of Group objects'''
    groups = []
    for i in range(n):
        groups.append(Group(i, i,5))
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
