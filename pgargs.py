# encoding: utf-8
"""
@author: Michael
@file: pgargs.py
@time: 2020/7/3 10:00 AM
@desc:
"""
import argparse
import os

import sys


def for_psql(args):
    return PGArgs.from_args(args).for_psql()


def for_osmosis(args):
    return PGArgs.from_args(args).for_osmosis()


def for_url(args):
    return PGArgs.from_args(args).for_url()


def _get_or_default(v, default):
    return v if v is not None else default


def _arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host', help="database host", default='localhost')
    parser.add_argument('-p', '--port', help="database port", default=5432, type=int)
    parser.add_argument('-u', '--user', help="database user", default='postgres')
    parser.add_argument('-w', '--password', help="database password")

    return parser


class PGArgs(object):
    def __init__(self, dbname, host=None, port=None, user=None, password=None):
        self._dbname = dbname
        self._host = _get_or_default(host, 'localhost')
        self._port = _get_or_default(port, 5432)
        self._user = _get_or_default(user, 'postgres')
        self._password = _get_or_default(password, os.getenv('PGPASSWORD'))

    @classmethod
    def from_args(cls, args=None):
        if isinstance(args, argparse.Namespace):
            return PGArgs._from_namespace(args)
        elif isinstance(args, list):
            return PGArgs._from_args(args)
        elif args is None:
            return PGArgs._from_args(sys.argv[1:])

    def for_psql(self):
        if os.getenv('PGPASSWORD') != self.password:
            os.environ['PGPASSWORD'] = self.password
        return f'-h {self.host} -p {self.port} -U {self.user}'

    def for_osmosis(self):
        # Note: port=xxxx is not supported by osmosis.
        # return f'database={args.dbname} host={args.host} password={args.password} user={args.user} port={args.port}'
        return f'database={self.dbname} host={self.host} password={self.password} user={self.user}'

    def for_url(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}'

    @classmethod
    def _from_namespace(cls, args: argparse.Namespace):
        return cls(args.dbname, args.host, args.port, args.user, args.password)

    @classmethod
    def _from_args(cls, args: list):
        args = _arg_parser().parse_args(args)
        return PGArgs._from_namespace(args)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def dbname(self):
        return self._dbname
