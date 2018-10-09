#!/usr/bin/env python3

class IndexMinPQ:
    def __init__(self, N):
        self._MAXN = N
        self._keys = [-1] * N   # here means element's values
        self._pq = [-1] * N     # index: 0-indexed heap position
                                # value: index of _keys, i.e., _keys[_pq[i]]
        self._qp = [-1] * N     # _qp[j] = i means _pq[i] = j
        self._size = 0          # N in textbook

    def debug(self):
        print(self._keys)
        for i, v in enumerate(self._pq):
            if v == -1:
                continue
            if self._qp[v] != i:
                print('_pq and _qp illegal! \n_pq:')
                print(self._pq)
                print('_qp:')
                print(self._qp)
                return
        print('pass _pq and _qp check')
        for i in self._pq:
            print(self._keys[i])

    def contains(self, i):
        return self._qp[i] != -1

    def insert(self, i, key):
        if self.contains(i):
            raise ValueError('index is used')
            return
        self._keys[i] = key
        self._pq[self._size] = i
        self._qp[i] = self._size
        self._size += 1
        self._swim(0, self._size - 1)

    def _swim(self, startpos, pos):
        'based on _siftdown in heapq from cpython'
        newitem = self._pq[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parentitem = self._pq[parentpos]
            if self._keys[newitem] < self._keys[parentitem]:
                self._pq[pos] = parentitem
                self._qp[parentitem] = pos
                pos = parentpos
                continue
            break
        self._pq[pos] = newitem
        self._qp[newitem] = pos

    def _sink(self, pos):
        'based on _siftup in heapq from cpython'
        endpos = self._size
        startpos = pos
        newitem = self._pq[pos]
        childpos = 2 * pos + 1
        while childpos < endpos:
            rightpos = childpos + 1
            rightitem = self._pq[rightpos]
            childitem = self._pq[childpos]
            if rightpos < endpos and not self._keys[childitem] < self._keys[rightitem]:
                childpos = rightpos
            self._pq[pos] = childitem
            self._qp[childitem] = pos
            pos = childpos
            childpos = 2 * pos + 1
        self._pq[pos] = newitem
        self._qp[newitem] = pos
        self._swim(startpos, pos)

if __name__ == '__main__':
    pq = IndexMinPQ(10)
    for i in range(1, 7):
        pq.insert(i, 10 + i)
    pq.insert(0, 10)
    pq.debug()
