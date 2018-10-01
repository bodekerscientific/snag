# code copied from snag/__init__.py
# create_namelist

import yaml
import datetime as dt
from six import string_types

from snag.namelist import Namelist
from snag.serialize import dump
from snag.utils import merge_dicts
from snag.version import version as __version__

from logging import basicConfig
from utils import make_regular_timeseries
basicConfig()


datetime_list = make_regular_timeseries(dt.datetime(2016, 01, 01), dt.datetime(2016, 01, 30), 86400)

for i, dt1 in enumerate(datetime_list):

    conf = 'D:/code-GitHub/snag/examples/mcmurdo_land.yml'

    if isinstance(conf, string_types):
        conf = yaml.load(open(conf))

    conf['data']['filename'] = 'T:/DSC-SCM/SCM_INPUT/ver2/Blended_ARM_data_{}{:02}{:02}_30min.nc'.format(dt1.year, dt1.month, dt1.day)
    conf['INDATA']['year_init'] =  int(dt1.year)
    conf['INDATA']['month_init'] = int(dt1.month)
    conf['INDATA']['day_init'] = int(dt1.day)

    # create a namelist object and initialise the variables including the tendencies
    nl = Namelist(conf)

    # set all vertical fluxes to 0 for test case
    nl.config['INPROF']['wi'][:] = 0
    nl.config['INPROF']['w_advi'][:] = 0
    nl.config['INOBSFOR']['w_inc'][:] = 0
    nl.config['INOBSFOR']['w_bg'][:] = 0

    # try validate it first (also validates on dump)
    try:
        nl.validate()
    except:
        pass

    # dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/namelist_ARM_MCMURDO_land_{}{:02}{:02}_30min.scm'.format(dt1.year, dt1.month, dt1.day), 'w'))
    dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/ensemble_namelists/group02/namelist_ARM_MCMURDO_land_{:02}.scm'.format(i), 'w'))
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

