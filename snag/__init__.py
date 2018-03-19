from collections import OrderedDict

import yaml
from six import string_types

from snag.namelist import Namelist
from snag.serialize import dump
from snag.utils import merge_dicts
from snag.version import version as __version__


def create_namelist(conf, stream=None):
    """
    Create a new SCM namelist file given a dictionary containing the
    :param conf: Dict-like object or a filename to a yaml file containing the configuration
    :param stream: A stream like object for example an open file. If nothing is provided then a string containing the configuration is returned
    :return:
    """
    if isinstance(conf, string_types):
        conf = yaml.load(open(conf))

    nl = Namelist(conf)
    return nl.dump(stream)
