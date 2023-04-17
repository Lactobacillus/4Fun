import os
import sys

def main():

    passed = list()

    for i in range(2, 413343 + 1):

        digit = [int(e) for e in list(str(i))]
        digit_exp = [e ** 5 for e in digit]
        digit_exp_sum = sum(digit_exp)

        if digit_exp_sum == i:

            passed.append(i)

    print(len(passed))
    print(sum(passed))


if __name__ == '__main__':

    main()
