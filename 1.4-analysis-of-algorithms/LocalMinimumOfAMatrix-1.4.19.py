#!/usr/bin/env python3

import random
import pprint

def find_minimum(m, top, left, bottom, right):
    minvalue = float('inf')
    minij = (0, 0)
    midrow = (top + bottom) // 2
    midcol = (left + right) // 2

    for j in range(left, right + 1):
        for i in (top, midrow, bottom):
            if m[i][j] < minvalue:
                minvalue = m[i][j]
                minij = (i, j)

    for i in range(top, bottom + 1):
        for j in (left, midcol, right):
            if m[i][j] < minvalue:
                minvalue = m[i][j]
                minij = (i, j)

    if bottom - top == 2 or right - left == 2:
        return minij
    else:
        i, j = minij
        neighbours = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for l in neighbours:
            if 0 <= l[0] < len(m) and 0 <= l[1] < len(m):
                if m[i][j] > m[l[0]][l[1]]:
                    if l[0] < midrow and l[1] < midcol:
                        return find_minimum(m, top, left, midrow, midcol)
                    elif l[0] > midrow and l[1] < midcol:
                        return find_minimum(m, midrow, left, bottom, midcol)
                    elif l[0] < midrow and l[1] > midcol:
                        return find_minimum(m, top, midcol, midrow, right)
                    else:
                        return find_minimum(m, midrow, midcol, bottom, right)
        return minij

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    for _ in range(20):
        N = random.randint(3, 50)
        m = [[random.randint(0, 100) for _ in range(N)] for _ in range(N)]
        i, j = find_minimum(m, 0, 0, N - 1, N - 1)
        neighbours = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for l in neighbours:
            if 0 <= l[0] < N and 0 <= l[1] < N:
                if m[i][j] > m[l[0]][l[1]]:
                    print(f'wrong at size {N} * {N}!')
                    pp.pprint(m)
                    print(f'function find wrong minimum at {(i, j)}')
                    break


