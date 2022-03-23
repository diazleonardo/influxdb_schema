InfluxDB Schema
===============

Many times I get confused about what is being logged in my home influx databases.

This program produces a listing of the databases, tables, fields and tags on your server.

![Portion of the listing for Raspberry Pi ](rpi.png "Portion")

Use
---

    usage: influxdb_schema.py [-h] [--outdir OUTDIR] [--debug] [--url URL] [--user USER] [--passwd PASSWD] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      --outdir OUTDIR       Name for output directory. Must exists before running.
      --debug               Output DEBUG level logs
      --url URL             Server address and port (http://influx.example.com:8086)
      --user USER, -u USER  user name if necessary for authetication.
      --passwd PASSWD, -p PASSWD
                            password if necessary for authetication.
      --version, -v         show program's version number and exit
