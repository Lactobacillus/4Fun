import os
import sys
import math
import numpy as np

def is_prime(n):

    if n == 1: return False
    elif n in [2, 3, 5, 7]: return True

    for i in range(2, int(math.sqrt(n) + 1)):

        if n % i == 0: break

    else:

        return True

    return False


def compute_prime_list(n):

    non_prime = {k: False for k in range(1, n + 1)}

    for i in range(2, n):

        if non_prime[i]:

            continue
        
        if is_prime(i):

            for j in range(i * 2, n + 1, i):

                non_prime[j] = True

    prime_list = [e for e in range(2, n + 1) if not non_prime[e]]

    return prime_list


def main():

    n = 1000000

    consum_idx = 1
    consum = dict()
    result = list()

    prime_list = compute_prime_list(n)
    prime_list_np = np.array(prime_list)
    prime_list_set = set(prime_list)

    consum[0] = prime_list_np[:]

    while True:

        to_be_added = prime_list_np[consum_idx:]
        consum[consum_idx] = consum[consum_idx - 1][0:-1] + to_be_added[:consum[consum_idx - 1][0:-1].shape[0]]
        consum[consum_idx] = consum[consum_idx][consum[consum_idx] <= n]

        check = list(map(is_prime, consum[consum_idx].tolist()))
        check_idx = [idx for idx, val in enumerate(check) if val]

        for idx in check_idx:

            if consum[consum_idx][idx] < n:

                result.append(consum[consum_idx][idx])

        if all([e > n for e in consum[consum_idx]]):

            break

        consum_idx = consum_idx + 1

        print(result[-1])


if __name__ == '__main__':

    main()
