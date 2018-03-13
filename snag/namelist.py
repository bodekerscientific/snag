from collections import defaultdict, OrderedDict

from snag.forcing import forcings
from snag.grid import GriddedVariable, DATA_SECTION

DEFAULT_NAMELIST_SECTIONS = [
    'CNTLSCM',
    'INDATA',
    'RUNDATA',
    'NC_OBS',
    'DIAGS',
    'LOGIC',
    'INGWD',
    'INPROF',
    'INOBSFOR',
    'INGEOFOR',
    'RADCLOUD',
    'PHYSWITCH',
]

VARIABLES = [
    'q', 'u', 'v', 'w', 'ozone'
]

COORD_VARIABLES = [
    'p', 'theta'
]


class ValidationError(Exception):
    pass


class Namelist(object):
    """
    All the configuration needed for a single SCM model run
    """

    def __init__(self, conf):
        """
        Initialise the NamelistConf with configuration
        :param conf: A dict-like object containing the
        """
        self._raw_conf = conf
        self.variables = {}
        for v in VARIABLES + COORD_VARIABLES:
            try:
                self.variables[v] = GriddedVariable.from_scm_conf(v, conf)
            except KeyError:
                raise ValidationError('Could not parse data source for variable {}. Check \'{}\' section'.format(v, DATA_SECTION))

        # Instantiate the forcings
        self.forcings = {}
        if 'forcings' in conf:
            for f in conf['forcings']:
                try:
                    Forcing = forcings[f]
                    self.forcings[f] = Forcing(conf['forcings'][f])
                except KeyError:
                    raise ValueError('No such forcing named {}'.format(f))

    def validate(self):
        pass

    def as_dict(self):
        """
        Creates a Python Dict of the content of the namelist

        This is used to serialise the namelist to file
        :return: Dict
        """

        snag_config = OrderedDict()

        # create the initial conditions
        for v in ('u', 'v', 'w', 'theta'):
            conf['INPROF']['{}i'.format(v)] = self.variables[v].initial_profile()
        conf['INPROF']['p_in'] = self.variables['p'].initial_profile()

        # Process the forcings
        for forcing in self.forcings:
            forcing.get_params(self.variables)

        # Override the configuration with the 'overrides' key. Note that the overridden configuration is not validated.
        if 'overrides' in self._raw_conf:
            for k in self._raw_conf['overrides']:
                conf[k].update(self._raw_conf['overrides'][k])

        return conf
