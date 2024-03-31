# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import norm


# CASH FROM OPERATIONS - MISCELLANEOUS

def fcst_othcf(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

    metr_lbl = 'POR_' + line_name

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_cf.columns:

        if yr < fcst_yr1:
            fcst_cf.loc[line_name, yr] = data.loc[(line_name, 'CF'), yr]
            fcst_metr.loc[metr_lbl, yr] = fcst_cf.loc[line_name, yr] / fcst_is.loc[base_met, yr]
        else: pass

    # Generate distribution (Normal distribution)
    dst_loc = fcst_metr.loc[metr_lbl,:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc[metr_lbl,:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # Forecast metric
    for yr in fcst_yrs:
        fcst_metr.loc[metr_lbl, yr] = np.random.choice(dst, 1)
        fcst_cf.loc[line_name, yr] = fcst_is.loc[base_met, yr] * fcst_metr.loc[metr_lbl, yr]

    return (fcst_is, fcst_cf, fcst_metr)


# CASH FOR INVESTMENTS

def fcst_capex(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

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


def fcst_othinv(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

    # ADD ACTUALS TO CASH FLOW STATEMENT & % OF REVENUE TO METRICS
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_cf.loc['Net_Acq', yr] = data.loc[('Net_Acq','CF'), yr]
            fcst_cf.loc['Other_CFI', yr] = data.loc[('Other_CFI','CF'), yr]
            fcst_metr.loc['POR_Other_CFI', yr] = fcst_cf.loc['Other_CFI', yr] / fcst_is.loc['Revenue', yr]
        else: pass

    # GENERATE INCOME TAX RATE DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc['POR_Other_CFI',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['POR_Other_CFI',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST
    for yr in fcst_yrs:
        fcst_metr.loc['POR_Other_CFI', yr] = np.random.choice(dst, 1)
        fcst_cf.loc['Net_Acq', yr] = 0
        fcst_cf.loc['Other_CFI', yr] = fcst_is.loc['Revenue', yr] * fcst_metr.loc['POR_Other_CFI', yr]

    return (fcst_is, fcst_cf, fcst_metr)
