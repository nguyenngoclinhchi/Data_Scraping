import pandas as pd
import numpy as np


def save_xls(list_dfs, xls_path):
    with pd.ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer, 'sheet%s' % n)
        writer.save()


def read_excel(xls_path, idx_col='PhoneNumber'):
    df = pd.read_excel(xls_path)
    df[idx_col + 'Idx'] = df[idx_col]
    df.set_index(idx_col + 'Idx', inplace=True)
    print(df.head())
    return df


table0 = read_excel('address-survey1.xlsx')
table1 = read_excel('survey1-all-ans.xlsx')
table2 = read_excel('survey2-filtered-ans.xlsx')
table3 = read_excel('status-reward-survey2.xlsx')

for i in table0.index:
    table0.loc[i, 'included in survey1'] = np.where(i in table1.index, "YES", "NO")
    table0.loc[i, 'included in survey2'] = np.where(i in table2.index, "YES", "NO")

df0 = pd.merge(table0, table3, on='PhoneNumber', how='outer')
df0.set_index('PhoneNumber', inplace=True)
df1 = pd.merge(df0, table1, on='PhoneNumber', how='outer')
df1.set_index('PhoneNumber', inplace=True)
df2 = pd.merge(df1, table2, on='PhoneNumber', how='outer')
df2.set_index('PhoneNumber', inplace=True)
save_xls([df2], 'Book3.xlsx')
