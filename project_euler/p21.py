import os
import sys
import math
from typing import List, Dict, Set, Tuple, Union, Any

def get_proper_divisors(n: int) -> List[int]:

    k = int(math.sqrt(n)) + 1
    result = set()

    for idx in range(1, k + 1):

        if n % idx == 0:

            result.add(idx)
            result.add(n // idx)

    result.remove(n)

    return result, sum(result)


def main():

    pairs = set()

    for idx in range(1, 10000):

        r, s = get_proper_divisors(idx)
        rr, ss = get_proper_divisors(s)

        print(idx, r)

        if ss == idx and s != idx:

            pairs.add(idx)
            pairs.add(s)

    pairs.remove(0)
    pairs.remove(1)

    print(sum(pairs))
    print(len(pairs))
    print(pairs)


if __name__ == '__main__':

    main()
