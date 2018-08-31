# code copied from snag/__init__.py
# create_namelist

import yaml
import datetime as dt
from six import string_types
import numpy as np
import netCDF4 as nc

from snag.namelist import Namelist
from snag.serialize import dump
from snag.utils import merge_dicts
from snag.version import version as __version__

from logging import basicConfig
from utils import make_regular_timeseries

basicConfig()

lat = -61.625
lon = 165.9375
num_days = 15  # number of days in input file
out_dt = 21600  # timestep (s) of input data

datetime_list = make_regular_timeseries(dt.datetime(2000, 1, 1, 12), dt.datetime(2000, 12, 31, 12), 86400)

for ii, i in enumerate(range(0, len(datetime_list), num_days - 1)):
    dt1 = datetime_list[i]

    conf = 'D:/code-GitHub/snag/examples/southern_ocean_basic.yml'

    if isinstance(conf, string_types):
        conf = yaml.load(open(conf))

    conf['data'][
        'filename'] = 'T:/DSC-SCM/scm_input/NZESM/NZESM_nudged_{}days_{}{:02}{:02}_lat{:.3f}_lon{:.3f}.nc'.format(num_days, dt1.year, dt1.month,
                                                                                                                  dt1.day, lat, lon)
    conf['INDATA']['year_init'] = int(dt1.year)
    conf['INDATA']['month_init'] = int(dt1.month)
    conf['INDATA']['day_init'] = int(dt1.day)
    conf['INDATA']['hour_init'] = 13
    conf['INDATA']['min_init'] = 0
    conf['INDATA']['sec_init'] = 0
    conf['CNTLSCM']['nfor'] = num_days * (86400 / out_dt)
    conf['RUNDATA']['ndayin'] = num_days - 1
    conf['RUNDATA']['nminin'] = (out_dt * ((86400 / out_dt) - 1)) / 60
    nc_file = nc.Dataset(conf['data']['filename'])

    # conf['INPROF']['tstari'] = np.round(np.mean(nc_file.variables['surface_temperature'][:]),2)
    # conf['RUNDATA']['tstar_sea'] = np.round(np.mean(nc_file.variables['surface_temperature'][:]),2)

    nl = Namelist(conf)
    # nl.variables['w'][:] = 0

    # set all vertical fluxes to 0 for test case
    # nl.config['INPROF']['wi'][:] = 0
    # nl.config['INPROF']['w_advi'][:] = 0
    # nl.config['INOBSFOR']['w_inc'][:] = 0
    # nl.config['INOBSFOR']['w_bg'][:] = 0

    try:
        nl.validate()
    except:
        pass

    # dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/namelist_ARM_MCMURDO_land_{}{:02}{:02}_30min.scm'.format(dt1.year, dt1.month, dt1.day), 'w'))
    dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/ensemble_namelists/group04/namelist_STH_OCEAN_{:02}.scm'.format(ii), 'w'))
# plot

# import matplotlib.pylab as plt
# import numpy as np
#
# plt.plot(nl.config['INPROF']['qi'])
# plt.plot(nl.config['INPROF']['theta'])
# plt.plot(nl.config['INPROF']['ui'])
# plt.plot(nl.config['INPROF']['vi'])
# plt.plot(nl.config['INPROF']['wi'])
#
#
# plt.imshow(np.transpose(nl.config['INOBSFOR']['t_inc']),origin=0)
#
# plt.colorbar()
#
# plt.close()
