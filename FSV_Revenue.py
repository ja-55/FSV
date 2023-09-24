import pandas as pd

data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')

data.set_index('Desc', inplace = True)

fcst_yr1 = data.columns[-1] + 1
fcst_yrs = list(range(fcst_yr1, fcst_yr1 + 3))

data = data.reindex(columns = data.columns.tolist() + fcst_yrs)

print(data)