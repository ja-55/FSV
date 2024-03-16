# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import norm

# CAPEX

def fcst_capex(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1):

    # ADD ACTUALS TO CASH FLOW STATEMENT & % OF REVENUE TO METRICS
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_cf.loc['Capex', yr] = data.loc[('Capex','CF'), yr]
            fcst_metr.loc['POR_Capex', yr] = fcst_cf.loc['Capex', yr] / fcst_is.loc['Revenue', yr]
        else: pass

    # GENERATE INCOME TAX RATE DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc['POR_Capex',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['POR_Capex',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST
    for yr in fcst_yrs:
        fcst_metr.loc['POR_Capex', yr] = np.random.choice(dst, 1)
        fcst_cf.loc['Capex', yr] = fcst_is.loc['Revenue', yr] * fcst_metr.loc['POR_Capex', yr]

    return (fcst_is, fcst_cf, fcst_metr)