"""
code to check options specified in yml file are consistent. reads in configuration dictionary (config) before writing to file
"""

import numpy as np

from snag.exceptions import ValidationError


def validate_land_points(config):
    if config['CNTLSCM']['land_points'] == 1 and config['LOGIC']['land_sea_mask']:
        # print('Land or coastal case chosen')
        pass
    elif config['CNTLSCM']['land_points'] == 0 and not config['LOGIC']['land_sea_mask']:
        # print('Sea case chosen')
        pass
    else:
        return ['Incorrect combination of CNTLSCM:land_points and LOGIC:land_sea_mask']
    return []


def validate_land_ice_soil(config):
    if config['CNTLSCM']['land_points'] == 1:  # only check for land case
        if config['LOGIC']['land_ice_mask'] and not config['LOGIC']['soil_mask']:
            print('Land ice subsurface chosen')
        elif not config['LOGIC']['land_ice_mask'] and config['LOGIC']['soil_mask']:
            print('Land soil subsurface chosen')
        else:
            return ['Incorrect combination of LOGIC:land_ice_mask and LOGIC:soil_mask']
        return []


def validate_fland_ctile(config):
    if config['CNTLSCM']['land_points'] == 1 and config['RUNDATA']['fland_ctile'] == 1:
        print('100% Land case chosen')
    elif config['CNTLSCM']['land_points'] == 1 and config['RUNDATA']['fland_ctile'] > 0 and config['RUNDATA']['fland_ctile'] < 1:
        print('Coastal case chosen')
    elif config['CNTLSCM']['land_points'] == 0 and config['RUNDATA']['fland_ctile'] == 0:
        print('Sea case chosen')
    else:
        return ['Incorrect combination of CNTLSCM:land_points and RUNDATA:fland_ctile']
    return []


def validate_soil_type(config):
    if config['CNTLSCM']['land_points'] == 1 and config['LOGIC']['land_ice_mask'] and config['INDATA']['soil_type'] == 1:
        pass
    elif config['CNTLSCM']['land_points'] == 1 and config['LOGIC']['soil_mask'] and 1 < config['INDATA']['soil_type'] <= 3:
        pass
    elif config['CNTLSCM']['land_points'] == 0:
        pass
    else:
        return ['Incorrect combination of LOGIC:land_ice_mask and INDATA:soil_type']
    return []


def validate_suface_diag(config):
    # check correct diagnostics output
    if config['CNTLSCM']['land_points'] == 1 and not config['DIAGS']['l_SCMDiag_sea'] and config['DIAGS']['l_SCMDiag_land']:
        # print('Land diagnostics output')
        pass
    elif config['CNTLSCM']['land_points'] == 0 and config['DIAGS']['l_SCMDiag_sea'] and not config['DIAGS']['l_SCMDiag_land']:
        # print('Sea diagnostics output')
        pass
    else:
        return ['Incorrect value for DIAGS:l_SCMDiag_sea or DIAGS:l_SCMDiag_land']
    return []


def validate_number_soil_layers(config):
    if config['CNTLSCM']['land_points'] == 1:  # only check for land case
        # check if soil layers are consistent for soil moisture and temperature. only needed for two options
        if config['INJULES']['smi_opt'] == 0:
            if len(config['INPROF']['t_deep_soili']) != len(config['INJULES']['smcli']):
                return ['different number of soil layers specified in INPROF:t_deep_soili and INJULES:smcli']
        if config['INJULES']['smi_opt'] == 2:
            if len(config['INPROF']['t_deep_soili']) != len(config['INJULES']['sth']):
                return ['different number of soil layers specified in INPROF:t_deep_soili and INJULES:sth']


def validate_length_of_simulation(config):
    forcing_length_s = config['INOBSFOR']['obs_pd'] * config['CNTLSCM']['nfor']
    requested_length_s = config['RUNDATA']['ndayin'] * 86400 + config['RUNDATA']['nminin'] * 60 + config['RUNDATA']['nsecin']
    if int(forcing_length_s) != int(requested_length_s):
        return ['stated length of forcing data (INOBSFOR:obs_pd * CNTLSCM:nfor does not match days requested in RUNDATA']
    return []


