# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import norm

# ACCOUNTS RECEIVABLE / INVENTORY / ACCOUNTS PAYABLE

def fcst_turnratios(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1,
                    turn_metric, turn_base):

    turn_name = 'Turn_' + turn_metric

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_bs.columns:
        
        if yr < fcst_yr1:
            fcst_bs.loc[turn_metric, yr] = data.loc[(turn_metric,'BS'), yr]
            fcst_metr.loc[turn_name, yr] = fcst_is.loc[turn_base, yr] / fcst_bs.loc[turn_metric, yr]
        else: pass

    # Generate turnover distribution (Normal distribution)
    dst_loc = fcst_metr.loc[turn_name,:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc[turn_name,:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # Forecast turnover and turn metric
    for yr in fcst_yrs:
        fcst_metr.loc[turn_name, yr] = np.random.choice(dst, 1)
        fcst_bs.loc[turn_metric, yr] = fcst_is.loc[turn_base, yr] / fcst_metr.loc[turn_name, yr]

    return (fcst_is, fcst_bs, fcst_metr)

# PPE & INTANGIBLES (GROSS AND NET)

def fcst_ppeia(fcst_bs, fcst_cf, fcst_metr, data, fcst_yrs, fcst_yr1):

    for yr in fcst_bs.columns:

        # Add actuals to balance sheet dataframe        
        if yr < fcst_yr1:
            fcst_bs.loc['PPE_Gross', yr] = data.loc[('PPE_Gross','BS'), yr]
            fcst_bs.loc['PPE_Net', yr] = data.loc[('PPE_Net','BS'), yr]
            fcst_bs.loc['IA_Gross', yr] = data.loc[('Intangibles_Gross','BS'), yr]
            fcst_bs.loc['IA_Net', yr] = data.loc[('Intangibles_Net','BS'), yr]

        else: pass

        # Calculate retirements for actual years except year 1
        if yr != fcst_bs.columns[0]:
            fcst_metr.loc['FA_Rtmt', yr] = -(fcst_bs.loc['PPE_Gross', (yr - 1)] - fcst_bs.loc['PPE_Gross', yr] - fcst_cf.loc['Capex', yr])
            fcst_metr.loc['FA_Rtmt_Pct', yr] = fcst_metr.loc['FA_Rtmt', yr] / fcst_bs.loc['PPE_Gross', (yr - 1)]
            
            if fcst_bs.loc['IA_Gross', (yr - 1)] - fcst_bs.loc['IA_Gross', yr] < 0:
                fcst_metr.loc['IA_Rtmt', yr] = 0
            else:
                fcst_metr.loc['IA_Rtmt', yr] = -(fcst_bs.loc['IA_Gross', (yr - 1)] - fcst_bs.loc['IA_Gross', yr])
            
            fcst_metr.loc['IA_Rtmt_Pct', yr] = fcst_metr.loc['IA_Rtmt', yr] / fcst_bs.loc['IA_Gross', (yr - 1)]
        else: pass

    # Create distribution for retirements as a percentage of gross PPE
    dst_fa_loc = fcst_metr.loc['FA_Rtmt_Pct',:(fcst_yr1 - 1)].mean()
    dst_fa_scale = fcst_metr.loc['FA_Rtmt_Pct',:(fcst_yr1 - 1)].std()
    dst_fa = norm(loc = dst_fa_loc, scale = dst_fa_scale).rvs(1000)

    # Create distribution for retirements as a percentage of gross PPE
    dst_ia_loc = fcst_metr.loc['IA_Rtmt_Pct',:(fcst_yr1 - 1)].mean()
    dst_ia_scale = fcst_metr.loc['IA_Rtmt_Pct',:(fcst_yr1 - 1)].std()
    dst_ia = norm(loc = dst_ia_loc, scale = dst_ia_scale).rvs(1000)

    # Calculate forecast of retirements and PPE (gross and net)
    for yr in fcst_yrs:

        # Fixed assets
        fcst_metr.loc['FA_Rtmt_Pct', yr] = -abs(np.random.choice(dst_fa, 1))
        fcst_metr.loc['FA_Rtmt', yr] = fcst_bs.loc['PPE_Gross', (yr - 1)] * fcst_metr.loc['FA_Rtmt_Pct', yr]
        fcst_bs.loc['PPE_Gross', yr] = fcst_bs.loc['PPE_Gross', (yr - 1)] - fcst_cf.loc['Capex', yr] + fcst_metr.loc['FA_Rtmt', yr]
        fcst_bs.loc['PPE_Net', yr] = fcst_bs.loc['PPE_Net', (yr - 1)] - fcst_cf.loc['Capex', yr] + fcst_metr.loc['FA_Rtmt', yr]

        # Intangible assets
        fcst_metr.loc['IA_Rtmt_Pct', yr] = -abs(np.random.choice(dst_ia, 1))
        fcst_metr.loc['IA_Rtmt', yr] = fcst_bs.loc['IA_Gross', (yr - 1)] * fcst_metr.loc['IA_Rtmt_Pct', yr]
        
        if fcst_bs.loc['IA_Gross', (yr - 1)] + fcst_metr.loc['IA_Rtmt', yr] < 0:
            fcst_bs.loc['IA_Gross', yr] = 0
        else:
            fcst_bs.loc['IA_Gross', yr] = fcst_bs.loc['IA_Gross', (yr - 1)] + fcst_metr.loc['IA_Rtmt', yr]

        if fcst_bs.loc['IA_Net', (yr - 1)] + fcst_metr.loc['IA_Rtmt', yr] < 0:
            fcst_bs.loc['IA_Net', yr] = 0
        else:
            fcst_bs.loc['IA_Net', yr] = fcst_bs.loc['IA_Net', (yr - 1)] + fcst_metr.loc['IA_Rtmt', yr]

    return (fcst_bs, fcst_metr)

# OTHER SIMPLE FORECASTS

def fcst_goodwill(fcst_bs, data, fcst_yr1, flag):

    # GOODWILL & INTANGBILE ASSETS (No variability)
    for yr in fcst_bs.columns:
        if yr < fcst_yr1:
            fcst_bs.loc[flag, yr] = data.loc[(flag,'BS'), yr]
        elif yr >= fcst_yr1:
            fcst_bs.loc[flag, yr] = data.loc[(flag,'BS'), (fcst_yr1 - 1)]

    return fcst_bs


# OTHER BALANCE SHEET PERCENT OF REV FORECASTS (Other CA, Other NCA, Other CL, Other NCL)

def fcst_othbs(fcst_is, fcst_bs, fcst_metr, data, fcst_yrs, fcst_yr1, line_name, base_met):

    metr_lbl = 'POR_' + line_name

    # Add actuals to income statement / balance sheet dataframe
    for yr in fcst_bs.columns:

        if yr < fcst_yr1:
            fcst_bs.loc[line_name, yr] = data.loc[(line_name, 'BS'), yr]
            fcst_metr.loc[metr_lbl, yr] = fcst_bs.loc[line_name, yr] / fcst_is.loc[base_met, yr]
        else: pass

    # Generate distribution (Normal distribution)
    dst_loc = fcst_metr.loc[metr_lbl,:(fcst_yr1 - 1)].mean()
    dst_scale = fcst_metr.loc[metr_lbl,:(fcst_yr1 - 1)].std()
    dst = norm(loc = dst_loc, scale = dst_scale).rvs(1000)

    # Forecast metric
    for yr in fcst_yrs:
        fcst_metr.loc[metr_lbl, yr] = np.random.choice(dst, 1)
        fcst_bs.loc[line_name, yr] = fcst_is.loc[base_met, yr] * fcst_metr.loc[metr_lbl, yr]

    return (fcst_is, fcst_bs, fcst_metr)

