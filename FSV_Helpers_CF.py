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


def fcst_othinv(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1):

    # ADD ACTUALS TO CASH FLOW STATEMENT & % OF REVENUE TO METRICS
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_cf.loc['Net_Acq', yr] = data.loc[('Net_Acq','CF'), yr]
            fcst_cf.loc['Other_CFI', yr] = data.loc[('Other_CFI','CF'), yr]
        else: pass

    # FORECAST
    for yr in fcst_yrs:
        fcst_cf.loc['Net_Acq', yr] = 0
        fcst_cf.loc['Other_CFI', yr] = 0

    return (fcst_is, fcst_cf, fcst_metr)

def fcst_othcfo(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

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


def fcst_cff_stock(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

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

def fcst_cff_div(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1, shr_price):

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_cf.columns:

        if yr < fcst_yr1:
            fcst_cf.loc['Dividends', yr] = data.loc[('Dividends', 'CF'), yr]
            fcst_is.loc['Shares', yr] = data.loc[('Shares', 'IS'), yr]
            fcst_metr.loc['DPS', yr] = fcst_cf.loc['Dividends', yr] / fcst_is.loc['Shares', yr]

            try: fcst_metr.loc['DPS_Gr', yr] = (fcst_metr.loc['DPS', yr] / fcst_metr.loc['DPS', (yr - 1)]) - 1
            except: pass

        else: pass

    # Generate distribution (Normal distribution)
    dst_loc = fcst_metr.loc['DPS_Gr',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['DPS_Gr',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # Forecast metric
    for yr in fcst_yrs:

        # Calculate share count rollforward
        fcst_is.loc['Shares', yr] = ((fcst_cf.loc['CS_Issue', yr] + fcst_cf.loc['CS_Repo', yr]) / shr_price) + fcst_is.loc['Shares', (yr - 1)]

        # Forecast dividend growth
        fcst_metr.loc['DPS_Gr', yr] = np.random.choice(dst, 1)
        fcst_metr.loc['DPS', yr] = fcst_metr.loc['DPS', (yr - 1)] * (1 + fcst_metr.loc['DPS_Gr', yr])
        fcst_cf.loc['Dividends', yr] = fcst_is.loc['Shares', yr] * fcst_metr.loc['DPS', yr]

    return (fcst_is, fcst_cf, fcst_metr)

def fcst_cff_ltd(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1):

    # Add actuals to income statement / cash flow dataframe
    for yr in fcst_cf.columns:

        if yr < fcst_yr1:
            fcst_cf.loc['LT_Borrow', yr] = data.loc[('LT_Borrow', 'CF'), yr]
        else: pass

    for yr in fcst_yrs:
        fcst_cf.loc['LT_Borrow', yr] = 0

    return (fcst_is, fcst_cf, fcst_metr)


def fcst_othcff(fcst_is, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1):

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_cf.columns:

        if yr < fcst_yr1:
            fcst_cf.loc['Other_CFF', yr] = data.loc[('Other_CFF', 'CF'), yr]
        else: pass

    # Forecast metric
    for yr in fcst_yrs:
        fcst_cf.loc['Other_CFF', yr] = 0

    return (fcst_is, fcst_cf, fcst_metr)


def fcst_cf_subt(fcst_is, fcst_cf, yr1_begcash):

    print(fcst_is['SubT_NetIncome'])

    fcst_cf['SubT_CFO'] = fcst_is['SubT_NetIncome'] + fcst_is['Depr'] + fcst_cf['Stock_Comp'] + fcst_cf['Other_CFO']
    fcst_cf['SubT_CFI'] = fcst_cf['Capex'] + fcst_cf['Net_Acq'] + fcst_cf['Other_CFI']
    fcst_cf['SubT_CFF'] = fcst_cf['ST_Borrow'] + fcst_cf['LT_Borrow'] + fcst_cf['CS_Issue'] + fcst_cf['CS_Repo'] + fcst_cf['Dividends']

    for yr in fcst_cf.columns:
        if yr == fcst_cf.columns[0]:
            fcst_cf.loc['Cash_Beg', yr] = yr1_begcash
            fcst_cf.loc['Cash_End', yr] = fcst_cf.loc['Cash_Beg', yr] + fcst_cf.loc['SubT_CFO', yr] + fcst_cf.loc['SubT_CFI', yr] + fcst_cf.loc['SubT_CFF', yr]
        else:
            fcst_cf.loc['Cash_Beg'] = fcst_cf.loc['Cash_End', (yr - 1)]
            fcst_cf.loc['Cash_End', yr] = fcst_cf.loc['Cash_Beg', yr] + fcst_cf.loc['SubT_CFO', yr] + fcst_cf.loc['SubT_CFI', yr] + fcst_cf.loc['SubT_CFF', yr]

    return (fcst_is, fcst_cf)