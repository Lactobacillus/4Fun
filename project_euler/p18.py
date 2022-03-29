import os
import sys

def main():

    maxsum = list()

    with open(sys.argv[1], 'r') as fs: lines = fs.readlines()
    lines = [list(map(int, l[:-1].split())) for l in lines]

    maxsum.append([lines[0][0]])

    for idx, val in enumerate(lines):

        if idx == 0: continue

        maxsum.append(list())

        for jdx in range(idx + 1):

            if jdx == 0:

                maxsum[-1].append(maxsum[-2][0] + lines[idx][jdx])

            elif jdx == idx:

                maxsum[-1].append(maxsum[-2][-1] + lines[idx][jdx])

            else:

                maxsum[-1].append(max(lines[idx][jdx] + maxsum[-2][jdx - 1], lines[idx][jdx] + maxsum[-2][jdx]))

    print(max(maxsum[-1]))


if __name__ == '__main__':

    main()
