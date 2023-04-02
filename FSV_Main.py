### IMPORTS

import numpy as np
import pandas as pd
import FSV_Helpers as fsvh


### INPUTS

path_file = ''
name_file = 'FSV_Python_Input.xlsx'
name_tab = 'Data'

path_full = path_file + name_file


### SET MODEL PARAMETERS

idx_common = ['STMT','METRIC']
fcst_yrone = 2023
fcst_yrfin = 2028
sims = 51
dist_size = 1000

### DERIVED PARAMETERS

fcst_horizon = list(range(fcst_yrone, (fcst_yrfin + 1)))

### READ IN DATA

data = pd.read_excel(path_full, sheet_name = name_tab)
data = data.set_index(idx_common)


### SET UP DEPENDENT DATA STRUCTURES - ACTUAL

actual_yrf = data.columns[0]
actual_yrl = data.columns[-1]

data_growth_cols = list(data.loc[('IS','REV'),:].pct_change().dropna().index.values)
data_growth = pd.DataFrame(columns = idx_common + data_growth_cols)
data_growth = data_growth.set_index(idx_common)

data_mgn_cols = list(data.loc[('IS','REV'),:].index.values)
data_mgn = pd.DataFrame(columns = idx_common + data_mgn_cols)
data_mgn = data_mgn.set_index(idx_common)

data_oth_cols = list(data.loc[('IS','REV'),:].index.values)
data_oth = pd.DataFrame(columns = idx_common + data_oth_cols)
data_oth = data_oth.set_index(idx_common)

### SET UP DEPENDENT DATA STRUCTURES - FORECAST

fcst = pd.DataFrame(columns = idx_common + fcst_horizon)
fcst = fcst.set_index(idx_common)

fcst_growth = pd.DataFrame(columns = idx_common + fcst_horizon)
fcst_growth = fcst_growth.set_index(idx_common)

fcst_mgn = pd.DataFrame(columns = idx_common + fcst_horizon)
fcst_mgn = fcst_mgn.set_index(idx_common)


# STEPS

"""
Revenue forecast
Gross margin forecast
SGA margin forecast
Tax rate forecast


Working capital forecast
Depreciation forecast
Capex forecast


"""

# 1) REVENUE

# Calc growth
data_growth = fsvh.calc_growth(data, data_growth, 'IS', 'REV', actual_yrf + 1, actual_yrl)

# Revenue growth distributions
dist_gr_rev_yr12 = np.random.normal(loc = 0.09, scale = 0.01, size = dist_size)
dist_gr_rev_yr34 = np.random.normal(loc = 0.05, scale = 0.01, size = dist_size)
dist_gr_rev_yr56 = np.random.normal(loc = 0.03, scale = 0.02, size = dist_size)

# Revenue growth forecast
fcst_growth.loc[('IS','REV'),2023] = np.random.choice(dist_gr_rev_yr12, 1, replace = False)[0]
fcst_growth.loc[('IS','REV'),2024] = np.random.choice(dist_gr_rev_yr12, 1, replace = False)[0]
fcst_growth.loc[('IS','REV'),2025] = np.random.choice(dist_gr_rev_yr34, 1, replace = False)[0]
fcst_growth.loc[('IS','REV'),2026] = np.random.choice(dist_gr_rev_yr34, 1, replace = False)[0]
fcst_growth.loc[('IS','REV'),2027] = np.random.choice(dist_gr_rev_yr56, 1, replace = False)[0]
fcst_growth.loc[('IS','REV'),2028] = np.random.choice(dist_gr_rev_yr56, 1, replace = False)[0]

# Revenue forecast
fcst.loc[('IS','REV'),2023] = data.loc[('IS','REV'),2022] * (1 + fcst_growth.loc[('IS','REV'),2023])
fcst.loc[('IS','REV'),2024] = fcst.loc[('IS','REV'),2023] * (1 + fcst_growth.loc[('IS','REV'),2024])
fcst.loc[('IS','REV'),2025] = fcst.loc[('IS','REV'),2024] * (1 + fcst_growth.loc[('IS','REV'),2025])
fcst.loc[('IS','REV'),2026] = fcst.loc[('IS','REV'),2025] * (1 + fcst_growth.loc[('IS','REV'),2026])
fcst.loc[('IS','REV'),2027] = fcst.loc[('IS','REV'),2026] * (1 + fcst_growth.loc[('IS','REV'),2027])
fcst.loc[('IS','REV'),2028] = fcst.loc[('IS','REV'),2027] * (1 + fcst_growth.loc[('IS','REV'),2028])


# 2) GROSS MARGIN

# Calc actual COS margins
data_mgn = fsvh.calc_mgn(data, data_mgn, 'IS', 'COS', actual_yrf, actual_yrl)

# COS margin distributions
dist_mgn_cos_yr12 = np.random.normal(loc = 0.608, scale = 0.02, size = dist_size)
dist_mgn_cos_yr34 = np.random.normal(loc = 0.610, scale = 0.03, size = dist_size)
dist_mgn_cos_yr56 = np.random.normal(loc = 0.614, scale = 0.04, size = dist_size)

# COS margin forecast
fcst_mgn.loc[('IS','COS'),2023] = np.random.choice(dist_mgn_cos_yr12, 1, replace = False)[0]
fcst_mgn.loc[('IS','COS'),2024] = np.random.choice(dist_mgn_cos_yr12, 1, replace = False)[0]
fcst_mgn.loc[('IS','COS'),2025] = np.random.choice(dist_mgn_cos_yr34, 1, replace = False)[0]
fcst_mgn.loc[('IS','COS'),2026] = np.random.choice(dist_mgn_cos_yr34, 1, replace = False)[0]
fcst_mgn.loc[('IS','COS'),2027] = np.random.choice(dist_mgn_cos_yr56, 1, replace = False)[0]
fcst_mgn.loc[('IS','COS'),2028] = np.random.choice(dist_mgn_cos_yr56, 1, replace = False)[0]
