#!/bin/env python3
import sys
import argparse
import json
import os
import logging
import tempfile

from src.getjson import get_data

logger = logging.getLogger(__name__)
# avoid foreign logs of level
logging.getLogger("requests").setLevel(logging.WARNING)

COLS = 4


def create_table(table, caption, style="border: 1px"):
    if len(table) > 0:
        _class = caption.replace(" ","_")
        result = [f'<table style="{style}" class="{_class}"><caption>{caption}</caption>']

        result.append("<tr>")
        for i, value in enumerate(table):
            if isinstance(value, (list, tuple)):
                new_value = value[0] + f" ({value[1][0]})"

            else:
                new_value = value
            result.append(f"<td>{new_value}</td>")
            if (i + 1) % COLS == 0:
                result.append("</tr><tr>")

        result.append("</table>")
    else:
        result = [f"<p>No {caption} registered</p>"]
    return '\n'.join(result)


def main(url, outfile):

    foo = get_data(url)

    if outfile is None:
        outfile = tempfile.NamedTemporaryFile(mode="w", prefix="influx_", suffix=".html", delete=False)
    else:
        outfile = open(outfile, "w")

    with outfile as fp:
        fp.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8"/>

        <style>
        body {margin-left: 2em;}
        caption {font-variant: small-caps; font-weight: bold; }
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        .Tags {width: 50%; table-layout:fixed}
        .Field_names {width: 80%; table-layout:fixed}
        table {background-color: #F0F8EB}
        th, td {padding: 5px;}
        tr:nth-child(even) {background-color: #E5F7D2;}
        h1 {border-bottom: 4px dotted blue; text-align: center; margin-top: 3em}
        h2 {margin-top:3em}
        </style>
        </head>
        <body>
        """)

        # pprint.pprint(foo)
        dbases = foo.keys()
        # logger.debug(pprint.pformat(foo))

        for dbase in dbases:
            fp.write(f"\n\n<h1>Database: {dbase}</h1>")
            tables = foo[dbase].keys()
            for table in tables:
                fp.write(f"\n<h2>Table (measurement): {table}</h2>")
                cur_table = foo[dbase][table]
                fp.write(create_table(cur_table['tags'], "Tags"))
                fp.write(create_table(cur_table["fields"], "Field names"))

        fp.write("</body></html>")
        return outfile


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)-4.4s %(module)-9.9s %(lineno)4d - %(message)s',
                        level=logging.DEBUG)
    logging.info("Starting %s", os.path.realpath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url, including port", default="http://localhost:8086")
    parser.add_argument("--outfile", "-o", help="name for output file")

    args = parser.parse_args()
    logger.debug(args)

    outfile = main(args.url, args.outfile)

    logger.info(f"Output sent to {outfile.name}")
