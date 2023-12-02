# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

import FSV_Helpers as fsvh

# NOTES
# python -m http.server


# READ IN DATA
data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')
main_is = pd.DataFrame(columns = data.columns)
main_bs = pd.DataFrame(columns = data.columns)

data.set_index('Desc', inplace = True)
main_is.set_index('Desc', inplace = True)
main_bs.set_index('Desc', inplace = True)

# VARIABLE SETUP
hist_yr1 = main_is.columns[1]
fcst_yr1 = main_is.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 3))

# ADD FORECAST COLUMNS
main_is = main_is.reindex(columns = main_is.columns.tolist() + fcst_yrs)
main_bs = main_bs.reindex(columns = main_is.columns.tolist() + fcst_yrs)

# SET UP METRICS 
metr_is = pd.DataFrame(columns = main_is.columns.tolist())

# REVENUE
main_is, metr_is = fsvh.fcst_rev(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# GROSS MARGIN
main_is, metr_is = fsvh.fcst_mn_gross(main_is, metr_is, data, fcst_yrs, fcst_yr1)


# OPERATING EXPENSES (NON-DEPRECIATION)


# ADD ACTUALS TO INCOME STATEMENT DATAFRAME
for yr in main_is.columns:
    
    if yr < fcst_yr1:
        main_is.loc['Opex_NonDepr', yr] = data.loc['Opex_NonDepr', yr]
    else:
        pass

# GENERATE DISTRIBUTION (Normal distribution)
dist_mn_opex_nondepr = norm(loc = 0.125, scale = 0.01).rvs(1000)

# ADD OPEX NON-DEPR MARGIN LINE
metr_is.loc['Margin_Opex_NonDepr',:] = main_is.loc['Opex_NonDepr',:] / main_is.loc['Revenue',:]

for yr in fcst_yrs:
    metr_is.loc['Margin_Opex_NonDepr', yr] = np.random.choice(dist_mn_opex_nondepr, 1)
    main_is.loc['Opex_NonDepr', yr] = main_is.loc['Revenue', yr] * metr_is.loc['Margin_Opex_NonDepr', yr]


# DEPRECIATION EXPENSES


# ADD ACTUALS TO INCOME STATEMENT DATAFRAME
for yr in main_is.columns:
    
    if yr < fcst_yr1:
        main_is.loc['Depr', yr] = data.loc['Depr', yr]
    else:
        pass

# GENERATE DISTRIBUTION (Normal distribution)
dist_mn_opex_depr = norm(loc = 0.033, scale = 0.005).rvs(1000)

# ADD OPEX NON-DEPR MARGIN LINE
metr_is.loc['Margin_Opex_Depr',:] = main_is.loc['Depr',:] / main_is.loc['Revenue',:]

for yr in fcst_yrs:
    metr_is.loc['Margin_Opex_Depr', yr] = np.random.choice(dist_mn_opex_depr, 1)
    main_is.loc['Depr', yr] = main_is.loc['Revenue', yr] * metr_is.loc['Margin_Opex_Depr', yr]




# OUTPUT
main_is.to_json('FSV_OP_IS.json')
metr_is.to_json('FSV_OP_Metr.json')