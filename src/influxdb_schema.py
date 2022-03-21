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


def fields(dba, m):
    r = requests.get(URL + "/query", params={"q": f"SHOW FIELD KEYS ON {dba} FROM {m}"})
    # print(r.json()["results"][0]["series"][0]["values"])
    if int(r.status_code) < 400:
        try:
            k = r.json()["results"][0]["series"][0]["values"]
            lista = {k[i][0]: k[i][1] for i in range(0, len(k), 1)}
        except KeyError:
            return []
    else:
        return []

    return lista


# ----------
HEADER = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>influxDB format</title>
<style>
body {margin-left: 2em;}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
table {background-color: #F0F8EB}
th, td {padding: 5px;}
tr:nth-child(even) {background-color: #E5F7D2;}

input[type='checkbox'] { display: none; } 
.wrap-collabsible { margin: 1.2rem 0; } 
.lbl-toggle { display: block; font-weight: bold; font-family: monospace; 
    font-size: 1.2rem; text-transform: uppercase; text-align: center; 
    padding: 1rem; color: #DDD; background: #0069ff; cursor: pointer; 
    border-radius: 7px; transition: all 0.25s ease-out; } 
.lbl-toggle:hover { color: #FFF; } 
.lbl-toggle::before { content: ' '; display: inline-block; 
    border-top: 5px solid transparent; border-bottom: 5px solid transparent; 
    border-left: 5px solid currentColor; vertical-align: middle; 
    margin-right: .7rem; transform: translateY(-2px); transition: transform .2s ease-out; } 
.toggle:checked+
.lbl-toggle::before { transform: rotate(90deg) translateX(-3px); } 
.collapsible-content { max-height: 0px; overflow: hidden; transition: max-height .25s ease-in-out; } 
.toggle:checked + .lbl-toggle + .collapsible-content { max-height: 350em; } 
.toggle:checked + .lbl-toggle { border-bottom-right-radius: 0; border-bottom-left-radius: 0; } 
.collapsible-content 
.content-inner { background: rgba(0, 105, 255, .2); border-bottom: 1px solid rgba(0, 105, 255, .45); 
    border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; padding: .5rem 1rem; } 
.collapsible-content p { margin-bottom: 0; }
    
    </style>
</head>
<body>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outfile",
        "-o",
        help="name for output file",
        default="/tmp/influx_db.schema.html",
    )
    args = parser.parse_args()

    dbs = databases()
    # TODO:  tt = db_tpl.render(table_name="Databases", databases=dbs)
    for db in dbs[0:]:
        tables = measurements(db)
        print(retention(db))
        table_dict = {}
        for table in tables:
            table_dict[table] = {}
            fi = fields(db, table)
            # table_dict[table]["fields"] = fi

            tags_in_meas = tag_keys(db, table)
            foo = []
            for v in tags_in_meas:
                foo.append({v: tag_values(db, table, v)})
            table_dict[table]["tags"] = foo
            # results[db] = table_dict
            print(tb_tpl.render(table_name=table, fields=fi, tags=foo),
                  file=open(f"/tmp/{table}.html", 'w'))
    print("END")
