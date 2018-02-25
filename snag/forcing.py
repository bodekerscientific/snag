class Forcing(object):
    def get_params(self, variables):
        """
        Get the configuration which is written to the namelist

        This function should convert the Forcing instance to a dict object which is subsequently merged with other forcing and configuration
        to produce the final output
        :return: Dict
        """
        raise NotImplementedError()


class StatisticalForcing(Forcing):
    def get_params(self, variables):
        return {
            'LOGIC': {
                'stats': True,
                'altdat': True
            }
        }


class ObservationalForcing(Forcing):
    def get_params(self, variables):
        conf = {
            'LOGIC': {
                'obs': True,
                # 'obs_pd':
            },
        }

        for v in ('u', 'v', 'w'):
            conf['INPROF']['{}i'.format(v)] = variables[v].initial_profile()
            conf['INOBSFOR']['{}_inc'.format(v)] = variables[v].as_tendencies()

        # Relative humidity uses qstar instead of q_inc for the tendencies
        conf['INPROF']['qi'] = variables['q'].initial_profile()
        conf['INOBSFOR']['q_star'] = variables['q'].as_tendencies()

        # Add pressure and theta levels
        #TODO: Implement
        conf['INOBSFOR']['p_in'] = variables['p'].as_tendencies()
        conf['INOBSFOR']['q_star'] = variables['theta'].as_tendencies()

        #TODO: handle surfaces

        return conf


class RevealedForcing(Forcing):
    def get_params(self, variables):
        return {
            'LOGIC': {
                'l_vertadv': True
            }
        }

RELAXATION_DISABLED = 0
RELAXATION_INITIAL_TAU = 0
RELAXATION_BG_TAU = 0
RELAXATION_INITIAL = 0
RELAXATION_BG = 0


class RelaxationForcing(Forcing):

    def get_params(self, variables):
        return {
            ''
        }


forcings = {
    'stat': StatisticalForcing,
    'obs': StatisticalForcing,
    'revealed': StatisticalForcing,
    'relaxation': StatisticalForcing,
}
