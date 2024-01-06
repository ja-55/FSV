# IMPORTS
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm

import FSV_Helpers_IS as fsvh

# NOTES
# python -m http.server


# READ IN DATA
data = pd.read_excel("FSV_Input.xlsx", sheet_name="Grid")
main_is = pd.DataFrame(columns=data.columns)
main_bs = pd.DataFrame(columns=data.columns)

data.set_index("Desc", inplace=True)
main_is.set_index("Desc", inplace=True)
main_bs.set_index("Desc", inplace=True)

# VARIABLE SETUP
hist_yr1 = main_is.columns[1]
fcst_yr1 = main_is.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 4))

# ADD FORECAST COLUMNS
main_is = main_is.reindex(columns=main_is.columns.tolist() + fcst_yrs)
main_bs = main_bs.reindex(columns=main_is.columns.tolist() + fcst_yrs)

# SET UP METRICS
metr_is = pd.DataFrame(columns=main_is.columns.tolist())

# FORECAST

# Revenue
main_is, metr_is = fsvh.fcst_rev(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# Gross Margin / Gross Profit
main_is, metr_is = fsvh.fcst_mn_gross(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# OpEx (Non-Depreciation)
main_is, metr_is = fsvh.fcst_mn_sga(main_is, metr_is, data, fcst_yrs, fcst_yr1)

# Depreciation
main_is, main_bs, metr_is = fsvh.fcst_depr(main_is, main_bs, metr_is, data, fcst_yrs, fcst_yr1)


# OUTPUT
main_is.to_json("FSV_OP_IS.json")
metr_is.to_json("FSV_OP_Metr.json")
