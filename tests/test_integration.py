import tempfile
from unittest import TestCase

from six import StringIO
import numpy as np
import yaml


from snag import create_namelist


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
        #self.assertIn('obs_pd', res)
