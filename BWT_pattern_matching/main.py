import os
import sys
import argparse

argParser = argparse.ArgumentParser(description = 'pattern matching using BWT (Burrows-Wheeler Transform)')
argParser.add_argument('-s', '--string', required = True, help = 'example : panamabananas -> smnpbnnaaaaa$a')

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

def main(original):

	original = preprocess(original)
	transformed = BWT(original)
	recovered = inverseBWT(transformed)

	print('o : ', original)
	print('t : ', transformed)
	print('r : ', recovered)

if __name__ == '__main__':

	arguments = argParser.parse_args()
	main(arguments.string)
