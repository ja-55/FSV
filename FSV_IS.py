# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

import FSV_Helpers_IS as fsvh
import FSV_Helpers_BS as fsvh_bs
import FSV_Helpers_CF as fsvh_cf

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

# Gross Margin / Gross Profit
fs_is, metrics = fsvh.fcst_mn_gross(fs_is, metrics, data, fcst_yrs, fcst_yr1)

# OpEx (Non-Depreciation)
fs_is, metrics = fsvh.fcst_mn_sga(fs_is, metrics, data, fcst_yrs, fcst_yr1, pct_depr_sga)

# Capex
fs_is, fs_cf, metrics = fsvh_cf.fcst_capex(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1)

# PPE, Goodwill, Intangibles
fs_bs = fsvh_bs.fcst_goodwill(fs_bs, data, fcst_yr1, 'Goodwill')
fs_bs, metrics = fsvh_bs.fcst_ppeia(fs_bs, fs_cf, metrics, data, fcst_yrs, fcst_yr1)

# # Depreciation
# fs_is, fs_bs, metrics = fsvh.fcst_depr(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, pct_depr_sga)

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
fs_is.to_excel("FSV_OP_IS.xlsx")
fs_bs.to_excel("FSV_OP_BS.xlsx")
fs_cf.to_excel("FSV_OP_CF.xlsx")
metrics.to_excel("FSV_OP_Metr.xlsx")