# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

import FSV_Helpers_IS as fsvh
import FSV_Helpers_BS as fsvh_bs

# NOTES
# python -m http.server


# READ IN DATA
data = pd.read_excel("FSV_Input.xlsx", sheet_name="Grid")
fs_is = pd.DataFrame(columns = data.columns).drop('Stmt', axis = 1)
fs_bs = pd.DataFrame(columns = data.columns).drop('Stmt', axis = 1)
fs_cf = pd.DataFrame(columns = data.columns).drop('Stmt', axis = 1)

data.set_index(['Desc','Stmt'], inplace=True)
fs_is.set_index('Desc', inplace=True)
fs_bs.set_index('Desc', inplace=True)
fs_cf.set_index('Desc', inplace=True)

# ASSUMPTIONS
pct_depr_sga = 0.75
num_fcst_yrs = 4

# VARIABLE SETUP
hist_yr1 = fs_is.columns[1]
fcst_yr1 = fs_is.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + num_fcst_yrs))

# ADD FORECAST COLUMNS
fs_is = fs_is.reindex(columns = fs_is.columns.tolist() + fcst_yrs)
fs_bs = fs_bs.reindex(columns = fs_is.columns.tolist())
fs_cf = fs_cf.reindex(columns = fs_is.columns.tolist())

# SET UP METRICS
metrics = pd.DataFrame(columns = fs_is.columns.tolist())

# FORECAST - INCOME STATEMENT

# Revenue
fs_is, metrics = fsvh.fcst_rev(fs_is, metrics, data, fcst_yrs, fcst_yr1)

# # Gross Margin / Gross Profit
# main_is, metr_is = fsvh.fcst_mn_gross(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# # OpEx (Non-Depreciation)
# main_is, metr_is = fsvh.fcst_mn_sga(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# # Depreciation
# main_is, main_bs, metr_is = fsvh.fcst_depr(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1, pct_depr_sga)

# # Interest Expense
# main_is, main_bs, metr_is = fsvh.fcst_costdebt(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1)

# # Tax Expense
# main_is, metr_is = fsvh.fcst_tax(main_is, metr_is, data, fcst_yrs, fcst_yr1)


# # FORECAST - BALANCE SHEET

# # Accounts Receivable
# main_is, main_bs, metr_is = fsvh_bs.fcst_turnratios(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1, 'AR', 'Revenue')

# # Inventory
# main_is, main_bs, metr_is = fsvh_bs.fcst_turnratios(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1, 'Inv', 'COS')

# # Accounts Payable
# main_is, main_bs, metr_is = fsvh_bs.fcst_turnratios(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1, 'AP', 'COS')

# # Goodwill
# main_bs = fsvh_bs.fcst_goodwill(main_bs, data, fcst_yr1)












# # OUTPUT
# # main_is.to_excel("FSV_OP_IS.xlsx")
# # metr_is.to_excel("FSV_OP_Metr.xlsx")
# # main_bs.to_excel("FSV_OP_BS.xlsx")
