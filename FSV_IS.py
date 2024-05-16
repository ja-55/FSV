# IMPORTS
import pandas as pd
import numpy as np
# from scipy.stats import skewnorm
from scipy.stats import norm

import FSV_Helpers_IS as fsvh
import FSV_Helpers_BS as fsvh_bs
import FSV_Helpers_CF as fsvh_cf
import FSV_Valuation as fsvh_val


# READ IN DATA
data = pd.read_excel("FSV_Input.xlsx", sheet_name="Grid")
data.set_index(['Desc','Stmt'], inplace=True)
val_op = pd.DataFrame(columns = ['Growth Rate','RONIC','Value per Share'])

# ASSUMPTIONS

# Forecast parameters
num_fcst_yrs = 4
num_sims = 11
df_cols = data.columns.tolist() + ['Desc']

# Fundamental stats
pct_depr_sga = 0.75
shr_price = 200
yr1_begcash = 5455
taxrate_stat = 0.21

# Cost of equity
rfr = 0.054
beta = 1.27
rtn_mkt = 0.07

# Flags
flag_taxrate = 'Statutory'

# Valuation rates
gr_loc = 0.02
gr_scale = 0.005
dst_gr = norm(loc = gr_loc, scale = gr_scale).rvs(1000)
ronic_loc = 0.15
ronic_scale = 0.02
dst_ronic = norm(loc = ronic_loc, scale = ronic_scale).rvs(1000)

# Other
metric_list = ['Growth_Revenue', 'Margin_Gross', 'Margin_SGA', 'POR_Capex', 'Margin_Operating', 'Cost_Debt', 'Margin_Pretax',
               'TaxRate', 'Margin_NetIncome', 'DPS', 'DPS_Gr', 'Debt_to_Assets', 'Cost_Equity', 'Cost_Capital']

for sim in range(num_sims):

    # DATAFRAME SETUP
    fs_is = pd.DataFrame(columns = df_cols)
    fs_bs = pd.DataFrame(columns = df_cols)
    fs_cf = pd.DataFrame(columns = df_cols)

    fs_is.set_index('Desc', inplace=True)
    fs_bs.set_index('Desc', inplace=True)
    fs_cf.set_index('Desc', inplace=True)

    # SET UP PARAMETERS FOR DATAFRAME COLUMNS
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

    # Depreciation
    fs_is, fs_bs, metrics = fsvh.fcst_depr(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, pct_depr_sga)

    # Interest Expense
    fs_is, fs_bs, metrics = fsvh.fcst_costdebt(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1)

    # Tax Expense
    fs_is, metrics = fsvh.fcst_tax(fs_is, metrics, data, fcst_yrs, fcst_yr1, taxrate_stat, flag_taxrate = 'Statutory')


    # FORECAST - BALANCE SHEET

    # Turnover-based metrics (AR, AP, Inventory)
    fs_is, fs_bs, metrics = fsvh_bs.fcst_turnratios(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'AR', 'Revenue')
    fs_is, fs_bs, metrics = fsvh_bs.fcst_turnratios(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'AP', 'COS')
    fs_is, fs_bs, metrics = fsvh_bs.fcst_turnratios(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'Inv', 'COS')

    # Goodwill
    fs_bs = fsvh_bs.fcst_goodwill(fs_bs, data, fcst_yr1,'Goodwill')

    # Other balance sheet metrics (Other CA, Other NCA, Other CL, Other NCL)
    fs_is, fs_bs, metrics = fsvh_bs.fcst_othbs(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'Other_CA', 'Revenue')
    fs_is, fs_bs, metrics = fsvh_bs.fcst_othbs(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'Other_NCA', 'Revenue')
    fs_is, fs_bs, metrics = fsvh_bs.fcst_othbs(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'Other_CL', 'Opex_NonDepr')
    fs_is, fs_bs, metrics = fsvh_bs.fcst_othbs(fs_is, fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'Other_NCL', 'Opex_NonDepr')


    # FORECAST - CASH FLOW

    # Cash from operations lines
    fs_is, fs_cf, metrics = fsvh_cf.fcst_othcfo(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1, 'Stock_Comp', 'Revenue')
    fs_is, fs_cf, metrics = fsvh_cf.fcst_othcfo(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1, 'Other_CFO', 'Revenue')

    # Cash for investment lines (ex capex)
    fs_is, fs_cf, metrics = fsvh_cf.fcst_othinv(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1)

    # Cash for financing lines
    fs_is, fs_cf, metrics = fsvh_cf.fcst_cff_stock(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1, 'CS_Issue', 'Revenue')
    fs_is, fs_cf, metrics = fsvh_cf.fcst_cff_stock(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1, 'CS_Repo', 'Revenue')
    fs_is, fs_cf, metrics = fsvh_cf.fcst_cff_ltd(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1)
    fs_is, fs_cf, metrics = fsvh_cf.fcst_othcff(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1)
    fs_is, fs_cf, metrics = fsvh_cf.fcst_cff_div(fs_is, fs_cf, metrics, data, fcst_yrs, fcst_yr1, shr_price)

    # Sub-totals
    fs_is, fs_bs, fs_cf = fsvh_cf.fcst_cf_subt(fs_is, fs_bs, fs_cf, data, yr1_begcash, fcst_yr1)

    ## FORECAST - CF DEPENDENT

    # BS Investments
    fs_bs, metrics = fsvh_bs.fcst_bsinv(fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'ST_Inv', 'Cash')
    fs_bs, metrics = fsvh_bs.fcst_bsinv(fs_bs, metrics, data, fcst_yrs, fcst_yr1, 'LT_Inv', 'Cash')


    # VALUATION
    val_df = fsvh_val.valuation_fcf(fcst_yrs, fs_is, fs_bs, fs_cf, pct_depr_sga, metrics.loc['TaxRate', fcst_yrs])
    fs_bs, metrics = fsvh_val.cost_capital(fs_bs, metrics, rfr, beta, rtn_mkt)

    gr = np.random.choice(dst_gr, 1)
    ronic = np.random.choice(dst_ronic, 1)

    cv = fsvh_val.cont_val(val_df, gr, ronic, metrics)
    sum_disc_vals = fsvh_val.disc_vals(val_df, metrics, cv)
    total_value_ps = fsvh_val.val_total(sum_disc_vals, fs_bs, fs_is, fcst_yrs)

    # STORE VALUATION DATA
    val_op.loc[sim,'Value per Share'] = total_value_ps
    val_op.loc[sim,'Growth Rate'] = gr
    val_op.loc[sim,'RONIC'] = ronic

    # print("Finished Sim #: " + str(sim))

    # FINANCIAL STATEMENT OUTPUT
    # fs_is.to_excel("FSV_OP_IS.xlsx")
    # fs_bs.to_excel("FSV_OP_BS.xlsx")
    # fs_cf.to_excel("FSV_OP_CF.xlsx")
    # metrics.loc[metric_list, :].to_excel("FSV_OP_Metr.xlsx")

val_op.to_excel("FSV_OP_Val.xlsx")


