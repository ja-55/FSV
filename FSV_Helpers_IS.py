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

    # ADD GROSS MARGIN / GROSS PROFIT LINE
    fcst_metr.loc['Margin_Gross',:] = 1 - (fcst_is.loc['COS',:] / fcst_is.loc['Revenue',:])
    fcst_is.loc['SubT_GrossProfit',:] = fcst_is.loc['Revenue',:] - fcst_is.loc['COS',:]

    for yr in fcst_yrs:
        fcst_metr.loc['Margin_Gross', yr] = np.random.choice(dst, 1)
        fcst_is.loc['COS', yr] = fcst_is.loc['Revenue', yr] * (1 - fcst_metr.loc['Margin_Gross', yr])
        fcst_is.loc['SubT_GrossProfit', :] = fcst_is.loc['Revenue',:] - fcst_is.loc['COS',:]

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

def fcst_depr(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.12, dst_scale = 0.005):

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['Depr', yr] = data.loc['Depr', yr]
            fcst_bs.loc['PPE_Gross', yr] = data.loc['PPE_Gross', yr]
            fcst_bs.loc['IA_Gross', yr] = data.loc['IA_Gross', yr]

            # Add historical average asset life to metrics
            fcst_metr.loc['AssetLife',yr] = (fcst_bs.loc['PPE_Gross', yr] + fcst_bs.loc['IA_Gross', yr]) / fcst_is.loc['Depr', yr]

        else: pass

    # Create distribution for average asset life
    dst_loc = fcst_metr.loc['AssetLife',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['AssetLife',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # Add forecast of average asset life to metrics & calculate depreciation (INCLUDES PH FOR PPE / IA)
    for yr in fcst_yrs:
        fcst_metr.loc['AssetLife',yr] = np.random.choice(dst, 1)
        fcst_bs.loc['PPE_Gross',yr] = fcst_bs.loc['PPE_Gross',yr] * 1.03
        fcst_bs.loc['IA_Gross',yr] = fcst_bs.loc['IA_Gross',yr] * 1.03
        print(fcst_bs)
        print(fcst_metr)
        fcst_is.loc['Depr', yr] = (fcst_bs.loc['PPE_Gross', (yr - 1)] + fcst_bs.loc['IA_Gross', (yr - 1)]) / fcst_metr.loc['AssetLife', yr]

    # Calculate operating margin / operating profit
    fcst_is.loc['SubT_OperatingProfit', :] = fcst_is.loc['SubT_GrossProfit', :] - fcst_is.loc['Opex_NonDepr', :] - fcst_is.loc['Depr', :]
    fcst_metr.loc['Margin_Operating', :] = fcst_is.loc['SubT_OperatingProfit', :] / fcst_is.loc['Revenue', :]

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




