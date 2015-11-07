#!/bin/env python3

import os
import sys
import argparse
import subprocess

def main():
    prefix, extension = os.path.splitext(__file__)
    child = prefix + "_child" + extension

    args = parse_options()
    files = get_files(args)

    do_grep(files, args, child)

def do_grep(files, args, child):
    count = len(files)
    count_per_proc = count // args.processes

    proc = 1
    start = 0
    end = count_per_proc + count % args.processes
    pipes = []

    while start < count:
        command = [sys.executable, child]

        if args.debug:
            command.append(str(proc))

        pipe = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        pipes.append(pipe)

        pipe.stdin.write(args.pattern.encode("utf8") + b"\n")

        for filename in files[start:end]:
            pipe.stdin.write(filename.encode("utf8") + b"\n")

        pipe.stdin.close()

        proc += 1
        start = end
        end += count_per_proc

    results = []

    while pipes:
        pipe = pipes.pop()
        results.extend(pipe.stdout.readlines())
        pipe.wait()

    for line in sorted(results):
        print(line.decode("utf8").strip())

def parse_options():
    def proc_count(value):
        value = int(value)

        if value < 1:
            value = 1
        elif value > 20:
            value = 20

        return value

    parser = argparse.ArgumentParser(description="Print file names with lines matching a pattern")

    parser.add_argument(
        "--processes", "-p", type=proc_count, default=8,
        help="The number of child processes to use [1..20]"
    )
    parser.add_argument(
        "--recurse", "-r", action="store_true", default=False,
        help="Recurse into subdirectories"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", default=False,
        help="Log debugging information"
    )
    parser.add_argument(
        "pattern", type=str,
        help="Pattern to search for"
    )
    parser.add_argument(
        "paths", type=str, nargs="+",
        help="Paths to search for the pattern in"
    )

    return parser.parse_args()

def get_files(args):
    file_list = []

    for path in args.paths:
        if os.path.isfile(path):
            file_list.append(path)
        elif args.recurse:
            for root, _, files in os.walk(path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_list.append(file_path)

    return file_list

if __name__ == '__main__':
    main()
