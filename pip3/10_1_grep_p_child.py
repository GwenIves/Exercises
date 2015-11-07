#!/bin/env python3

import sys

def main():
    if len(sys.argv) == 2:
        proc_str = "{}: ".format(sys.argv[1])
    else:
        proc_str = ""

    stdin = sys.stdin.buffer.read()
    lines = stdin.decode("utf8", "ignore").splitlines()

    pattern = lines[0]
    files = lines[1:]
    block_size = min(len(pattern), 8000)

    for filename in files:
        do_grep(pattern, filename, proc_str, block_size)

def do_grep(pattern, filename, proc_str, block_size):
    previous = ""

    try:
        with open(filename, "rb") as fh:
            while True:
                current = fh.read(block_size)

                if not current:
                    break

                current = current.decode("utf8", "ignore")
                current = previous[-len(pattern):] + current
                previous = current

                if pattern in current:
                    print("{}{}".format(proc_str, filename))
                    break
    except EnvironmentError as err:
        print("{}{}".format(proc_str, err))

if __name__ == '__main__':
    main()
