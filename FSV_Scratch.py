import pandas as pd

data = pd.read_excel('FSV_Input.xlsx', sheet_name = 'Grid')

data.set_index('Desc', inplace = True)

print(data)