import netCDF4 as nc
import numpy as np

from snag.vertical_interp import vert_interp, calc_tendencies, model_levels_nml
from snag.utils import extract_vars, to_np


DATA_SECTION = 'data'


def load_from_nc(var, conf):
    ds = nc.Dataset(conf['filename'])
    conf.setdefault('scale_factor', 1.0)
    conf.setdefault('variable', var)

    return extract_vars(ds, conf['variable'], scale_factor=conf['scale_factor'])


class GriddedVariable(object):
    """
    A single gridded data variable

    Used for calculating the IC, BCs and tendencies
    """

    def __init__(self, var_name):
        self.var_name = var_name
        self._data = None
        self._levels = None
        self._dts = None

    def set_data(self, data):
        self._levels, self._data = self._vertical_interpolation(data)
        self._dts = data.coords['time']

    def _vertical_interpolation(self, data):
        # Pass through to call Jono's script
        return vert_interp(to_np(data), self.var_name, to_np(data.coords['height']))

    def as_tendencies(self):
        """
        Calculate tendencies from the raw_data
        :return: A numpy array
        """
        return calc_tendencies(self._data, self._dts)

    @classmethod
    def from_scm_conf(cls, var, conf):
        var_conf = conf[DATA_SECTION][var]

        if isinstance(var_conf, np.ndarray) or isinstance(var_conf, list):
            data = np.array(var_conf)
        else:
            if 'filename' not in var_conf:
                raise ValueError('filename for not specified for {} data'.format(var))

            data = load_from_nc(var, var_conf)

        n = cls(var)
        n.set_data(data)
        return n
