#!/bin/env python3

import sys
import collections

def main():
    sites = collections.defaultdict(set)

    for filename in sys.argv[1:]:
        try:
            with open(filename) as open_file
                for line in open_file:
                    add_sites(line, sites, filename)
        except EnvironmentError as err:
            print(err)

    print_sites(sites)

def add_sites(line, sites, filename):
    i = 0
    size = len(line)

    while True:
        site = None

        i = line.find("http://", i)

        if i == -1:
            break

        i += 7

        for j in range(i, size):
            if not line[j].isalnum() and line[j] not in ".-":
                site = line[i:j]
                break

        if site:
            sites[site].add(filename)

def print_sites(sites):
    for site in sorted(sites):
        print("{} is referred to in:".format(site))

        for filename in sorted(sites[site], key=str.lower):
            print("\t{}".format(filename))

if __name__ == '__main__':
    main()
