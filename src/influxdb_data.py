#!/bin/env python3
import sys
import argparse
import json
import os
import logging
import pprint


logger = logging.getLogger(__name__)
# avoid foreign logs of level
logging.getLogger("requests").setLevel(logging.WARNING)

COLS = 4
width = 72 // COLS


def create_table(table, caption, style="border: 1px"):
    if len(table) > 0:
        result = [f'<table style="{style}"><caption>{caption}</caption>']
        rows = max(1, len(table) // COLS)
        counter = 0
        for r in range(rows):
            result.append("<tr>")
            for c in range(COLS):
                try:
                    value = table[counter]
                except IndexError:
                    break
                counter += 1
                result.append(f"<td>{value}</td>")
            result.append("</tr>")
        result.append("</table>")
    else:
        result = [f"<p>No {caption} registered</p>"]
    return '\n'.join(result)


def main(infile, outfile):
    # open data file
    with open(infile) as fp:
        foo = json.load(fp)

    with open(outfile, "w") as fp:
        fp.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8"/>

        <style>
        body {margin-left: 2em;}
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        table {background-color: #F0F8EB}
        th, td {padding: 5px;}
        tr:nth-child(even) {background-color: #E5F7D2;}
        </style>
        </head>
        <body>
        """)

        # pprint.pprint(foo)
    dbases = foo.keys()
    logger.debug(pprint.pformat(foo))

    for dbase in dbases:
        fp.write(f"\n\n<h1>Database: {dbase}</h1>")
        tables = foo[dbase].keys()
        for table in tables:
            fp.write(f"\n<h2>Table (measurement): {table}</h2>")
            cur_table = foo[dbase][table][0]
            fp.write(create_table(cur_table['tags'], "Tags"))
            fp.write(create_table(cur_table["fields"], "Field names"))

    fp.write("</body></html>")


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)-4.4s %(module)-9.9s %(lineno)4d - %(message)s',
                        level=logging.DEBUG)
    logging.info("Starting %s", os.path.realpath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="JSON formatted input file")
    parser.add_argument("--outfile", "-o", help="name for output file", default="/tmp/aaaaa.html")

    args = parser.parse_args()
    logger.debug(args)
    if args.outfile is not None:
        args.outfile = os.path.splitext(args.infile)[0] + ".html"
    logger.debug(args)
    main(args.infile, args.outfile)
