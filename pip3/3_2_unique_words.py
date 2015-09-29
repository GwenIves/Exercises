#!/bin/env python3

import sys
import string
import collections

def main():
	words = collections.defaultdict(int)
	strip = string.whitespace + string.punctuation + string.digits + "\"'"

	for filename in sys.argv[1:]:
		try:
			with open(filename) as open_file:
				for line in open_file:
					for word in line.split():
						word = word.lower().strip(strip)

						if len(word) > 2:
							words[word] += 1
		except EnvironmentError as err:
			print(err)

	for word, count in sorted(words.items(), key=lambda pair: pair[1], reverse=True):
		print("'{}' occurs {} time{}".format(word, count, "s" if count > 1 else ""))

if __name__ == '__main__':
    main()
