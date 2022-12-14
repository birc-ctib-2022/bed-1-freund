"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from typing import TextIO
from bed import (
    parse_line, print_line
)

def parser(inputFile):
    outLines = []
    lineBegin, lineEnd = 0, 0
    for i, c in enumerate(inputFile):
        if c == "\n":
            lineEnd = i
            outLines.append(parse_line(inputFile[lineBegin:lineEnd]))
            lineBegin = i + 1
    return outLines


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(description="Cleans up a BED file")
    # 'infile' is either provided as an input file name or stdin
    argparser.add_argument('infile',
                           nargs='?',                    # 0 or 1 arguments
                           type=argparse.FileType('r'),  # file for reading
                           default=sys.stdin)
    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('outfile',
                           nargs='?',                    # 0 or 1 arguments
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work

    fileRead = args.infile.read()
    parsedLines = parser(fileRead)
    for i in parsedLines:
        print_line(i, args.outfile)

if __name__ == '__main__':
    main()
