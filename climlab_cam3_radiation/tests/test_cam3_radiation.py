import numpy as np
import pytest
import climlab_cam3_radiation
from climlab_cam3_radiation import driver, absems



def test_cam3_radiation():
    pass
    # # Call the CAM3 radiation driver
    # (TdotRad, SrfRadFlx, qrs, qrl, swflx, swflxc, lwflx, lwflxc, SwToaCf,
    #  SwSrfCf, LwToaCf, LwSrfCf, LwToa, LwSrf, SwToa, SwSrf,
    #  swuflx, swdflx, swuflxc, swdflxc,
    #  lwuflx, lwdflx, lwuflxc, lwdflxc) = \
    #     driver(KM, JM, IM, do_sw, do_lw, p, dp, ps, Tatm, Ts,
    #            q, O3mmr, cldfrac, clwp, ciwp, in_cld,
    #            aldif, aldir, asdif, asdir, eccf, coszen,
    #            scon, flus, r_liq, r_ice,
    #            CO2vmr, N2Ovmr, CH4vmr, CFC11vmr,
    #            CFC12vmr, g, Cpd, epsilon, stebol)
