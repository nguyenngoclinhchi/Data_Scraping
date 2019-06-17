import pandas as pd

table1 = pd.read_excel('Book1.xlsx')
table2 = pd.read_excel('Book2.xlsx')

table3 = pd.merge(table1, table2, on='PhoneNumber', how='left')
file = pd.DataFrame(table3).to_excel('Book3.xlsx', index=False)