from unittest import TestCase

import yaml
from six import StringIO

from snag import create_namelist
from snag.namelist import Namelist


class TestIntegration(TestCase):
    def test_create_namelist(self):
        stream = StringIO()
        cfg = yaml.load(open('test_conf.yml'))
        create_namelist(cfg, stream)

        stream.seek(0)

        res = stream.read()
        self.assertGreater(len(res), 0)
        self.assertIn('INOBSFOR', res)
        # TO be calculated
        # self.assertIn('obs_pd', res)

    def test_modify_namelist(self):
        cfg = yaml.load(open('test_conf.yml'))
        nl = Namelist(cfg)
        nl.config['INPROF']['wi'][:] = 0
        res = nl.dump()

        self.assertGreater(len(res), 0)
        self.assertIn('wi = \t0.0,\t0.0,', res)
