# encoding: utf-8
"""
@author: Michael
@file: test_pbf2pgsql.py
@time: 2020/7/1 4:51 PM
@desc:
"""
import shlex
import shutil
from unittest import TestCase

import sqlalchemy_utils as sau

from osm2pgsql import *


class Test(TestCase):
    # args = None

    @classmethod
    def setUpClass(cls) -> None:
        os.environ['PGPASSWORD'] = 'xxx'  # TODO: localhost postgresql password
        print(os.getenv('PGPASSWORD'))
        cls.args = parse_args_imp(shlex.split('./resources/demo.osm.pbf osm_demo'))

    def test_get_osmosis_root(self):
        # Clean osmosis directory if exists
        osmosis_local_dir = '.osmosis'
        if os.path.exists(osmosis_local_dir):
            shutil.rmtree(osmosis_local_dir)

        target_osmosis_root = os.path.abspath('.osmosis/osmosis')
        osmosis_root = get_osmosis_root()

        self.assertEqual(target_osmosis_root, osmosis_root)

    def test_osm2pgsql(self):
        # Clean before import
        url = pgargs.for_url(self.args)
        if sau.database_exists(url):
            sau.drop_database(url)
        self.assertFalse(sau.database_exists(url))

        # import osm to postgresql
        osm2pgsql(args=self.args)
        self.assertTrue(sau.database_exists(url))
