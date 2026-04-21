# Drop data
# Don't use other libraries for this assignment such as numpy or pandas.

def drop_first(l: list) -> list:
    # This function should drop the first element of the list l 
    # and return the modified list.
    # Fill in the code here
    if l:
        l.pop(0)

    return l

def drop_last(l: list) -> list:
    # This function should drop the last element of the list l
    # and return the modified list.
    # Fill in the code here
    if l:
        l.pop(-1)

    return l

def drop_odd_indices(l: list) -> list:
    # This function should drop all the elements at odd indices from the list l
    # and return the modified list.
    # Fill in the code here
    l = l[::2]

    return l

def drop_even_indices(l: list) -> list:
    # This function should drop all the elements at even indices from the list l
    # and return the modified list.
    # Fill in the code here
    l = l[1::2]

    return l

def drop_value(v: int, l: list) -> list:
    # Fill in the code here
    # Your code should be able to handle errors, 
    # such as v not being in l or l being empty
    if v in l:
        l.remove(v)

    return l

def drop_odd_values(l: list) -> list:
    # This function should drop all the odd numbers from the list l
    # and return the modified list.
    # Fill in the code here
    even_only = []
    for i in range(len(l) - 1, -1, -1):
        if l[i] % 2 == 1:
            l.pop(i)

    return l

def drop_even_values(l: list) -> list:
    # This function should drop all the even numbers from the list l
    # Fill in the code here
    for i in range(len(l) - 1, -1, -1):
        if l[i] % 2 == 0:
            l.pop(i)

    return l

def drop_at(index: int, l: list) -> list:
    # Fill in the code here
    # Your code should be able to handle errors, 
    # such as n being out of range or l being empty
    if index >= 0 and index < len(l):
        del l[index]
    return l

def drop_until(index: int, l: list) -> list:
    # Fill in the code here
    # Your code should be able to handle errors, 
    # such as n being out of range or l being empty
    if index >= 0 and index < len(l):
        del l[0:index]

    return l

def drop_from(index: int, l: list) -> list:
    # Fill in the code here
    # Your code should be able to handle errors, 
    # such as n being out of range or l being empty
    if index >= 0 and index < len(l):
        last_index = len(l)
        del l[index: last_index]

    return l

def drop_range(start: int, end: int, l: list) -> list:
    # Fill in the code here
    # Your code should be able to handle errors, 
    # such as n being out of range or l being empty
    if start >= 0 and end <= len(l) and start < end:
        del l[start:end]

    return l

import random

def main():
    # Practice
    l1 = [2, 1, 4, 3, 6, 5, 7]

    drop_first(l1)
    # drop_last(l1)
    # drop_odd_indices(l1)
    # drop_even_indices(l1)

    # drop_value(4, l1)
    # drop_odd_values(l1)
    # drop_even_values(l1)

    # drop_at(3, l1)
    # drop_until(2, l1)
    # drop_from(2, l1)
    # drop_range(2, 4, l1)

if __name__ == "__main__":
    main()
