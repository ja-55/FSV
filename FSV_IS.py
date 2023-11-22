# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm
import matplotlib.pyplot as plt


# NOTES

# python -m http.server



# READ IN DATA
data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')
main_is = pd.DataFrame(columns = data.columns)

data.set_index('Desc', inplace = True)
main_is.set_index('Desc', inplace = True)

# VARIABLE SETUP
hist_yr1 = main_is.columns[1]
fcst_yr1 = main_is.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 3))

# ADD FORECAST COLUMNS
main_is = main_is.reindex(columns = main_is.columns.tolist() + fcst_yrs)


# REVENUE


# GENERATE REVENUE GROWTH DISTRIBUTION (Skewnorm distribution)
a, loc, scale = 4, -0.05, 0.1
dist_gr_rev = skewnorm(a, loc, scale).rvs(1000)

# SET UP METRICS 
metr_is = pd.DataFrame(columns = main_is.columns.tolist())

# ADD ACTUALS TO INCOME STATEMENT DATAFRAME
for yr in main_is.columns:
    
    if yr < fcst_yr1:
        main_is.loc['Revenue', yr] = data.loc['Revenue', yr]
    else:
        pass

# ADD REVENUE GROWTH LINE
metr_is.loc['Growth_Revenue',:] = data.loc['Revenue',:].pct_change()

for yr in fcst_yrs:
    metr_is.loc['Growth_Revenue', yr] = np.random.choice(dist_gr_rev, 1)
    main_is.loc['Revenue', yr] = main_is.loc['Revenue', (yr - 1)] * (1 + metr_is.loc['Growth_Revenue', yr])


# GROSS MARGIN


# ADD ACTUALS TO INCOME STATEMENT DATAFRAME
for yr in main_is.columns:
    
    if yr < fcst_yr1:
        main_is.loc['COS', yr] = data.loc['COS', yr]
    else:
        pass

# GENERATE GROSS MARGIN DISTRIBUTION (Normal distribution)
dist_mn_gross = norm(loc = 0.326, scale = 0.01).rvs(1000)

# ADD GROSS MARGIN LINE
metr_is.loc['Margin_Gross',:] = 1 - (main_is.loc['COS',:] / main_is.loc['Revenue',:])

for yr in fcst_yrs:
    metr_is.loc['Margin_Gross', yr] = np.random.choice(dist_mn_gross, 1)
    main_is.loc['COS', yr] = main_is.loc['Revenue', yr] * (1 - metr_is.loc['Margin_Gross', yr])


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













print(main_is)
