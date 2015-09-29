#!/bin/env python3

import argparse
import encodings

def get_blocksize(argument):
    try:
        blocksize = int(argument)

        if not 8 < blocksize < 80:
            raise ValueError("Blocksize out of range: {}".format(blocksize))
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err))

    return blocksize

def get_encoding(argument):
    encoding = argument.lower()

    if(encoding not in encodings.aliases.aliases.keys()
            and encoding not in encodings.aliases.aliases.values()):
        raise argparse.ArgumentTypeError("Invalid encoding {}".format(argument))

    return encoding

def dump_file(filename, args):
    enc_str = "{} characters".format(args.encoding.upper())
    enc_len = len(enc_str)
    blk_len = 2 * args.blocksize +(args.blocksize - 1) // 4

    print("{}:".format(filename))
    print("{:<8}  {:<{}}  {:<{}}".format("Block", "Bytes", blk_len, enc_str, enc_len))
    print("{:-<8}  {:-<{}}  {:-<{}}".format("", "", blk_len, "", enc_len))

    block_count = 1
    block_fmt = "{:0>{}}  " if args.decimal else "{:0>{}x}  "

    try:
        with open(filename, "rb") as f:
            while True:
                block = f.read(args.blocksize)

                if not block:
                    break

                print(block_fmt.format(block_count, 8), end="")
                block_count += 1

                for index, byte in enumerate(block):
                    print("{:0>2x}".format(block[index]), end="")

                    if index % 4 == 3:
                        print(" ", end="")

                print("  ", end="")

                chars = [c if c.isprintable() else "." for c in block.decode(args.encoding)]

                print("".join(chars))
    except EnvironmentError:
        print("Error reading file {}".format(filename))

def main():
    parser = argparse.ArgumentParser(description="Show a hex dump of a binary file")

    parser.add_argument("-b", "--blocksize", action="store", type=get_blocksize,
            metavar="BLOCKSIZE", default=16,
            help="block size(8..80) [default: 16]")
    parser.add_argument("-d", "--decimal", action="store_const", const=True, default=False,
            help="decimal block numbers [default: hexadecimal]")
    parser.add_argument("-e", "--encoding", action="store", type=get_encoding,
            metavar="ENCODING", default="utf8",
            help="encoding(ASCII..UTF-32) [default: UTF-8]")
    parser.add_argument("files", action="store", nargs="+", type=str,
            help="Files to dump")

    args = parser.parse_args()

    for f in args.files:
        dump_file(f, args)

if __name__ == '__main__':
    main()
