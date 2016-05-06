#!/bin/env python3

import os
import argparse
import functools
import datetime

def coroutine(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        generator = f(*args, **kwargs)
        next(generator)
        return generator

    return wrapper

@coroutine
def reporter(args, _pipeline):
    M = 1024 * 1024

    while True:
        f, stat = (yield)

        out = "{:40s}".format(f)

        if 'size' in args.output:
            size = stat.st_size

            if size > M:
                size /= M
                suffix = "m"
            elif size > 1024:
                size /= 1024
                suffix = "k"
            else:
                suffix = " "

            out += "{:10.2f}{}".format(size, suffix)

        if 'date' in args.output:
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            out += "{:>40s}".format(mtime.strftime('%Y-%d-%m %H:%M:%S'))

        print(out)

@coroutine
def suffix_matcher(args, pipeline):
    while True:
        f, stat = (yield)

        if args.suffix:
            ext = os.path.splitext(f)[1]
            ext = ext[1:]

            if ext not in args.suffix:
                continue

        pipeline.send((f, stat))

@coroutine
def size_matcher(args, pipeline):
    while True:
        f, stat = (yield)

        if args.smaller is not None and stat.st_size > args.smaller:
            continue
        if args.bigger is not None and stat.st_size < args.bigger:
            continue

        pipeline.send((f, stat))

@coroutine
def age_matcher(args, pipeline):
    while True:
        f, stat = (yield)

        if args.days is not None:
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            delta = datetime.datetime.now() - mtime

            if delta.days > args.days:
                continue

        pipeline.send((f, stat))

@coroutine
def get_files(_args, pipeline):
    def propagate(f):
        stat = os.stat(f)
        pipeline.send((f, stat))
    while True:
        path = (yield)

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    propagate(os.path.join(root, f))
        else:
            propagate(path)

def main():
    args = parse_args()

    pipeline = None
    steps = []

    for c in (reporter, suffix_matcher, size_matcher, age_matcher, get_files):
        pipeline = c(args, pipeline)
        steps.append(pipeline)

    for path in args.paths:
        pipeline.send(path)

    for step in steps:
        step.close()

def parse_args():
    def size(val):
        amount, unit = val[:-1], val[-1]
        unit = unit.lower()

        if unit == 'k':
            return int(amount) * 1024
        elif unit == 'm':
            return int(amount) * 1024 * 1024
        else:
            return int(val)

    parser = argparse.ArgumentParser(description="Show file properties")

    parser.add_argument(
        "-d", "--days", action="store", type=int, default=None,
        help="Discard older than d days"
    )

    parser.add_argument(
        "-b", "--bigger", action="store", type=size, default=None,
        help="Discard smaller than b bytes"
    )

    parser.add_argument(
        "-s", "--smaller", action="store", type=size, default=None,
        help="Discard larger than b bytes"
    )

    parser.add_argument(
        "-u", "--suffix", action="store", type=str, nargs='*', default=[],
        help="Discard not matching suffix"
    )

    parser.add_argument(
        "-o", "--output", action="store", type=str, nargs='*', default=[],
        choices=["size", "date"],
        help="Properties to output"
    )

    parser.add_argument(
        "paths", action="store", nargs="*", type=str, default=".", metavar="path",
        help="Paths to process, . is used if none given"
    )

    return parser.parse_args()

if __name__ == '__main__':
    main()
