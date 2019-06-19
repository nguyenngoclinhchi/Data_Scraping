from datetime import datetime

import bs4
import future.backports.urllib.request
import pandas.io.common
import pandas as pd
import pymysql
import pyodbc

def print_list(ls):
    for content in ls:
        print(content)

def print_meta(meta):
    for i in meta:
        print_list(i)

def crawl_cols(row):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    return cols
    
def get_bs_obj(link):
    request = future.backports.urllib.request.Request(link, headers = {'User-Agent': 'Mozilla/5.0'})
    web_page = pandas.io.common.urlopen(request)
    bs_obj = bs4.BeautifulSoup(web_page.read(), features = "lxml")
    
    tables = bs_obj.find_all('table', attrs = {'class': 'genTbl closedTbl crossRatesTbl elpTbl elp30'})
    for table in tables:
        table_body = table.find('tbody')
    
        rows = table_body.find_all('tr')
        title = table_body.find("span").attrs["title"]
        for row in rows:
            data = list()
            # cols = row.find_all('td')
            # cols = [ele.text.strip() for ele in cols]
            cols = crawl_cols(row)
            index_name = row.find("a").attrs["title"]
            index_link = "https://www.investing.com" + row.find("a").attrs["href"] + "-historical-data"
            data.append(title)
            data.append(index_name)
            data.append(index_link)
            for i in cols:
                if i:
                    data.append(i)
            meta_list.append(data)  # Get rid of empty values
    return bs_obj

def meta_to_smart(meta):
    for index in meta.head():
        for i in index:
            print(i.__len())



meta_list = list()
smart_list = list()
df = pd.read_excel('MacroData_WebsiteSources.xlsx')
df_values = pd.read_excel('Values-2019-06-18.xlsx')
df_merged = pd.merge(df, df_values, on = "ID_macro_ent", how = "outer")
df.set_index("Country", inplace = True)
link = "https://www.investing.com/indices/world-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
get_bs_obj(link)
# print_list(meta_list)
# df_meta = pd.DataFrame(meta_list)
df_meta = pd.DataFrame(meta_list, columns = ["Country", "IndexName", "IndexLink", "Index", "Last", "High", "Low", "Change", "Change%", "Time"])
df_meta = df_meta[["Country", "IndexName", "Index", "Last", "IndexLink", "High", "Low", "Change", "Change%", "Time"]]
df_meta.set_index(["Country", "IndexName"], inplace = True)
df_meta.sort_index()
for i in df.index:
    if i not in df_meta.index:
        print(i)
file = df_meta.to_excel("meta_data_investing.xlsx", index = True)
print("The file has been created")