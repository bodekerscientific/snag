from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from snag.namelist import Namelist


class TestGriddedVariableFromConf(TestCase):

    @patch('snag.namelist.GriddedVariable')
    def test_simple(self, mock_gridded_variable):
        mock_gridded_variable.from_scm_conf().datetime_span.return_value = (datetime(2000, 1, 1), datetime(2000, 1, 2, 6))
        nl = Namelist({})

        self.assertEqual(2000, nl.config['INDATA']['year_init'])
        self.assertEqual(1, nl.config['INDATA']['month_init'])
        self.assertEqual(1, nl.config['INDATA']['day_init'])
        self.assertEqual(0, nl.config['INDATA']['sec_init'])
        self.assertEqual(1, nl.config['RUNDATA']['ndayin'])
        self.assertEqual(360, nl.config['RUNDATA']['nminin'])

    @patch('snag.namelist.GriddedVariable')
    @patch('snag.namelist.logger')
    def test_explicit(self, mock_logger, mock_gridded_variable):
        conf = {
            'INDATA': {
                'year_init': 2001,
            }
        }
        mock_gridded_variable.from_scm_conf().datetime_span.return_value = (datetime(2000, 1, 1), datetime(2000, 1, 2, 6))
        nl = Namelist(conf)

        # This overrides the value from the file
        self.assertEqual(2001, nl.config['INDATA']['year_init'])

        # rest remain the same
        self.assertEqual(1, nl.config['INDATA']['month_init'])
        self.assertEqual(1, nl.config['INDATA']['day_init'])
        self.assertEqual(0, nl.config['INDATA']['sec_init'])
        self.assertEqual(1, nl.config['RUNDATA']['ndayin'])
        self.assertEqual(360, nl.config['RUNDATA']['nminin'])

        mock_logger.warning.assert_called_once()