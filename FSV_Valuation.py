### IMPORTS

import pandas as pd

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







