#!/usr/bin/env python3
# vim: ts=4:sw=4:ai
"""Module  doc string
"""

import argparse
import logging
import math  # for ceil
import os
import sys
from datetime import datetime, timezone
import zipfile
import tarfile

import jinja2
import requests
import requests.status_codes

logger = logging.getLogger(__name__)


# avoid foreign logs of level
# for key in logging.Logger.manager.loggerDict:
#     print(key)
for _ in ['urllib3']:
    logging.getLogger(_).setLevel(logging.WARNING)


def flatten(list_of_lists) -> list:
    return [_[0] for _ in list_of_lists if not _[0].startswith("_")]


def req(params: str):
    try:  # this checks for the connection
        r = requests.get(args.url + "/query", params={"q": params}, auth=(args.user, args.passwd))
    except requests.exceptions.ConnectionError:
        logger.fatal(f"Connection refused")
        sys.exit(9)
    # this checks for the returned values
    if r.status_code != requests.codes.ok:
        return []
    try:  # if the series is empty it will raise error
        k = r.json()["results"][0]["series"][0]["values"]
    except KeyError:
        k = []
    return k


def databases() -> list:
    k = req(params="SHOW DATABASES")
    return flatten(k)


def retention(dba: str) -> dict:
    """list of retention policies as a dict."""
    k = req(params=f"SHOW RETENTION POLICIES ON {dba}")
    return k[0]


def series(dba: str) -> list:
    """A logical grouping of data defined by shared measurement, tag set, and field key. """
    k = req(f"SHOW SERIES ON {dba}")
    return flatten(k)


def measurements(dba: str) -> list:
    k = req(f"SHOW MEASUREMENTS ON {dba}")
    return flatten(k)


def tag_keys(dba: str, from_table: str) -> list:

    k = req(f"SHOW TAG KEYS ON {dba} FROM {from_table}")
    return flatten(k)


def tag_values(dba: str, from_table: str, key) -> list:
    k = req(f'SHOW TAG VALUES ON {dba} FROM {from_table} WITH KEY = "{key}"')
    return list(zip(*k))[1]


def fields(dba: str, from_table: str, cols=5) -> list:
    k = req(f"SHOW FIELD KEYS ON {dba} FROM {from_table}")
    try:
        lista = [(k[i][0], k[i][1]) for i in range(0, len(k), 1)]
    except KeyError:
        return []

    rows = math.ceil(len(lista) / cols)
    sec_list = []
    if rows == 1 and len(lista) < cols:
        sec_list = [lista[c:] for c in range(len(lista))]
    else:
        for r in range(rows):
            pri_list = []
            for c in range(cols):
                try:
                    pri_list.append(lista[r * cols + c])
                except IndexError:
                    pri_list.append(" "*6)

            sec_list.append(pri_list)
    return sec_list


def per_database(db: str, renderer) -> str:
    tables = measurements(db)
    ret = retention(db)
    ser = series(db)
    #  logger.debug(f"Series for {db} {len(ser)}")
    tab_dict = {}
    for table in tables:
        fi2 = fields(db, table)
        tags_in_meas = tag_keys(db, table)
        tags = []
        for v in tags_in_meas:
            tags.append({v: tag_values(db, table, v)})
        tab_dict[table] = (fi2, tags)  # fi2 is a [list of [list] of tuple (temp0, float)]

    return renderer.render(db=db, ret=ret, tables=tab_dict)


def main():
    env = jinja2.Environment(loader=jinja2.PackageLoader("src"),
                             autoescape=jinja2.select_autoescape(),
                             trim_blocks=True, lstrip_blocks=True, )
    tpl_index = env.get_template("index.html")
    tpl_per_db = env.get_template("per_db.html")

    dbs = databases()
    data = open("res/style.css", "r").read()

    cdir = os.getcwd()
    os.chdir(args.outdir)
    with zipfile.ZipFile("influxdb_schema.zip", "w", compression=zipfile.ZIP_DEFLATED) as myzip:
        myzip.writestr("style.css", data=data)
        data = tpl_index.render(table_name="Databases", databases=dbs,
                                footer="As of " + datetime.now(timezone.utc).isoformat(sep="T", timespec='minutes'))
        myzip.writestr("index.html", data=data)

        for db in dbs[0:]:
            data = per_database(db, tpl_per_db)
            myzip.writestr(f"{db}.html", data=data)

    os.chdir(cdir)
    logger.info(f"Output written to {args.outdir}")


def version():
    parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(parent_folder+'/setup.py', "r") as fp:
        lines = fp.readlines()
    foo = [line for line in lines if line.startswith("__version__")][0].split('=')[1].strip()
    return foo


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", help="Name for output directory. Must exists before running.",
                        default="/tmp/influxdb_schema")
    parser.add_argument("--debug",
                        help="Output DEBUG level logs", action="store_true")
    parser.add_argument("--url",
                        help="Server address and port (http://influx.example.com:8086)",
                        default="http://localhost:8086")
    parser.add_argument("--user", "-u", default=None,
                        help="user name if necessary for authetication.")
    parser.add_argument("--passwd", "-p", default=None,
                        help="password if necessary for authetication.")
    parser.add_argument("--version","-v", action="version",
                        version="%(prog)s (version {version})".format(version=version()))
    args = parser.parse_args()
    print(args)

    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.FATAL

    logging.basicConfig(format='%(levelname)-4.4s %(module)-9.9s %(lineno)4d - %(message)s', level=level)
    logger = logging.getLogger(__file__)
    logger.info("Starting %s", os.path.realpath(__file__))

    main()

    logger.info("Finished")