def validate_obs_forcing(config):
    # check that observational forcing variables have no nan's and are correct length (nfor * model_levels_nml)
    errors = []
    if config['LOGIC']['obs']:
        for var in ['t_inc', 'q_star', 'u_inc', 'v_inc', 'w_inc', 't_bg', 'q_bg', 'u_bg', 'v_bg', 'w_bg']:
            if var not in config['INOBSFOR']:
                errors.append('Variable {} is not present in INOBSFOR'.format(var))
                continue

            if var in ['w_inc', 'w_bg']:  # w forcing has extra layer
                if config['INOBSFOR'][var].shape != (config['CNTLSCM']['nfor'], (config['CNTLSCM']['model_levels_nml'] + 1)):
                    errors.append('Incorrect shape of forcing variable {}'.format(var))
            elif config['INOBSFOR'][var].shape != (config['CNTLSCM']['nfor'], config['CNTLSCM']['model_levels_nml']):
                errors.append('Incorrect shape of forcing variable {}'.format(var))
            if np.any(np.isnan(config['INOBSFOR'][var])):
                errors.append('Nan values in forcing variable {}'.format(var))
    return errors


def validate_intial_state(config):
    errors = []
    # check that intial state variables have no nan's and are the correct length,
    for var in ['p_in', 'theta', 'qi', 'ui', 'vi', 'wi', 'w_advi']:
        if var not in config['INPROF']:
            errors.append('Variable {} is not present in INPROF'.format(var))
            continue
        if var in ['p_in', 'wi', 'w_advi']:  # w variables have extra layer
            if len(config['INPROF'][var]) != (config['CNTLSCM']['model_levels_nml'] + 1):
                errors.append('Incorrect length of forcing variable {}'.format(var))
        elif len(config['INPROF'][var]) != config['CNTLSCM']['model_levels_nml']:
            errors.append('Incorrect length of forcing variable {}'.format(var))
        if np.any(np.isnan(config['INPROF'][var])):
            errors.append('Nan values in inital profile of {}'.format(var))
    return errors


def validate_JULES_tiles(config):
    if config['CNTLSCM']['land_points'] == 1: # only check for land case
        # check the length of JULES tiles:
        errors = []
        vars = [
            ('frac_typ', 9),
            ('z0_tile', 9),
            ('tstar_tile', 9),
            ('catch', 9),
            ('canopy', 9),
            ('infil_tile', 9),
            ('snow_tile', 9),
            ('rgrain', 9),
            ('canht', 5),
            ('lai', 5)
        ]
        for v, expected_len in vars:
            if v not in config['INJULES']:
                errors.append('Variable {} is not present in INJULES'.format(v))
            elif len(config['INJULES'][v]) != expected_len: # Can't take the length of an int or a float
                errors.append('Incorrect length of Jules parameter {}. Expected length of {}'.format(v, expected_len))

        try:
            if not isinstance(config['INJULES']['smi_opt'], int):
                errors.append('Expected Jules parameter smi_opt to be an int')
        except KeyError:
            errors.append('Variable smi_opt is not present in INJULES')

        try:
            if not isinstance(config['INJULES']['gs'], float):
                errors.append('Expected Jules parameter gs to be a float')
        except KeyError:
            errors.append('Variable gs is not present in INJULES')
        return errors


def validate_surface_forcing(config):
    errors = []
    if config['LOGIC']['obs_surf']:
        # check if at least one variable available
        if 'tstar_forcing' not in config['INOBSFOR'] and 'flux_h' not in config['INOBSFOR']:
            errors.append('no surface observation forcing (t_star_forcing or flux_h) available')

        # check length of variables that are there
        for var in ['flux_h', 'flux_e', 'tstar_forcing']:
            try:
                if len(config['INOBSFOR'][var]) != config['CNTLSCM']['nfor']:
                    errors.append('surface forcing variables {} does not match nfor'.format(var))
            except KeyError:
                pass
    return errors


def validate_nml_style(config):
    if config['LOGIC']['obs'] == True and config['INOBSFOR']['old_nml'] == True:
        return ['Old style observation forcing (old_nml) specified. SNAG creates new style formatting. Check']
    return []
