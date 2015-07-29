#!/bin/env python3

import sys
import string
import collections

def main ():
	words = collections.defaultdict (int)
	strip = string.whitespace + string.punctuation + string.digits + "\"'"

	for filename in sys.argv[1:]:
		for line in open (filename):
			for word in line.split ():
				word = word.lower().strip(strip)

				if len (word) > 2:
					words[word] += 1

	for word, count in sorted (words.items (), key=lambda pair: pair[1], reverse=True):
		print ("'{}' occurs {} time{}".format (word, count, "s" if count > 1 else ""))

main ()