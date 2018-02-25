from unittest import TestCase

from snag import create_namelist
import tempfile


class TestIntegration(TestCase):
    def test_create_namelist(self):
        fp = tempfile.TemporaryFile()
        create_namelist(fp, {
            'input': {
                'p': {
                    'filename': '/home/jared/Downloads/Pressure_climatology_2000s_ARM.nc',
                    'var_name': 'v'
                },
                'theta': {
                    'filename': np.range(19),
                    'var_name': 'v'
                },
                't': {
                    'filename': '',
                    'var_name': 'v'
                },
                'q': 0.0,
                'u': 2.0,
                'v': 2.0,
                'w': 0.0,

            },
            'forcing': {
              'observational': {
                  'enabled': True,
              }
            },
            'overrides': {
                'INOBSFOR': {
                    'obs_pd': 1
                }
            }
        })

        fp.seek(0)

        res = fp.read()
        self.assertGreater(len(res), 0)
        self.assertIn('inobsfor', res)
        self.assertIn('obs_pd', res)