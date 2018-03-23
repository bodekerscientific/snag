# code copied from snag/__init__.py
# create_namelist

import yaml
from six import string_types

from snag.namelist import Namelist
from snag.serialize import dump
from snag.utils import merge_dicts
from snag.version import version as __version__

from logging import basicConfig

basicConfig()


conf = r'D:\code-GitHub\snag\examples\mcmurdo_land.yml'

if isinstance(conf, string_types):
    conf = yaml.load(open(conf))

nl = Namelist(conf)
#nl.variables['w'][:] = 0

# set all vertical fluxes to 0 for test case
nl.config['INPROF']['wi'][:] = 0
nl.config['INPROF']['w_advi'][:] = 0
nl.config['INOBSFOR']['w_inc'][:] = 0
nl.config['INOBSFOR']['w_bg'][:] = 0

try:
    nl.validate()
except:
    pass

dump(nl.as_dict(),stream=open('namelist_L85_ARM_MCMURDO_test_land9.scm','w'))

# plot

import matplotlib.pylab as plt
import numpy as np

plt.plot(nl.config['INPROF']['qi'])
plt.plot(nl.config['INPROF']['theta'])
plt.plot(nl.config['INPROF']['ui'])
plt.plot(nl.config['INPROF']['vi'])
plt.plot(nl.config['INPROF']['wi'])


plt.imshow(np.transpose(nl.config['INOBSFOR']['t_inc']),origin=0)

plt.colorbar()

plt.close()

