__author__ = 'abhinav'

def contains (l1, l2):
    match = 0
    for elem in l1:
        if l2[match] == elem:
            match += 1
            if match == len(l2):
                return True
        else:
            if match != 0:
                match = 0
    return match == len(l2)


a = [3, 7, 5, 3, 7, 5]
b = [5, 3, 5]
print contains(a, b)
