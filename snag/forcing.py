class BaseForcing(object):
    def __init__(self, conf):
        self.forcing_conf = conf

    def check_if_active(self, conf):
        """
        Check if this type of forcing is to be applied.

        TODO: I don't really like this interface
        :param conf:
        :return:
        """
        return False

    def get_params(self, variables):
        """
        Get the configuration which is written to the namelist

        This function should convert the Forcing instance to a dict object which is subsequently merged with other forcing and configuration
        to produce the final output
        :return: Dict
        """
        raise NotImplementedError()


class StatisticalForcing(BaseForcing):
    def check_if_active(self, conf):
        return 'stats' in conf['LOGIC'] and conf['LOGIC']['stats']

    def get_params(self, variables):
        return {
            'LOGIC': {
                'stats': True,
                'altdat': True
            }
        }


class ObservationalForcing(BaseForcing):
    def check_if_active(self, conf):
        return 'obs' in conf['LOGIC'] and conf['LOGIC']['obs']

    def get_params(self, variables):
        conf = {
            'LOGIC': {
                'obs': True,
                # 'obs_pd':
            },
            'INPROF': {},
            'INOBSFOR': {}
        }

        for v in ('u', 'v', 'w'):
            conf['INPROF']['{}i'.format(v)] = variables[v].initial_profile()
            conf['INOBSFOR']['{}_inc'.format(v)] = variables[v].as_tendencies()

        # Initialise initial vertical advection profile # TODO (jono) figure out some logic around this
        conf['INPROF']['w_advi'] = variables['w'].initial_profile()

        # Specific humidity uses qstar instead of q_inc for the tendencies
        conf['INPROF']['qi'] = variables['q'].initial_profile()
        conf['INOBSFOR']['q_star'] = variables['q'].as_tendencies()

        # Add pressure and theta levels
        conf['INPROF']['p_in'] = variables['p'].initial_profile()
        conf['INPROF']['theta'] = variables['theta'].initial_profile()

        conf['INOBSFOR']['t_inc'] = variables['t'].as_tendencies()

        # Write out the background states
        for v in ('t', 'q', 'u', 'v', 'w'):
            conf['INOBSFOR']['{}_bg'.format(v)] = variables[v].data[:] # includes initial state

        # TODO: handle surfaces

        return conf


# class RevealedForcing(BaseForcing):
#     def get_params(self, variables):
#         return {
#             'LOGIC': {
#                 'l_vertadv': True
#             }
#         }
#
# RELAXATION_DISABLED = 0
# RELAXATION_INITIAL_TAU = 0
# RELAXATION_BG_TAU = 0
# RELAXATION_INITIAL = 0
# RELAXATION_BG = 0
#
#
# class RelaxationForcing(BaseForcing):
#
#     def get_params(self, variables):
#         return {
#             ''
#         }


forcings = {
    'obs': ObservationalForcing,
    # 'stat': StatisticalForcing,
    # 'revealed': RevealedForcing,
    # 'relaxation': RelaxationForcing,
}
