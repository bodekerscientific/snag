import netCDF4 as nc
import numpy as np

from jc_scripts.dsc_scm.vertical_interp import vert_interp
from snag import DATA_SECTION


def load_from_nc(conf):
    ds = nc.Dataset(conf['filename'])

    return ds.variables[conf['var_name']]


class GriddedVariable(object):
    """
    A single gridded data variable

    Used for calculating the IC, BCs and tendencies
    """

    def __init__(self, var_name):
        self.var_name = var_name
        self._data = None

    def set_data(self, data):
        self._data = self._vertical_interpolation(data)

    def _vertical_interpolation(self, data):
        # Pass through to call Jono's script

        return vert_interp(data, self.var_name, range(len(data)))

    def as_tendencies(self):
        """
        Calculate tendencies from the raw_data
        :return: A numpy array
        """
        return None

    @classmethod
    def from_scm_conf(cls, var, conf):
        var_conf = conf[DATA_SECTION][var]

        if isinstance(var_conf, np.ndarray) or isinstance(var_conf, list):
            data = np.array(var_conf)
        else:
            if 'filename' not in var_conf:
                raise ValueError('filename for not specified for {} data'.format(var))

            data = load_from_nc(var_conf)

        n = cls(var)
        n.set_data(data)
        return n
