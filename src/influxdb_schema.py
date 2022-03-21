#!/usr/bin/env python3
# vim: ts=4:sw=4:ai

import requests
import pprint
import json
import argparse
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("src"), autoescape=select_autoescape(),
                  trim_blocks=True, lstrip_blocks=True, )
db_tpl = env.get_template("databases.html")
tb_tpl = env.get_template("table_dict.html")

URL = "http://mqtt.ldiaz.lan:8086"

base_dir = "../html"


def flatten(list_of_lists) -> list:
    return [_[0] for _ in list_of_lists if not _[0].startswith("_")]


def databases():
    r = requests.get(URL + "/query", params={"q": "SHOW DATABASES"})
    k = r.json()["results"][0]["series"][0]["values"]
    return flatten(k)


def retention(dba):
    """list of retention policies as a dict."""
    r = requests.get(URL + "/query", params={"q": f"SHOW RETENTION POLICIES ON {dba}"})
    k = r.json()["results"][0]["series"][0]["values"]
    d = {}
    for i in k:
        d["name"] = i[0]
        d["duration"] = i[1]
        d["shardDuration"] = i[2]
        d["replicaN"] = i[3]
        d["default"] = i[4]
    return d


def series(dba):
    """list of retention policies as a dict."""
    r = requests.get(URL + "/query", params={"q": f"SHOW SERIES ON {dba}"})
    print(r.status_code)
    k = r.json()["results"][0]["series"][0]["values"]
    print(k)


def measurements(dba):
    """list of retention policies as a dict."""
    r = requests.get(URL + "/query", params={"q": f"SHOW MEASUREMENTS ON {dba}"})
    print(r.status_code)
    k = r.json()["results"][0]["series"][0]["values"]
    return flatten(k)


def tag_keys(dba, m):
    """list of retention policies as a dict."""
    r = requests.get(URL + "/query", params={"q": f"SHOW TAG KEYS ON {dba} FROM {m}"})
    # print(r.json())
    if int(r.status_code) < 400:
        try:
            k = r.json()["results"][0]["series"][0]["values"]
        except KeyError:
            return []
    else:
        return []
    return flatten(k)


def tag_values(dba, m, key):
    """list of retention policies as a dict."""
    r = requests.get(
        URL + "/query",
        params={"q": f'SHOW TAG VALUES ON {dba} FROM {m} WITH KEY = "{key}"'},
    )
    # print(r.json()["results"][0]["series"][0]["values"])
    if int(r.status_code) < 400:
        try:
            k = r.json()["results"][0]["series"][0]["values"]
        except KeyError:
            return []
    else:
        return []

    return list(zip(*k))[1]


def fields(dba:str, m:str, cols=5) -> [list, list]:
    r = requests.get(URL + "/query", params={"q": f"SHOW FIELD KEYS ON {dba} FROM {m}"})
    if int(r.status_code) < 400:
        try:
            k = r.json()["results"][0]["series"][0]["values"]
            lista = [(k[i][0], k[i][1]) for i in range(0, len(k), 1)]
        except KeyError:
            return []
    else:
        return []
    # XXXX: new format
    import math  # (len(a)/cols)
    rows = math.ceil(len(lista) / cols)
    sec_list = []
    for r in range(rows):
        pri_list = []
        for c in range(cols):
            try:
                pri_list.append(lista[r * cols + c])
            except IndexError:
                pri_list.append("")

        sec_list.append(pri_list)
    return lista, sec_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        "-o",
        help="name for output directory",
        default="/tmp/influxdb_schema",
    )
    args = parser.parse_args()

    dbs = databases()
    rete = [retention(db) for db in dbs]

    print(db_tpl.render(table_name="Databases", databases=dbs, ret=rete),
                        file=open(f"{base_dir}/databases.html", 'w'))

    for db in dbs[0:]:
        tables = measurements(db)

        table_dict = {}
        for table in tables:
            table_dict[table] = {}
            fi, fi2 = fields(db, table)

            tags_in_meas = tag_keys(db, table)
            foo = []
            for v in tags_in_meas:
                foo.append({v: tag_values(db, table, v)})
            table_dict[table]["tags"] = foo
            # results[db] = table_dict
            print(tb_tpl.render(table_name=table, fields=fi2, tags=foo),
                  file=open(f"{base_dir}/{table}.html", 'w'))
    print("END")
