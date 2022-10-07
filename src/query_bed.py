"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    parse_line, print_line
)
from query import Table
from format_bed import parser


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work

    # Load inputs and create BedLines, which will be added to a searchable table
    queryFile = args.query.readlines()
    bedFile = args.bed.read()
    parsedFiles = parser(bedFile)

    # Create table and load BedLines into it
    toc = Table()
    for i in parsedFiles:
        toc.add_line(i)

    # Identify queries, get chromosomes that match the search query,
    # and exclude all entries that are outside the range of the query
    final_out = []
    for j in queryFile:
        tmp = j.split("\t")
        chrom = toc.get_chrom(tmp[0])

        queryPositionStart = int(tmp[1])
        queryPositionEnd = int(tmp[2])

        for k in chrom:
            if  queryPositionStart >= k.chrom_start and queryPositionEnd < k.chrom_end:
                final_out.append(k)

    # Output all relevant features
    for i in final_out:
        print_line(i, args.outfile)


if __name__ == '__main__':
    main()
