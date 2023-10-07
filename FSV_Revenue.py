import pandas as pd
import numpy as np
from scipy.stats import skewnorm

# READ IN DATA
data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')
data.set_index('Desc', inplace = True)

# VARIABLE SETUP
hist_yr1 = data.columns[1]
fcst_yr1 = data.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 3))

# ADD FORECAST COLUMNS
data = data.reindex(columns = data.columns.tolist() + fcst_yrs)

# GENERATE REVENUE GROWTH DISTRIBUTION (Skewnorm distribution)
a, loc, scale = 1.3, -0.1, 2.2
sample = skewnorm(a, loc, scale).rvs(1000)

# ADD REVENUE GROWTH ROW
data.loc['Growth',:] = data.loc['Revenue',:].pct_change()

