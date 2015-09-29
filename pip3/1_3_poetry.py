#!/bin/env python3

import random
import sys

articles = ["a", "the"]
subjects = ["cat", "dog", "man", "woman"]
verbs = ["sang", "ran", "jumped"]
adverbs = ["loudly", "quietly", "well", "badly"]

def main():
	lines = 5

	try:
		i = int(sys.argv[1])

		if 1 < i < 10:
			lines = i
	except(ValueError, IndexError):
		pass

	for line in range(lines):
		print("{} {} {}".format(random.choice(articles), random.choice(subjects), random.choice(verbs)), end = "")

		if random.randint(1, 100) < 50:
			print(" {}".format(random.choice(adverbs)))
		else:
			print()

if __name__ == '__main__':
    main()
