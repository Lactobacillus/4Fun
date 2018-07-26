import os
import sys
import argparse

argParser = argparse.ArgumentParser(description = 'pattern matching using BWT (Burrows-Wheeler Transform)')
argParser.add_argument('-s', '--string', required = True, help = 'example : panamabananas -> smnpbnnaaaaa$a')
argParser.add_argument('-p', '--pattern', required = False, help = 'string for pattern matching')

def preprocess(string):

	return string.replace('$', '') + '$'

def cyclicRotate(string):

	return string[1:] + string[0]

def BWT(string):

	stringList = list()

	for _ in range(len(string)):

		stringList.append(string)
		string = cyclicRotate(string)

	stringList.sort()
	result = ''.join([s[-1] for s in stringList])

	printList(stringList)

	return result

def inverseBWT(string):

	if string.count('$') != 1:

		return ''

	originList = list(string)
	stringList = list(string)

	for _ in range(len(string) - 1):

		stringList.sort()
		stringList = [o + s for o, s in zip(originList, stringList)]

	printList(stringList)
	
	for s in stringList:

		if s[-1] == '$':

			return s

def printList(l):

	for e in l:

		print(e)

	print('')

def getSuffixArray(string):

	stringList = list()
	suffixArray = list()

	for _ in range(len(string)):

		stringList.append(string)
		string = cyclicRotate(string)

	stringList.sort()

	for string in stringList:

		suffixArray.append((len(string.split('$')[0]) + 1) % len(stringList))

	return suffixArray

def lfMapping(original, transformed):

	lf = dict()

	characters = set(transformed)

	for char in characters:

		mapping = list()

		for idx in range(1, len(transformed) + 1):

			mapping.append(transformed[:idx].count(char))

		lf[char] = mapping

	for key, val in lf.items():

		print(key, ' : ', val)

	print('')

	return lf

def findTop(stringList, char, top):

	for idx in range(0, len(stringList)):

		if stringList[idx][-1] == char and idx >= top:

			return idx

def findBottom(stringList, char, bottom):

	for idx in range(len(stringList), 0, -1):

		if stringList[idx - 1][-1] == char and idx - 1 <= bottom:

			return idx - 1

def findFront(stringList, char, pos):

	count = 1

	for idx, string in enumerate(stringList):

		if string[0] == char:

			if pos == count:

				return idx

			else:

				count = count + 1

def patternMatching(string, query, lf):

	stringList = list()

	for _ in range(len(string)):

		stringList.append(string)
		string = cyclicRotate(string)

	stringList.sort()

	top = 0
	bottom = len(stringList)

	for idx, char in enumerate(query[::-1]):

		top = findFront(stringList, char, lf[char][findTop(stringList, char, top)])
		bottom = findFront(stringList, char, lf[char][findBottom(stringList, char, bottom)])

	return top, bottom

def main(arg):

	original = preprocess(arg.string)
	transformed = BWT(original)
	recovered = inverseBWT(transformed)

	print('o : ', original)
	print('t : ', transformed)
	print('r : ', recovered)
	print('')

	if len(arg.pattern) > 0:

		pattern = arg.pattern
		lf = lfMapping(original, transformed)
		matched = patternMatching(original, pattern, lf)

	print(matched)
	print('')

	suffix = getSuffixArray(original)
	print('suffix array : ', suffix)
	print('')

	for idx in range(matched[0], matched[1] + 1):

		pos = len(original) - suffix[idx]
		print('position : ', pos)
		print(original[:pos] + ' ' + original[pos:pos + len(pattern)] + ' ' + original[pos + len(pattern):])

if __name__ == '__main__':

	arguments = argParser.parse_args()
	main(arguments)
