#!/usr/bin/env python3

from collections import deque

def is_valid(l):
    s = deque()
    i = 0
    for out in l:
        while not s or s[-1] != out:
            if i >= len(l):
                return False
            s.append(i)
            i += 1
        s.pop()
    return not s


if __name__ == '__main__':
    l = [0, 1, 2, 3, 4, 5]
    print(f'{l}: {is_valid(l)}')
    l = [1, 2, 3, 0]
    print(f'{l}: {is_valid(l)}')
    l = [2, 5, 6, 7, 4, 8, 9, 3, 1, 0]
    print(f'{l}: {is_valid(l)}')
    l = [4, 6, 8, 7, 5, 3, 2, 9, 0, 1]
    print(f'{l}: {is_valid(l)}')
    l = [3, 0, 1, 2]
    print(f'{l}: {is_valid(l)}')

