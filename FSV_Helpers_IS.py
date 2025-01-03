# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

# REVENUE

def fcst_rev(fs_is, metrics, data, fcst_yrs, fcst_yr1,
             dst_a = 4, dst_loc = 0.05, dst_scale = 0.01):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fs_is.columns:
        if yr < fcst_yr1: fs_is.loc['Revenue', yr] = data.loc[('Revenue','IS'), yr]
        else: pass

    # GENERATE REVENUE GROWTH DISTRIBUTION (Skewnorm distribution)
    dst = skewnorm(dst_a, dst_loc, dst_scale).rvs(1000)

    # ADD REVENUE GROWTH TO METRICS - HISTORY
    metrics.loc['Growth_Revenue',:] = data.loc[('Revenue','IS'),:].pct_change()

    # ADD REVENUE GROWTH / REVENUE $ FORECAST
    for yr in fcst_yrs:
        metrics.loc['Growth_Revenue', yr] = np.random.choice(dst, 1)
        fs_is.loc['Revenue', yr] = fs_is.loc['Revenue', (yr - 1)] * (1 + metrics.loc['Growth_Revenue', yr])

    return (fs_is, metrics)

# GROSS MARGIN

def fcst_mn_gross(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1,
             dst_loc = 0.3584, dst_scale = 0.01):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1: fcst_is.loc['COS', yr] = data.loc[('COS','IS'), yr]
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

def fcst_mn_sga(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1, pct_sga_depr,
             dst_loc = 0.03, dst_scale = 0.005):

    # ADD ACTUALS TO INCOME STATEMENT DATAFRAME
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1: fcst_is.loc['Opex_NonDepr', yr] = data.loc[('SGA','IS'), yr] - data.loc[('Depr','IS'), yr] * pct_sga_depr
        else: pass

    # GENERATE SG&A DISTRIBUTION (Normal distribution)
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # ADD SG&A MARGIN LINE
    fcst_metr.loc['Margin_SGA',:] = fcst_is.loc['Opex_NonDepr',:] / fcst_is.loc['Revenue',:]

    for yr in fcst_yrs:
        fcst_metr.loc['Margin_SGA', yr] = np.random.choice(dst, 1)
        fcst_is.loc['Opex_NonDepr', yr] = fcst_is.loc['Revenue', yr] * fcst_metr.loc['Margin_SGA', yr]

    return (fcst_is, fcst_metr)

# DEPRECIATION

def fcst_depr(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1, pct_sga_depr):

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['Depr', yr] = data.loc[('Depr','IS'), yr]

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
        fcst_is.loc['Depr', yr] = (fcst_bs.loc['PPE_Gross', yr] + fcst_bs.loc['IA_Gross', yr]) / fcst_metr.loc['AssetLife', yr]

    # Calculate operating margin / operating profit
    fcst_is.loc['SubT_OperatingProfit', :] = fcst_is.loc['SubT_GrossProfit', :] - fcst_is.loc['Opex_NonDepr', :] - fcst_is.loc['Depr', :] * pct_sga_depr
    fcst_metr.loc['Margin_Operating', :] = fcst_is.loc['SubT_OperatingProfit', :] / fcst_is.loc['Revenue', :]

    return (fcst_is, fcst_bs, fcst_metr)


# COST OF DEBT / INTEREST EXPENSE

def fcst_costdebt(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1):

    # ADD ACTUALS TO INCOME STATEMENT / BALANCE SHEET DATAFRAME & COST OF DEBT TO METRICS
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['IntExp', yr] = data.loc[('IntExp','IS'), yr]
            fcst_is.loc['OthInc', yr] = data.loc[('OthInc','IS'), yr]
            fcst_bs.loc['LTD_Current', yr] = data.loc[('LTD_Current','BS'), yr]
            fcst_bs.loc['LTD_NonCurrent', yr] = data.loc[('LTD_NonCurrent','BS'), yr]
            fcst_metr.loc['Cost_Debt',yr] = fcst_is.loc['IntExp', yr] / (fcst_bs.loc['LTD_Current', yr] + fcst_bs.loc['LTD_NonCurrent', yr])
        else: pass

    # GENERATE COST OF DEBT DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc['Cost_Debt',:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc['Cost_Debt',:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST / DEBT IS PH
    for yr in fcst_yrs:
        fcst_metr.loc['Cost_Debt', yr] = np.random.choice(dst, 1)
        fcst_bs.loc['LTD_Current', yr] = fcst_bs.loc['LTD_Current', (yr - 1)] * 1.03
        fcst_bs.loc['LTD_NonCurrent', yr] = fcst_bs.loc['LTD_NonCurrent', (yr - 1)] * 1.03
        fcst_is.loc['IntExp', yr] = (fcst_bs.loc['LTD_Current', yr] + fcst_bs.loc['LTD_NonCurrent', yr]) * fcst_metr.loc['Cost_Debt', yr]
        fcst_is.loc['OthInc', yr] = 0

    fcst_is.loc['SubT_PretaxProfit', :] = fcst_is.loc['SubT_OperatingProfit', :] - fcst_is.loc['IntExp', :] - fcst_is.loc['OthInc', :]
    fcst_metr.loc['Margin_Pretax', :] = fcst_is.loc['SubT_PretaxProfit', :] / fcst_is.loc['Revenue', :]

    return (fcst_is, fcst_bs, fcst_metr)

# INCOME TAX RATE / INCOME TAX EXPENSE

def fcst_tax(fcst_is, fcst_metr, data, fcst_yrs, fcst_yr1, taxrate_stat, flag_taxrate):

    # ADD ACTUALS TO INCOME STATEMENT & TAX RATE TO METRICS
    for yr in fcst_is.columns:
        
        if yr < fcst_yr1:
            fcst_is.loc['TaxExp', yr] = data.loc[('TaxExp','IS'), yr]
            fcst_metr.loc['TaxRate', yr] = fcst_is.loc['TaxExp', yr] / fcst_is.loc['SubT_PretaxProfit', yr]
        else: pass

    # GENERATE INCOME TAX RATE DISTRIBUTION (Normal distribution)
    dst_loc = fcst_metr.loc['TaxRate',:(fcst_yr1 - 1)].mean()
    dst_scale = 0
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # FORECAST
    for yr in fcst_yrs:
        if flag_taxrate == 'Statutory':
            fcst_metr.loc['TaxRate', yr] = taxrate_stat
        else:
            fcst_metr.loc['TaxRate', yr] = np.random.choice(dst, 1)
        fcst_is.loc['TaxExp', yr] = fcst_is.loc['SubT_PretaxProfit', yr] * fcst_metr.loc['TaxRate', yr]

    fcst_is.loc['SubT_NetIncome', :] = fcst_is.loc['SubT_PretaxProfit', :] - fcst_is.loc['TaxExp', :]
    fcst_metr.loc['Margin_NetIncome', :] = fcst_is.loc['SubT_NetIncome', :] / fcst_is.loc['Revenue', :]

    return (fcst_is, fcst_metr)