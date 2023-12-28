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

# SG&A MARGIN (Ex. Depreciation)

def fcst_mn_sga(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.12, dst_scale = 0.005):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1: fcst_is.loc['Opex_NonDepr', yr] = data.loc['Opex_NonDepr', yr]
        else: pass

    # GENERATE SG&A DISTRIBUTION (Normal distribution)
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # ADD SG&A MARGIN LINE
    fcst_metr.loc['Margin_SGA',:] = 1 - (fcst_is.loc['Opex_NonDepr',:] / fcst_is.loc['Revenue',:])

    for yr in fcst_yrs:
        fcst_metr.loc['Margin_SGA', yr] = np.random.choice(dst, 1)
        fcst_is.loc['Opex_NonDepr', yr] = fcst_is.loc['Revenue', yr] * (1 - fcst_metr.loc['Margin_SGA', yr])

    return (fcst_is, fcst_metr)

# DEPRECIATION

def fcst_depr(fcst_is, , fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.12, dst_scale = 0.005):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['Depr', yr] = data.loc['Depr', yr]
            fcst_bs.loc['PPE_Gross', yr] = data.loc['PPE_Gross', yr]
            fcst_bs.loc['Accum_Depr', yr] = data.loc['Accum_Depr', yr]
            fcst_bs.loc['PPE_Net', yr] = fcst_bs.loc['PPE_Gross', yr] - fcst_bs.loc['Accum_Depr', yr]
        else: pass


    # ADD HISTORICAL AVERAGE ASSET LIFE TO METRICS
    if yr < fcst_yr1:
        fcst_metr.loc['AssetLife',:] = fcst_bs.loc['PPE_Gross', yr] / fcst_is.loc['Depr', yr]
    
    # CREATE DISTRIBUTION FOR ASSET LIFE
    dst_loc = fcst_metr.loc['AssetLife',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['AssetLife',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # ADD FORECAST AVERAGE ASSET LIFE TO METRICS
    if yr >= fcst_yr1:
        fcst_metr.loc['AssetLife',yr] = np.random.choice(dst, 1)

    # NEED GROSS PPE FORECAST TO FINISH

    return (fcst_is, fcst_bs, fcst_metr)


# COST OF DEBT / INTEREST EXPENSE (Pending debt forecasting)

def fcst_costdebt(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.03, dst_scale = 0.0025):

    # ADD ACTUALS TO INCOME STATEMENT / BALANCE SHEET DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['IntExp', yr] = data.loc['IntExp', yr]
            fcst_bs.loc['LTD_Current', yr] = data.loc['LTD_Current', yr]
            fcst_bs.loc['LTD_NonCurrent', yr] = data.loc['LTD_NonCurrent', yr]
        else: pass

    # GENERATE GROSS MARGIN DISTRIBUTION (Normal distribution)
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # ADD COST OF DEBT TO METRICS
    fcst_metr.loc['CostDebt',:] = fcst_is.loc['IntExp',:] / (fcst_bs.loc['LTD_Current',:] + fcst_bs.loc['LTD_NonCurrent',:])

    for yr in fcst_yrs:
        fcst_metr.loc['CostDebt', yr] = np.random.choice(dst, 1)
        fcst_is.loc['IntExp', yr] = (fcst_bs.loc['LTD_Current', yr] + fcst_bs.loc['LTD_NonCurrent', yr]) * fcst_metr.loc['CostDebt', yr]

    return (fcst_is, fcst_bs, fcst_metr)

# ACCOUNTS RECEIVABLE / INVENTORY / ACCOUNTS PAYABLE

def fcst_turnratios(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1,
                    turn_metric, turn_base):

    turn_name = 'Turn_' + turn_metric

    # ADD ACTUALS TO INCOME STATEMENT / BALANCE SHEET DATAFRAME
    for yr in fcst_bs.columns:
        
        if yr < fcst_yr1:
            fcst_bs.loc[turn_metric, yr] = data.loc[turn_metric, yr]
            fcst_metr.loc[(turn_name),yr] = fcst_is.loc[turn_base, yr] / fcst_bs.loc[turn_metric, yr]
        else: pass

    # GENERATE TURNOVER DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc[turn_name,:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc[turn_name,:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST TURNOVER AND TURN METRIC
    for yr in fcst_yrs:
        fcst_metr.loc[turn_name, yr] = np.random.choice(dst, 1)
        fcst_bs.loc[turn_metric, yr] = fcst_is.loc[turn_base, yr] / fcst_metr.loc[turn_name, yr]

    return (fcst_is, fcst_bs, fcst_metr)

# OTHER BALANCE SHEET PERCENT OF REV FORECASTS (Other CA, Other NCA, Other CL, Other NCL)

def fcst_pctofrev(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1, stmt_name):

    metr_name = 'POR_' + stmt_name

    # ADD ACTUALS TO INCOME STATEMENT / BALANCE SHEET DATAFRAME
    for yr in fcst_bs.columns:

        if yr < fcst_yr1:
            fcst_bs.loc[stmt_name, yr] = data.loc[stmt_name, yr]
            fcst_metr.loc[(metr_name),yr] = fcst_bs.loc[metr_name, yr] / fcst_is.loc['Revenue', yr]
        else: pass

    # GENERATE TURNOVER DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc[metr_name,:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc[metr_name,:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST TURNOVER AND TURN METRIC
    for yr in fcst_yrs:
        fcst_metr.loc[metr_name, yr] = np.random.choice(dst, 1)
        fcst_bs.loc[stmt_name, yr] = fcst_is.loc['Revenue', yr] * fcst_metr.loc[metr_name, yr]

    return (fcst_is, fcst_bs, fcst_metr)



# OTHER SIMPLE FORECASTS

def fcst_oth(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1):

    # GOODWILL & INTANGBILE ASSETS (No variability)
    for yr in fcst_bs.columns:
        if yr < fcst_yr1:
            fcst_bs.loc['Goodwill', yr] = data.loc['Goodwill', yr]
            fcst_bs.loc['Intangibles', yr] = data.loc['Intangibles', yr]
        elif yr >= fcst_yr1:
            fcst_bs.loc['Goodwill', yr] = data.loc['Goodwill', (fcst_yr1 - 1)]
            fcst_bs.loc['Intangibles', yr] = data.loc['Intangibles', (fcst_yr1 - 1)]

    return (fcst_is, fcst_bs, fcst_metr)