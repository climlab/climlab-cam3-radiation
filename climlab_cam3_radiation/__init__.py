__version__ = '0.3.1'

#  import everything from the fortran object
from ._cam3 import *
import xarray as xr
import pooch


_datapath_http = "http://www.atmos.albany.edu/facstaff/brose/resources/climlab_data/"

def init_cam3(mod):
    # Initialise absorptivity / emissivity data
    remotepath_http = _datapath_http + 'absorptivity/abs_ems_factors_fastvx.c030508.nc'
    filehandle = pooch.retrieve(url=remotepath_http,
        known_hash="261043a01b15ebb82ba2baa71311a6807ba9ea6d720baa15bc091f0e61b2a8f2")
    data = xr.open_dataset(filehandle)
    #  Populate storage arrays with values from netcdf file
    for field in ['ah2onw', 'eh2onw', 'ah2ow', 'ln_ah2ow', 'cn_ah2ow', 'ln_eh2ow', 'cn_eh2ow']:
        setattr(mod, field, data[field].transpose())

init_cam3(absems)
