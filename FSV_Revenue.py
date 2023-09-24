import pandas as pd
import numpy as np
from scipy.stats import chi2

# READ IN DATA
data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')
data.set_index('Desc', inplace = True)

# VARIABLE SETUP
hist_yr1 = data.columns[1]
fcst_yr1 = data.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 3))

# ADD FORECAST COLUMNS
data = data.reindex(columns = data.columns.tolist() + fcst_yrs)

# GENERATE REVENUE GROWTH DISTRIBUTION

#x = np.linspace(chi2.ppf(0.01, 51),
#                chi2.ppf(0.99, 51), 100)


# ADD REVENUE GROWTH ROW
data.loc['Growth',:] = data.loc['Revenue',:].pct_change()

#print(x)