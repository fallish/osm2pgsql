# Introduction
The tool is used to import PBF file into postgis as [snapshot schema](https://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage_0.48#PostGIS_Tasks_.28Snapshot_Schema.29)

# Usage
```shell script
    usage: osm2pgsql.py [-h] [-o OSMOSIS] [-H HOST] [-p PORT] [-u USER] [-w PASSWORD] pbf dbname

    positional arguments:
      pbf                   pbf
      dbname                database name
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OSMOSIS, --osmosis OSMOSIS
                            osmosis search path
    
    database connection options:
      -H HOST, --host HOST  database host
      -p PORT, --port PORT  database port
      -u USER, --user USER  database user
      -w PASSWORD, --password PASSWORD
                            database password
```


# Example
```shell script
    python3 osm2pgsql.py xxx.osm.pbf osmdb_xxx -H localhost -u postgres -w xxx
```
The password also can be set via environment variable PGPASSWORD 
```shell script
    export PGPASSWORD=xxx
```
