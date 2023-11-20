# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
import matplotlib.pyplot as plt

# READ IN DATA
data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')

main_is = data.copy()
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

# ADD REVENUE GROWTH LINE
metr_is.loc['Growth_Revenue',:] = main_is.loc['Revenue',:].pct_change()

for yr in fcst_yrs:
    metr_is.loc['Growth_Revenue', yr] = np.random.choice(dist_gr_rev, 1)
    main_is.loc['Revenue', yr] = main_is.loc['Revenue', (yr - 1)] * (1 + metr_is.loc['Growth_Revenue', yr])


# GROSS MARGIN


# GENERATE GROSS MARGIN DISTRIBUTION (Skewnorm distribution)
a, loc, scale = 4, 0.30, 0.35
dist_mn_gross = skewnorm(a, loc, scale).rvs(1000)

# ADD GROSS MARGIN LINE
metr_is.loc['Margin_Gross',:] = 1 - (main_is.loc['COS',:] / main_is.loc['Revenue',:])

for yr in fcst_yrs:
    metr_is.loc['Margin_Gross', yr] = np.random.choice(dist_mn_gross, 1)
    main_is.loc['COS', yr] = main_is.loc['Revenue', yr] * (1 - metr_is.loc['Margin_Gross', yr])

print(metr_is)