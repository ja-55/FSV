# IMPORTS

import pandas as pd


# ARRANGE VALUATION DATAFRAME

def arrange_valdf(fcst_yrs, fs_is, fs_bs, fs_cf, pct_depr_sga, tax_rate):

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
    val_df.loc['Gross_CF', :] = val_df.loc['EBITA', :] - val_df.loc['Cash_Tax', :] - val_df.loc['Depr', :]

    # Calculate Investment
    work_cap_ca = fs_bs.loc['Cash', :] + fs_bs.loc['AR', :] + fs_bs.loc['Inv', :] + fs_bs.loc['Other_CA', :]
    work_cap_cl = fs_bs.loc['AP', :] + fs_bs.loc['Other_CL', :]
    work_cap = work_cap_ca - work_cap_cl
    work_cap_inv = work_cap.diff(axis = 1)
    
    val_df.loc['Inv_WorkCap'] = work_cap_inv.loc[:, fcst_yrs]
    val_df.loc['Capex'] = fs_cf.loc['Capex', fcst_yrs]
    val_df.loc['FCF'] = val_df.loc['Gross_CF', :] - val_df.loc['Inv_WorkCap', :] - val_df.loc['Capex', :]







    return val_df


# ### INPUTS

# years = range(2023,2028)

# ### DATAFRAME SETUPS

# ebita = pd.DataFrame(columns = years,
#                       index = ['1. Revenue','2. -COS','3. -SGA',
#                                '4. +Op Lease Int','5. xEBITA'])

# noplat = pd.DataFrame(columns = years,
#                       index = ['1. EBITA', '2. -Cash Taxes', '3. xNOPLAT'])

# gross_cf = pd.DataFrame(columns = years,
#                       index = ['1. NOPLAT','2. -Depreciation','3. xGross CF',])

# gross_inv = pd.DataFrame(columns = years,
#                          index = ['1. +Delta Op WC','2. +Net Capex',
#                                   '3. +Delta Op Lease Debt','4. +Intangible Investment',
#                                   '5. +Misc Investment', '6. xGross Investment'])

# ### CALCULATIONS

# ebita['5. xEBITA'] = ebita.sum()

# noplat['1. EBITA'] = ebita['5. xEBITA']
# noplat['3. xNOPLAT'] = noplat.sum()

# gross_cf['1. NOPLAT'] = noplat['3. xNOPLAT']
# gross_cf['3. xGross CF'] = gross_cf.sum()

# gross_inv['6. xGross Investment'] = gross_inv.sum()

# fcf = gross_cf['3. xGross CF'] - gross_inv['6. xGross Investment']



yrs = range(2018,2028)

lst_components = ['REV','COS','SGA','DEP','OLI','Cash Tax','OWC','Capex','Inv Op Lease','Inv Intang','Inv Other']
lst_totals = ['EBITA','NOPLAT','Gross CF', 'Gross Inv','FCF']

df_components = pd.DataFrame(index = lst_components, columns = yrs)
df_totals = pd.DataFrame(index = lst_totals, columns = yrs)







