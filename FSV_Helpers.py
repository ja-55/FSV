# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

# REVENUE

def fcst_rev(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_a = 4, dst_loc = -0.05, dst_scale = 0.01):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        if yr < fcst_yr1: fcst_is.loc['Revenue', yr] = data.loc['Revenue', yr]
        else: pass

    # GENERATE REVENUE GROWTH DISTRIBUTION (Skewnorm distribution)
    dst = skewnorm(dst_a, dst_loc, dst_scale).rvs(1000)

    # ADD REVENUE GROWTH LINE
    fcst_metr.loc['Growth_Revenue',:] = data.loc['Revenue',:].pct_change()

    for yr in fcst_yrs:
        fcst_metr.loc['Growth_Revenue', yr] = np.random.choice(dst, 1)
        fcst_is.loc['Revenue', yr] = fcst_is.loc['Revenue', (yr - 1)] * (1 + fcst_metr.loc['Growth_Revenue', yr])

    return (fcst_is, fcst_metr)

# GROSS MARGIN

def fcst_mn_gross(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.326, dst_scale = 0.01):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1: fcst_is.loc['COS', yr] = data.loc['COS', yr]
        else: pass

    # GENERATE GROSS MARGIN DISTRIBUTION (Normal distribution)
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # ADD GROSS MARGIN LINE
    fcst_metr.loc['Margin_Gross',:] = 1 - (fcst_is.loc['COS',:] / fcst_is.loc['Revenue',:])

    for yr in fcst_yrs:
        fcst_metr.loc['Margin_Gross', yr] = np.random.choice(dst, 1)
        fcst_is.loc['COS', yr] = fcst_is.loc['Revenue', yr] * (1 - fcst_metr.loc['Margin_Gross', yr])

    return (fcst_is, fcst_metr)