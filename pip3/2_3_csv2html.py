#!/bin/env python3

import csv
import io
import optparse
import xml.sax.saxutils

MAX_WIDTH = 100

def print_start():
    print("<table border='1'>")

def print_end():
    print("</table>")

def extract_fields(line):
    try:
        reader = csv.reader(io.StringIO(line), delimiter=',')
        return list(reader)[0]
    except IndexError:
        return []

def print_line(line, options):
    print("<tr bgcolor='{}'>".format(options["color"]))

    fields = extract_fields(line)

    maxwidth = options["maxwidth"]

    for field in fields:
        if not field:
            print("<td></td>")
        else:
            try:
                x = float(field.replace(",", ""))
                print("<td align='right'>{0:{1}}</td>".format(round(x), options["format"]))
            except ValueError:
                field = field.title()

                if len(field) > maxwidth:
                    field = field[:maxwidth] + "..."

                field = xml.sax.saxutils.escape(field)
                print("<td>{}</td>".format(field))

    print("</tr>")

def process_options():
    parser = optparse.OptionParser()

    parser.add_option("-w", "--maxwidth", default=100,
                      help="Maximum width of string fields(100 default)")
    parser.add_option("-f", "--format", default=".0f",
                      help="Print format for numeric fields(.0f default)")

    (opts, _) = parser.parse_args()

    options = {}

    try:
        "{0:{1}}".format(1.0, opts.format)
        options["format"] = opts.format
    except ValueError:
        options["format"] = ".0f"

    try:
        if 10 < int(opts.maxwidth) < 1000:
            options["maxwidth"] = int(opts.maxwidth)
        else:
            options["maxwidth"] = 100
    except ValueError:
        options["maxwidth"] = 100

    return options

def main():
    opts = process_options()

    print_start()

    lineno = 0

    while True:
        try:
            line = input()

            if lineno == 0:
                opts["color"] = "lightgreen"
            elif lineno % 2 == 0:
                opts["color"] = "white"
            else:
                opts["color"] = "lightyellow"

            print_line(line, opts)

            lineno += 1
        except EOFError:
            break

    print_end()

if __name__ == '__main__':
    main()
