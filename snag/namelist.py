from collections import OrderedDict
from logging import getLogger

from snag import namelist_checks
from snag.exceptions import ValidationError
from snag.forcing import forcings
from snag.grid import GriddedVariable, DATA_SECTION, VALID_VARIABLES
from snag.serialize import dump

logger = getLogger(__name__)

DEFAULT_NAMELIST_SECTIONS = [
    'CNTLSCM',
    'INDATA',
    'RUNDATA',
    'NC_OBS',
    'LOGIC',
    'INJULES',
    'INGWD',
    'INPROF',
    'INGEOFOR',
    'PHYSWITCH',
    'RADCLOUD',
    'INOBSFOR',
    'DIAGS',
]


def check_value_eq(conf, variable, expected, message=None):
    """
    Prints a warning if a config variable is set and not what is expected

    :param conf: A dictlike object
    :param variable: The variable to check
    :param expected: The expected value to compare against
    :param message: The message to print. If None is passed a generic message is printed
    :return: True if the value if absent or correct
    """
    if message is None:
        message = '{} does not match the expected value of {}'.format(variable, expected)

    # Assumes two level indexing
    if variable in conf and conf[variable] != expected:
        logger.warning(message)
        return False
    return True


class Namelist(object):
    """
    All the configuration needed for a single SCM model run
    """

    def __init__(self, conf):
        """
        Initialise the NamelistConf with configuration
        :param conf: A dict-like object containing the paths to the input data and model configuration parameters
        """
        self._raw_conf = conf
        self.variables = {}
        for v in VALID_VARIABLES:
            try:
                self.variables[v] = GriddedVariable.from_scm_conf(v, conf)
            except KeyError:
                raise ValidationError(
                    'Could not parse data source for variable {}. Check \'{}\' section'.format(v, DATA_SECTION))
        self.variables['theta'] = GriddedVariable.calculate_theta(self.variables['p'], self.variables['t'], )

        # Update any dates/levels that were not explicitly specified
        for v in self.variables:
            if self.variables[v]._dts is None:
                self.variables[v]._dts = self.variables['p']._dts
                self.variables[v].levels = self.variables['p'].levels

        # Instantiate the forcings
        self.forcings = []
        if 'forcing' in conf:
            for f in conf['forcing']:
                try:
                    Forcing = forcings[f]
                    self.forcings.append(Forcing(conf['forcing'][f]))
                except KeyError:
                    raise ValueError('No such forcing named {}'.format(f))

        self.config = self.as_dict()

    def dump(self, stream=None):
        """
        Dump the namelist to a stream or string if not stream is provided

        :param stream: A stream like object for example an open file. If nothing is provided then a string containing the configuration is returned
        :return:
        """
        self.validate()
        return dump(self.config, stream)

    def validate(self):
        checks = [f for name, f in namelist_checks.__dict__.items() if name.startswith('validate_')]
        errors = []
        for v in checks:
            try:
                errors.extend(v(self.config) or [])
            except KeyError as e:
                errors.append('Could not find configuration parameter: {}'.format(e.args[0]))

        if len(errors):
            for e in errors:
                logger.error(e)
            raise ValidationError('Could not create a valid namelist')

    def _set_dt_config(self, conf):
        start_dt, end_dt = self.variables['p'].datetime_span()
        nforcings = len(self.variables['p'].data) # includes initial time

        # Loop over the various date/time variables and check if they have been set correctly
        for v, attr in (('year_init', 'year'), ('month_init', 'month'), ('day_init', 'day'), ('hour_init', 'hour'), ('min_init', 'minute'),
                        ('sec_init', 'second')):
            value = getattr(start_dt, attr)
            check_value_eq(conf['INDATA'], v, value, 'INDATA.{} does not match the extracted value obtained from the input data'.format(v))
            # Always override the set values with the startdate extracted from the input data
            conf['INDATA'][v] = value

        # Set the number of forcing steps
        check_value_eq(conf['CNTLSCM'], 'nfor', nforcings)
        conf['CNTLSCM']['nfor'] = nforcings

        # Set the run length
        sim_length = end_dt - start_dt
        check_value_eq(conf['RUNDATA'], 'ndayin', sim_length.days)
        conf['RUNDATA']['ndayin'] = sim_length.days
        check_value_eq(conf['RUNDATA'], 'nminin', sim_length.seconds // 60)
        conf['RUNDATA']['nminin'] = sim_length.seconds // 60
        check_value_eq(conf['RUNDATA'], 'nsecin', sim_length.seconds % 60)
        conf['RUNDATA']['nsecin'] = sim_length.seconds % 60

    def as_dict(self):
        """
        Creates a Python Dict of the content of the namelist

        This is used to serialise the namelist to file
        :return: Dict
        """

        snag_config = OrderedDict()
        for sec in DEFAULT_NAMELIST_SECTIONS:
            snag_config[sec] = OrderedDict()

        for k in DEFAULT_NAMELIST_SECTIONS:
            if k in self._raw_conf and self._raw_conf[k] is not None:
                snag_config[k].update(self._raw_conf[k])

        self._set_dt_config(snag_config)

        # Process the forcings
        for forcing in self.forcings:
            forcing_conf = forcing.get_params(self.variables)
            for k in forcing_conf:
                snag_config[k].update(forcing_conf[k])

        snag_config['RUNDATA']['ozone'] = self.variables['ozone'].initial_profile() # TODO needs to select timestep based on month

        # Override with explicitly set params
        for k in DEFAULT_NAMELIST_SECTIONS:
            if k in self._raw_conf and self._raw_conf[k] is not None:
                snag_config[k].update(self._raw_conf[k])

        return snag_config
