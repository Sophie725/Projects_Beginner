# Insert data
# Don't use other libararies for this assignment such as numpy or pandas.

def insert_first(l: list, v: int) -> list:
    # This function should insert the value 0 at the beginning of the list l
    # and return the modified list.
    # Fill in the code here
    
    return l

def insert_last(l: list, v: int) -> list:
    # This function should insert the value 0 at the end of the list l
    # and return the modified list.
    # Fill in the code here
    
    return l

def insert_at_index(l: list, v: int, i: int) -> list:
    # This function should insert the value 0 at the index i of the list l
    # and return the modified list.
    # Fill in the code here
    
    return l

def insert_before_value(l: list, v: int, target: int) -> list:
    # This function should insert the value v before the first occurrence of 
    # the target value in the list l and return the modified list.
    # Fill in the code here
    
    return l

def insert_after_value(l: list, v: int, target: int) -> list:
    # This function should insert the value v after the first occurrence of 
    # the target value in the list l and return the modified list.
    # Fill in the code here
    
    return l

def insert_list(l1: list, l2: list, i: int) -> list:
    # This function should insert the list l2 into the list l1 at the index i
    # and return the modified list.
    # Fill in the code here
    
    return l1


def main():
    v = 10
    i = 2
    l1 = [1, 2, 3, 4, 5]
    l2 = [6, 7, 8, 9, 10]
    
    print(insert_fist(l1, v))
    print(insert_last(l1, v))
    print(insert_at_index(l1, v, i))
    print(insert_before_value(l1, v, i))
    print(insert_after_value(l1, v, i))
    print(insert_list(l1, l2, i))

if __name__ == "__main__":
    main()