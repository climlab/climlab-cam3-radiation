import numpy as np
import pytest
from climlab_cam3_radiation import driver, absems


#### Define thermodynamic and physical constants
g = 9.8          # gravitational acceleration (m / s**2)
Cpd = 1004.      # specific heat at constant pressure for dry air (J / kg / K)
stebol = 5.67E-8 #  Stefan-Boltzmann constant (W / m**2 / K**4)
Rd = 287.         # gas constant for dry air (J / kg / K)
Rv = 461.5       # gas constant for water vapor (J / kg / K)epsilon = Rd / Rv
epsilon = Rd / Rv

#### Set up the pressure domain
# CAM3 radiation code expects arrays with 3D arrays with (KM, JM, 1)
#        and 2D arrays with (JM, 1).
# and with element 0 corresponding to the TOP
ps = 1000. #  Surface pressure in hPa
KM = 30  # number of pressure levels
JM = 1   # number of columns
IM = 1   # number of longitudes
deltap = ps / KM  # pressure interval
#plev = np.linspace(0., ps, KM+1)  # pressure bounds
#plev = plev[..., np.newaxis, np.newaxis]
p = np.linspace(deltap/2., ps-deltap/2., KM)
p = p[..., np.newaxis]
#   why are we passing missing instead of the actual layer thicknesses?
dp = np.zeros_like(p) - 99. # set as missing
# Set the temperatures
#  Using a linearly decreasing temperature from surface to TOA
Ts = 288.
Tatm = np.linspace(200., 288.-10., KM)
Tatm = Tatm[..., np.newaxis, np.newaxis]

do_sw = 1   # '1=do, 0=do not compute SW'
do_lw = 1   # '1=do, 0=do not compute LW'
in_cld = 0  # '1=in-cloud, 0=grid avg cloud water path'

# atmospheric composition
# specific humidity profile computed from those temperatures using Manabe's
# fixed relative humidity profile
specific_humidity = np.array([4.13141097e-03, 3.41509495e-03, 2.81099479e-03, 2.30359570e-03,
       1.87920573e-03, 1.52578624e-03, 1.23279279e-03, 9.91026303e-04,
       7.92494475e-04, 6.30283118e-04, 4.98437246e-04, 3.91851633e-04,
       3.06170488e-04, 2.37695932e-04, 1.83304857e-04, 1.40373783e-04,
       1.06711275e-04, 8.04974602e-05, 6.02302082e-05, 4.46774859e-05,
       3.28354282e-05, 2.38916443e-05, 1.71932832e-05, 1.22193649e-05,
       8.55682965e-06, 5.87957411e-06, 5.00000000e-06, 5.00000000e-06,
       5.00000000e-06, 5.00000000e-06])
q = specific_humidity[::-1, np.newaxis, np.newaxis]
# Convert to volume mixing ratio from mass mixing ratio
#  just multiplying by ratio of molecular weights of H2O and dry air
#  A global-mean ozone climatology
O3vmr = np.array([2.25573888e-08, 2.38730436e-08, 2.52586476e-08, 2.66442517e-08,
       2.80298557e-08, 2.97254145e-08, 3.14254923e-08, 3.31238355e-08,
       3.46767916e-08, 3.62297478e-08, 3.76122833e-08, 3.86410454e-08,
       3.96698075e-08, 4.08899052e-08, 4.21303310e-08, 4.39781220e-08,
       4.60528063e-08, 4.87636254e-08, 5.16974065e-08, 5.57122567e-08,
       6.17914190e-08, 7.15771368e-08, 9.29020109e-08, 1.29109217e-07,
       1.75914529e-07, 2.45552383e-07, 3.92764464e-07, 7.61726407e-07,
       2.25137178e-06, 7.27500161e-06])[::-1, np.newaxis, np.newaxis]
# convert to mass mixing ratio (needed by CAM3 driver)
#  The conversion factor is m_o3 / m_air = 48.0 g/mol / 28.97 g/mol
O3mmr = O3vmr * 48.0 / 28.97
# Other values taken from the AquaPlanet Experiment protocols,
# except for O2 which is set the realistic value 0.21
CO2vmr = 348. / 1E6 * np.ones_like(p)
CH4vmr = 1650. / 1E9 * np.ones_like(p)
N2Ovmr = 306. / 1E9 * np.ones_like(p)
CFC11vmr = 0. * np.ones_like(p)
CFC12vmr = 0. * np.ones_like(p)

# Solar parameters
scon = 1365.2  # solar constant
coszen = 1/4   # cosine of zenith angle
eccf = 1.      # eccentricity factor, instantaneous irradiance = scon * eccf
# surface albedo
aldif = 0.3
aldir = 0.3
asdif = 0.3
asdir = 0.3

# cloud parameters
cldfrac = np.zeros_like(p)
clwp = np.zeros_like(p)
ciwp = np.zeros_like(p)
r_liq = np.zeros_like(p)
r_ice = np.zeros_like(p)

# Surface upwelling LW
flus = - 99.   # set to missing as default


def test_cam3_radiation():
    # Call the CAM3 radiation driver
    (TdotRad, SrfRadFlx, qrs, qrl, swflx, swflxc, lwflx, lwflxc, SwToaCf,
     SwSrfCf, LwToaCf, LwSrfCf, LwToa, LwSrf, SwToa, SwSrf,
     swuflx, swdflx, swuflxc, swdflxc,
     lwuflx, lwdflx, lwuflxc, lwdflxc) = \
        driver(KM, JM, IM, do_sw, do_lw, p, dp, ps, Tatm, Ts,
               q, O3mmr, cldfrac, clwp, ciwp, in_cld,
               aldif, aldir, asdif, asdir, eccf, coszen,
               scon, flus, r_liq, r_ice,
               CO2vmr, N2Ovmr, CH4vmr, CFC11vmr,
               CFC12vmr, g, Cpd, epsilon, stebol)
