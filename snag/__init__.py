__version__ = '0.0.2'

import f90nml
import yaml
from six import string_types

DATA_SECTION = 'input'

from snag.namelist import Namelist


def create_namelist(output_fh, conf):
    """
    Create a new SCM namelist file given a dictionary containing the
    :param fh:
    :param conf: Dict-like object or a filename to a yaml file containing the configuration
    :return:
    """
    if isinstance(conf, string_types):
        conf = yaml.load(conf)

    loaded_conf = Namelist(conf)
    nml = f90nml.Namelist(loaded_conf.as_dict())
    nml.write(output_fh)
