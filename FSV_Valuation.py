# IMPORTS

import pandas as pd


# ARRANGE VALUATION DATAFRAME

def valuation_fcf(fcst_yrs, fs_is, fs_bs, fs_cf, pct_depr_sga, tax_rate):

    lines_ebita = ['Revenue','COS','SGA','Depr']

    val_df = pd.DataFrame(index = lines_ebita, columns = fcst_yrs)

    # Assign values from forecast
    val_df.loc['Revenue', :] = fs_is.loc['Revenue', fcst_yrs]
    val_df.loc['COS', :] = fs_is.loc['COS', fcst_yrs] - fs_is.loc['Depr', fcst_yrs] * (1 - pct_depr_sga)
    val_df.loc['SGA', :] = fs_is.loc['Opex_NonDepr', fcst_yrs]
    val_df.loc['Depr', :] = fs_is.loc['Depr', fcst_yrs]

    # Calculate Gross CF
    val_df.loc['EBITA', :] = val_df.loc['Revenue', :] - val_df.loc['COS', :] - val_df.loc['SGA', :]
    val_df.loc['Cash_Tax', :] = val_df.loc['EBITA', :] * tax_rate
    val_df.loc['NOPLAT', :] = val_df.loc['EBITA', :] - val_df.loc['Cash_Tax', :]
    val_df.loc['Gross_CF', :] = val_df.loc['NOPLAT', :] - val_df.loc['Depr', :]

    # Calculate Investment
    work_cap_ca = fs_bs.loc['Cash', :] + fs_bs.loc['AR', :] + fs_bs.loc['Inv', :] + fs_bs.loc['Other_CA', :]
    work_cap_cl = fs_bs.loc['AP', :] + fs_bs.loc['Other_CL', :]
    work_cap = work_cap_ca - work_cap_cl
    work_cap_inv = work_cap.diff(periods = 1)
    
    val_df.loc['Inv_WorkCap', :] = work_cap_inv[fcst_yrs]
    val_df.loc['Capex', :] = fs_cf.loc['Capex', fcst_yrs]
    val_df.loc['FCF', :] = val_df.loc['Gross_CF', :] - val_df.loc['Inv_WorkCap', :] - val_df.loc['Capex', :]

    return val_df


def cost_capital(fs_bs, metrics, rfr, beta, rtn_mkt):

    # Calculate debt / asset ratio
    lst_ast = ['Cash', 'ST_Inv', 'LT_Inv', 'AR', 'Inv', 'Other_CA', 'Other_NCA', 'Goodwill', 'PPE_Net', 'IA_Net']
    fs_bs.loc['Tot_Assets', :] = fs_bs.loc[lst_ast, :].sum()
    metrics.loc['Debt_to_Assets', :] = fs_bs.loc[['LTD_Current','LTD_NonCurrent'], :].sum() / fs_bs.loc['Tot_Assets', :]

    # Calculate cost of capital
    coc_debt = metrics.loc['Debt_to_Assets', :] * (metrics.loc['Cost_Debt', :] * (1 - metrics.loc['TaxRate', :]))
    coc_equity = (1 - metrics.loc['Debt_to_Assets', :]) * (rfr + beta * (rfr + rtn_mkt))
    metrics.loc['Cost_Capital', :] = coc_debt + coc_equity

    return fs_bs, metrics


def cont_val(val_df, gr_rate, ronic, metrics):

    cv_factor = (1 - (gr_rate / ronic)) / (metrics.loc['Cost_Capital', max(val_df.columns)] - gr_rate)

    gr_noplat_fcst = val_df.loc['NOPLAT', max(val_df.columns)] / val_df.loc['NOPLAT', min(val_df.columns)] ** (1 / (max(val_df.columns) - min(val_df.columns))) - 1

    cv = val_df.loc['NOPLAT', max(val_df.columns)] * (1 + gr_noplat_fcst) * cv_factor

    return cv

def disc_vals(val_df, metrics, cv):

    sum_disc_vals = 0

    for yr in val_df.columns:

        disc_factor = 1 / ((1 + metrics.loc['Cost_Capital', yr]) ** (yr - min(val_df.columns) + 1))
        fcf_disc = val_df.loc['FCF', yr] * disc_factor
        sum_disc_vals = sum_disc_vals + fcf_disc

    disc_factor_cv = 1 / ((1 + metrics.loc['Cost_Capital', max(val_df.columns)]) ** (max(val_df.columns) - min(val_df.columns) + 2))

    sum_disc_vals = sum_disc_vals + cv * disc_factor_cv

    return sum_disc_vals


def val_total(sum_disc_vals, fs_bs, fs_is, fcst_yrs):

    crnt_yr = min(fcst_yrs) - 1
    tot_debt = fs_bs.loc['LTD_Current', crnt_yr] + fs_bs.loc['LTD_NonCurrent', crnt_yr]
    fin_ast = fs_bs.loc['ST_Inv', crnt_yr] + fs_bs.loc['LT_Inv', crnt_yr]
    total_value = sum_disc_vals - tot_debt + fin_ast

    total_value_ps = total_value / fs_is.loc['Shares', crnt_yr]

    print(total_value)
    print(fs_is.loc['Shares', crnt_yr])

    return total_value_ps