from unittest import TestCase
from unittest.mock import patch, Mock

from snag.grid import GriddedVariable


class TestGriddedVariableFromConf(TestCase):
    def setUp(self):
        GriddedVariable.set_data = Mock()
        load_from_nc = patch('snag.grid.load_from_nc')
        self.addCleanup(load_from_nc.stop)
        self.mock_load_from_nc = load_from_nc.start()

    def test_simple(self):
        conf = {
            'data': {
                'p': {
                    'filename': 'test.nc',
                    'variable': 'a'
                }
            }
        }
        res = GriddedVariable.from_scm_conf('p', conf)
        self.mock_load_from_nc.assert_called_once()
        self.assertTrue(isinstance(res, GriddedVariable))

    def test_common_filename(self):
        conf = {
            'data': {
                'filename': 'test.nc',
                'p': {
                    'variable': 'a'
                }
            }
        }
        GriddedVariable.from_scm_conf('p', conf)
        self.mock_load_from_nc.assert_called_once()

    def test_missing_filename(self):
        conf = {
            'data': {
                'p': {
                    'variable': 'a'
                }
            }
        }
        self.assertRaises(ValueError, GriddedVariable.from_scm_conf, 'p', conf)

    def test_not_required(self):
        conf = {
            'data': {
            }
        }
        self.assertIsNone(GriddedVariable.from_scm_conf('theta', conf))
        self.assertRaises(KeyError, GriddedVariable.from_scm_conf, 'p', conf)