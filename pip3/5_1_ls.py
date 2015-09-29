#!/bin/env python3

import argparse
import locale
import time
import sys
import os

YEAR_SHOW_LIMIT = 60 * 60 * 24 * 30 * 6

def get_stat(root, path, args):
    if args.modified or args.sizes or args.order[0][0] != "n":
        return os.lstat(os.path.join(root, path))
    else:
        return None

def get_sort_key(args):
    if args.order[0][0] == "n":
        return lambda pair: pair[0]
    elif args.order[0][0] == "m":
        return lambda pair: pair[1].st_mtime
    else:
        return lambda pair: pair[1].st_size

def get_items(names, root, args):
    items = []

    for name in names:
        if name[0] == "." and not args.hidden:
            continue

        try:
            stat = get_stat(root, name, args)
            items.append((name, stat))
        except PermissionError as err:
            print(err, file=sys.stderr)

    return items

def print_directory(items, root, args):
    print(root)

    current_time = time.time()

    key = get_sort_key(args)

    for item in sorted(items, key=key):
        name = item[0]
        stat = item[1]

        if args.modified:
            age = current_time - stat.st_mtime

            if age > YEAR_SHOW_LIMIT:
                fmt = "%b %d  %Y "
            else:
                fmt = "%b %d %H:%M "

            print(time.strftime(fmt, time.localtime(stat.st_mtime)), end="")

        if args.sizes:
            print("{:10n} ".format(stat.st_size), end="")

        print(name)

    print()

def process_path_recursive(path, args):
    key = get_sort_key(args)

    for root, dirs, files in os.walk(path):
        items = get_items(files + dirs, root, args)

        print_directory(items, root, args)

        if not args.hidden:
            dirs[:] = [dir for dir in dirs if not dir[0] == "."]

        dirs.sort(key=key)

def process_path_single(path, args):
    items = get_items(os.listdir(path), path, args)
    print_directory(items, path, args)

def process_path(path, args):
    try:
        if args.recursive:
            process_path_recursive(path, args)
        else:
            process_path_single(path, args)
    except(PermissionError, FileNotFoundError) as err:
        print(err, file=sys.stderr)

def main():
    locale.setlocale(locale.LC_ALL, "")

    parser = argparse.ArgumentParser(description="Show directory listings")

    parser.add_argument("-H", "--hidden", action="store_const", const=True, default=False,
            help="Show hidden files [default: off]")
    parser.add_argument("-m", "--modified", action="store_const", const=True, default=False,
            help="Show last modified date/time [default: off]")
    parser.add_argument("-r", "--recursive", action="store_const", const=True, default=False,
            help="Recurse into subdirectories [default: off]")
    parser.add_argument("-s", "--sizes", action="store_const", const=True, default=False,
            help="Display sizes [default: off]")
    parser.add_argument("-o", "--order", action="store", type=str, nargs=1, default=["name"],
            choices=["name", "n", "modified", "m", "size", "s"],
            help="Order by name, modification time or size [default: name]")
    parser.add_argument("paths", action="store", nargs="*", type=str, default=".", metavar="path",
            help="Path to process, . is used if none given")

    args = parser.parse_args()

    for path in args.paths:
        process_path(path, args)

if __name__ == '__main__':
    main()
