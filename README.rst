InfluxDB Schema
===============

Many times I get confused about what is being logged in my home influx databases.

This program produces a listing of the databases, tables, fields and tags on your server.

![Portion of the listing for Raspberry Pi ](https://github.com/diazleonardo/influxdb_schema/blob/master/src/res/rpi.png)

![SSS Portion of the listing for Raspberry Pi ](/influxdb_schema/blob/master/src/res/rpi.png)

Use
---

```

usage: influxdb_schema.py [-h] [--outfile OUTFILE] [--debug] [--url URL] [--user USER] [--passwd PASSWD] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE, -o OUTFILE
                        Name for the output (zip) file.
  --debug               Output DEBUG level logs
  --url URL             Server address and port (http://influx.example.com:8086)
  --user USER, -u USER  user name if necessary for authetication.
  --passwd PASSWD, -p PASSWD
                        password if necessary for authetication.
  --version, -v         show program's version number and exit

```
