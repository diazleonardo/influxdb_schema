# InfluxDB Schema


Many times I get confused about what is being logged in my home influx databases.

This program produces a listing of the databases, tables, fields and tags on your server.



## Use

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

**--url** Server address and port (http://influx.example.com:8086)

**-- outfile** is the name (and possibly path) of the file where the zip files will be stored.  The zip suffix won't be provided.

**--user** if necessary for authetication.

**--passwd** if necessary for authetication.

**--debug** is only used for internal purposes.  Will log at the DEBUG level if set, otherwise only WARNING and above are printed.

## Product

The final product is a zip file containing at least two files. 
`style.css` contains styles for the html pages. `index.html` is a page with links to each database page.

You can modify the `css` page to your liking, but remember to keep a copy since it will be overwritten next time.

Example of the index.html file
<p align="center">
![Databases](https://github.com/diazleonardo/influxdb_schema/blob/master/src/res/databases.png)
</p>

Example of one database (rpi_monitoring.html) file

![rpi](https://user-images.githubusercontent.com/11944096/159730316-cde3ceab-84d5-4c36-97b4-e5a67cb06972.png)
