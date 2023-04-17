import os
import sys

def main():

    a_list = [e for e in range(2, 100 + 1)]
    b_list = [e for e in range(2, 100 + 1)]
    result = list()

    for a in a_list:

        for b in b_list:

            result.append(a ** b)

    result = list(set(result))
    result.sort()

    print(result)
    print(len(result))


if __name__ == '__main__':

    main()
