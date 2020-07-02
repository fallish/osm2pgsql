# encoding: utf-8
"""
@author: Michael
@file: pbf2pgsql.py.py
@time: 2020/7/1 4:45 PM
@desc:

The tool is used to import PBF file into postgis as snapshot schema https://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage_0.48#PostGIS_Tasks_.28Snapshot_Schema.29

Prerequisite:
    1. Python3
    2. PostgreSQL client, i.e psql
    3. Osmosis in local machine or network available to download Osmosis

"""
import glob
import os
import sys


def pbf2pgsql(args):
    osmosis_root = get_osmosis_root(args.osmosis)

    # create database
    create_database(osmosis_root, args)

    # import to postgis
    import_pbf(osmosis_root, args)


def create_database(osmosis_root, args):
    # create database
    os.putenv('PGPASSWORD', args.password)
    pgsql_args = _format_pgsql_args(args)

    _execute(f'dropdb {pgsql_args} --if-exists {args.dbname}')
    _execute(f'createdb {pgsql_args} {args.dbname}')
    _execute(f'psql {pgsql_args} -c "CREATE EXTENSION postgis" {args.dbname}')
    _execute(f'psql {pgsql_args} -c "CREATE EXTENSION hstore" {args.dbname}')
    _execute(f'psql {pgsql_args} -f {osmosis_root}/script/pgsnapshot_schema_0.6.sql {args.dbname}')
    _execute(f'psql {pgsql_args} -f {osmosis_root}/script/pgsnapshot_schema_0.6_action.sql {args.dbname}')
    _execute(f'psql {pgsql_args} -f {osmosis_root}/script/pgsnapshot_schema_0.6_bbox.sql {args.dbname}')
    _execute(f'psql {pgsql_args} -f {osmosis_root}/script/pgsnapshot_schema_0.6_linestring.sql {args.dbname}')


def import_pbf(osmosis_root, args):
    pbf = get_pbf(args.pbf)
    pg_args = _format_osmosis_pg_args(args)
    cmd = f'{osmosis_root}/bin/osmosis --read-pbf {pbf} --sort  --write-pgsql {pg_args}'
    _execute(cmd)


def _execute(cmd, default_code=0, exit_on_fail=True):
    print(cmd)
    r = os.system(cmd)
    if r != default_code:
        print(f'Error: fail to execute {cmd}')
        if exit_on_fail:
            sys.exit(-1)
        else:
            return False

    return True


def _format_osmosis_pg_args(args):
    # Note: port=xxxx is not supported by osmosis.
    # return f'database={args.dbname} host={args.host} password={args.password} user={args.user} port={args.port}'
    return f'database={args.dbname} host={args.host} password={args.password} user={args.user}'


def _format_pgsql_args(args):
    return f'-h {args.host} -p {args.port} -U {args.user}'


def get_pbf(pbf):
    """
    Get pbf path in local file system. If the pbf is website link, ftp link or hdfs url, download it to local file system,
    and return the pbf  path in local file system

    :param pbf: the pbf url
    :return: pbf in local file system
    """
    # TODO
    return pbf


def get_osmosis_root(root=None):
    """
    Find osmosis tool root directory under {root} directory or current directory. If no osmosis found, will download it

    :param root:
    :return:
    """
    osmosis = _get_osmosis_local(root)
    if osmosis:
        return os.path.dirname(os.path.dirname(osmosis))
    else:
        print('Warn: no osmosis found in local host')

    osmosis = _get_osmosis_remote()
    if osmosis:
        return osmosis
    else:
        print('Warn: no osmosis get from remote')

    raise Exception(f'osmosis not found exception under {root}')


def _get_osmosis_local(root=None):
    root = root if root else '.osmosis'
    targets = glob.glob(os.path.join(root, '**/bin/osmosis'), recursive=True)
    if targets:
        return os.path.abspath(next(iter(targets)))


def _get_osmosis_remote():
    # TODO
    # https://wiki.openstreetmap.org/wiki/Osmosis
    # https://bretth.dev.openstreetmap.org/osmosis-build/

    # ownload from remote and decompress

    import wget
    osmosis_url = 'https://bretth.dev.openstreetmap.org/osmosis-build/osmosis-0.47.zip'

    osmosis_tmp = '.osmosis'
    osmosis_root = f'{osmosis_tmp}/osmosis'
    os.path.exists(osmosis_tmp) or os.makedirs(osmosis_tmp)

    osmosis = wget.download(osmosis_url, out=osmosis_tmp)
    _execute(f'unzip {osmosis} -d {osmosis_root}')

    return os.path.abspath(osmosis_root)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('pbf', help="pbf")
    parser.add_argument('dbname', help="database name")

    parser.add_argument('-o', '--osmosis', help="osmosis search path")

    group = parser.add_argument_group('database connection options')

    group.add_argument('-H', '--host', help="database host", default='localhost')
    group.add_argument('-p', '--port', help="database port", default=5432, type=int)
    group.add_argument('-u', '--user', help="database user", default='postgres')
    group.add_argument('-w', '--password', help="database password", default='docker')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    return pbf2pgsql(args)


if __name__ == '__main__':
    main()
