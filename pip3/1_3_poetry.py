#!/bin/env python3

import random
import sys

ARTICLES = ["a", "the"]
SUBJECTS = ["cat", "dog", "man", "woman"]
VERBS = ["sang", "ran", "jumped"]
ADVERBS = ["loudly", "quietly", "well", "badly"]

def main():
    lines = 5

    try:
        i = int(sys.argv[1])

        if 1 < i < 10:
            lines = i
    except(ValueError, IndexError):
        pass

    for _ in range(lines):
        print(
            "{} {} {}".format(
                random.choice(ARTICLES),
                random.choice(SUBJECTS),
                random.choice(VERBS)
            ),
            end=""
        )

        if random.randint(1, 100) < 50:
            print(" {}".format(random.choice(ADVERBS)))
        else:
            print()

if __name__ == '__main__':
    main()
