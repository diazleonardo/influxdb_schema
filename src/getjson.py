#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is mod:`getjson` from influxdb.

   
   
   Created by ldm on 2020-08-05 
"""

import os
import subprocess
import requests
import pprint
import logging
import sys

logger = logging.getLogger(__name__)
# avoid foreign logs of level
logging.getLogger("urllib3").setLevel(logging.WARNING)


def _query(url, params:str):
    r = requests.get(url + '/query?', params=params)
    if r.status_code != 200:
        raise
    return r.json()['results'][0]['series'][0]['values']


def get_databases(url: str):
    """ Get database names PLUS some basic information.

    Set the database name as keys in the final dictionary.
    We follow tis longer method just to get teh system_info too.
    :param url:
    :return:
    """

    r = requests.get(url + '/debug/vars')
    if r.status_code != 200:
        raise

    jresp = r.json()
    system_data = jresp["system"]

    dbases = {}
    for k, v in jresp.items():
        if k.startswith("database:") and not v['tags']['database'].startswith("_"):
            dbases.setdefault(v['tags']['database'], {"values": v['values']})
    del jresp

    for db in dbases.keys():
        params = {"q": "show measurements", "db": db}
        foo = _query(url, params)

        # reduce to simple lis (and not a list of lists)
        tables = [_[0] for _ in foo]

        for table in tables:
            dbases[db].setdefault(table, _query(url, params={"db": db, "q": f"show field keys from {table}"}))
    return dbases, system_data


def main(url):
    dbases, system_data = get_databases(url)
    # pprint.pprint(system_data)
    # pprint.pprint(dbases)
    # get_data(url, dbases)

    logger.debug(pprint.pformat(dbases))
    logger.debug(pprint.pformat(system_data))


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)-4.4s %(module)-21.21s %(lineno)4d - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__file__)
    logger.info("Starting %s", os.path.realpath(__file__))

    main("http://mqtt.ldiaz.lan:8086")

    logger.info("Finished")
