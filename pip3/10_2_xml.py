#!/bin/env python3

import argparse
import os
import queue
import threading
import xml.etree.ElementTree

class Worker(threading.Thread):
    def __init__(self, input_queue, output_queue, args):
        super().__init__()

        self.input_queue = input_queue
        self.output_queue = output_queue
        self.verbose = args.verbose
        self.debug = args.debug

    def run(self):
        while True:
            try:
                filename = self.input_queue.get()
                self.process(filename)
            finally:
                self.input_queue.task_done()

    def process(self, filename):
        result = {}
        tags = set()

        try:
            with open(filename, 'r') as f:
                if self.debug:
                    print("{} processing {}".format(threading.current_thread().name, filename))

                line = f.readline()

                if line.startswith("<?xml"):
                    tree = xml.etree.ElementTree.parse(f)

                    for element in tree.iter():
                        tags.add(element.tag)

                    result["tags"] = tags
        except (IOError, UnicodeDecodeError, xml.etree.ElementTree.ParseError) as err:
            if self.verbose:
                result["error"] = str(err)

        if result:
            self.output_queue.put((filename, result))

def main():
    args = parse_options()

    input_queue = queue.Queue()
    output_queue = queue.Queue()

    for _ in range(args.threads):
        worker = Worker(input_queue, output_queue, args)
        worker.daemon = True
        worker.start()

    get_files(args.paths, input_queue)
    input_queue.join()
    output_results(output_queue)

def parse_options():
    def thread_count(value):
        value = int(value)

        if value < 1:
            value = 1
        elif value > 20:
            value = 20

        return value

    parser = argparse.ArgumentParser(description="Print a summary of XML files in path")

    parser.add_argument(
        "--threads", "-t", type=thread_count, default=8,
        help="The number of threads to use [1..20]"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", default=False
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=False
    )
    parser.add_argument(
        "paths", type=str, nargs="+",
        help="Paths to search for XML files in"
    )

    return parser.parse_args()

def get_files(paths, output_queue):
    for path in paths:
        if os.path.isfile(path):
            output_queue.put(path)
        else:
            for root, _, files in os.walk(path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    output_queue.put(file_path)

def output_results(output_queue):
    output = []

    while True:
        try:
            item = output_queue.get(False)
        except queue.Empty:
            break
        else:
            output.append(item)

    for filename, processed in sorted(output):
        print(filename)

        if "error" in processed:
            print("\tError: {}".format(processed["error"]))
        else:
            for tag in sorted(processed["tags"]):
                print("\t{}".format(tag))


if __name__ == "__main__":
    main()
