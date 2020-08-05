#!/bin/env python3
import sys
import argparse
import json
import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

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

    jenv = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))

    dbases = foo.keys()
    template = jenv.get_template('data.html')
    logger.debug(template.render(dbases=foo, a_variable="AAA"))
    # logger.debug(dbases)

    #rendered = template.render(navigation=dbases, a_variable="AAA")

    #logger.debug(rendered)
    # for dbase in dbases:
    #     fp.write(f"\n\n<h1>Database: {dbase}</h1>")
    #     tables = foo[dbase].keys()
    #     for table in tables:
    #         fp.write(f"\n<h2>Table (measurement): {table}</h2>")
    #         cur_table = foo[dbase][table][0]
    #         fp.write(create_table(cur_table['tags'], "Tags"))
    #         fp.write(create_table(cur_table["fields"], "Field names"))
    #
    # fp.write("</body></html>")
    #


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)-4.4s %(module)-9.9s %(lineno)4d - %(message)s',
                        level=logging.DEBUG)
    logging.info("Starting %s", os.path.realpath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="JSON formatted input file")
    parser.add_argument("--outfile", "-o", help="name for output file")

    args = parser.parse_args()
    logger.debug(args)
    if args.outfile is not None:
        args.outfile = os.path.splitext(args.infile)[0] + ".html"
    logger.debug(args)
    main(args.infile, args.outfile)
