import os
import sys
import math
import numpy as np
from itertools import permutations
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Union, Any

def is_palindrom(s: str) -> bool:

    return s == s[::-1]


def main():

    with open(sys.argv[1], 'r') as fs: words = fs.read().replace('"', '')
    words = words.split(',')
    words = [w for w in words if not is_palindrom(w)]

    temp = defaultdict(list)
    anagrams = dict()

    for w in words:

        key = sorted(list(w))
        temp[tuple(key)].append(w)

    for key, val in temp.items():

        if len(val) > 1: anagrams[key] = val

    table = list()
    table.append(['0', '3', '2', '1']) # STOP -> SPOT
    table.append(['3', '2', '0', '1']) # STOP -> POST

    for key, val in anagrams.items():

        if len(val) > 2: continue

        order = {e: idx for idx, e in enumerate(list(val[0]))}
        shuffled = [str(order[e]) for e in list(val[1])]
        table.append(''.join(shuffled))

    answer = list()

    for t in table:

        o = [e for e in range(len(t))]
        t = list(map(int, list(t)))

        candidates = np.array(list(permutations(range(10), len(o))))
        to_deci = np.array([10 ** (len(o) - e - 1) for e in range(len(o))]).reshape(-1, 1)
        cand_o = candidates[:,o]
        cand_t = candidates[:,t]
        valid = np.where((cand_o[:,0] != 0) & (cand_t[:,0] != 0))[0]
        cand_o = cand_o[valid, :]
        cand_t = cand_t[valid, :]
        cand_o = np.matmul(cand_o, to_deci)
        cand_t = np.matmul(cand_t, to_deci)

        oo = np.power(np.sqrt(cand_o).astype(int), 2)
        tt = np.power(np.sqrt(cand_t).astype(int), 2)

        temp_ans = np.where((oo == cand_o) & (tt == cand_t))[0]

        answer = answer + cand_o[temp_ans,...].tolist()
        answer = answer + cand_t[temp_ans,...].tolist()

    print(max(answer))


if __name__ == '__main__':

    main()
