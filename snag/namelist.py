from collections import defaultdict, OrderedDict

from snag.forcing import forcings
from snag.grid import GriddedVariable, DATA_SECTION, VALID_VARIABLES

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
        for v in VALID_VARIABLES:
            try:
                self.variables[v] = GriddedVariable.from_scm_conf(v, conf)
            except KeyError:
                raise ValidationError('Could not parse data source for variable {}. Check \'{}\' section'.format(v, DATA_SECTION))
        self.variables['theta'] = GriddedVariable.calculate_theta(self.variables['p'], self.variables['t'],)

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
        for sec in DEFAULT_NAMELIST_SECTIONS:
            snag_config[sec] = OrderedDict()

        # create the initial conditions
        for v in ('u', 'v', 'w', 'theta'):
            snag_config['INPROF']['{}i'.format(v)] = self.variables[v].initial_profile()
        snag_config['INPROF']['p_in'] = self.variables['p'].initial_profile()

        # Process the forcings
        for forcing in self.forcings:
            forcing.get_params(self.variables)

        # Override the configuration with the default sections. Note that the overridden configuration is not validated.
        for k in DEFAULT_NAMELIST_SECTIONS:
            if k in self._raw_conf and self._raw_conf[k] is not None:
                snag_config[k].update(self._raw_conf[k])

        return snag_config
