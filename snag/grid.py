import netCDF4 as nc
import numpy as np

from snag.utils import extract_vars, to_np
from snag.vertical_interp import vert_interp, calc_tendencies

DATA_SECTION = 'data'


VARIABLE_DEFAULTS = {
    'p': {
        'grid': 'rho_with_model_top',
        'units': 'Pa'
    },
    't': {
        'grid': 'theta_without_surf',
        'units': 'K'
    },
    'q': {
        'grid': 'theta_without_surf',
        'units': 'kg/kg'
    },
    'u': {
        'grid': 'rho',
        'units': 'm s-1'
    },
    'v': {
        'grid': 'rho',
        'units': 'm s-1'
    },
    'w': {
        'grid': 'theta',
        'units': 'm s-1'
    },
    'ozone': {
        'grid': 'theta_without_surf',
        'units': 'kg/kg'
    },
    'theta': {
        'grid': 'theta_without_surf',
        'units': 'K',
        'required': False
    },
}

VALID_VARIABLES = VARIABLE_DEFAULTS.keys()


def load_from_nc(var, conf):
    ds = nc.Dataset(conf['filename'])
    conf.setdefault('variable', var)
    conf.setdefault('units', None)
    conf.setdefault('time_variable', 'time')
    conf.setdefault('vertical_variable', 'height')

    return extract_vars(ds, conf['variable'], target_units=conf['units'], time_variable=conf['time_variable'],
                        vertical_variable=conf['vertical_variable'])


class GriddedVariable(object):
    """
    A single gridded data variable

    Used for calculating the IC, BCs and tendencies
    """

    def __init__(self, var_name, var_config=None):
        assert var_name in VARIABLE_DEFAULTS
        self.var_name = var_name
        # update the config if available
        self.config = VARIABLE_DEFAULTS[var_name]
        if var_config is not None:
            self.config.update(var_config)

        self.data = None
        self.levels = None
        self._dts = None

    def set_data(self, data):
        self.levels, self.data = vert_interp(to_np(data), self.var_name, to_np(data.coords['height']),
                                             vertical_grid=self.config['grid'])
        self._dts = data.coords['time']

    def _vertical_interpolation(self, data):
        # Pass through to call Jono's script
        return

    def initial_profile(self):
        return list(self.data[0])

    def as_tendencies(self):
        """
        Calculate tendencies from the raw_data
        :return: A numpy array
        """
        return calc_tendencies(self.data, self._dts)

    @classmethod
    def from_scm_conf(cls, var, conf):
        try:
            var_conf = conf[DATA_SECTION][var]
        except KeyError:
            # Check if the variable is required. IF it isn't required return None, else raise an exception
            if var in VARIABLE_DEFAULTS and not VARIABLE_DEFAULTS[var].get('required', True):
                return None
            raise

        if isinstance(var_conf, np.ndarray) or isinstance(var_conf, list):
            # Use numpy array if available
            data = np.array(var_conf)
            n = cls(var)
        else:
            if 'filename' not in var_conf:
                if 'filename' in conf[DATA_SECTION]:
                    var_conf['filename'] = conf[DATA_SECTION]['filename']
                else:
                    raise ValueError('filename for not specified for {} data'.format(var))

            n = cls(var, var_conf)
            data = load_from_nc(var, n.config)

        n.set_data(data)
        return n

    @classmethod
    def calculate_theta(cls, press, temp):
        # Regrid press to temp vertical levels
        levels, press_regridded = vert_interp(press.data, 'p', press.levels, temp.config['grid'])
        theta = temp.data * np.power(100000.0 / press_regridded, 0.286) # pressure in Pa

        # Load up the GriddedVariable instance
        n = cls('theta')
        n.data = theta
        n.levels = levels
        n._dts = press._dts

        return n