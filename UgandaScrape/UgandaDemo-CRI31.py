from datetime import datetime

import bs4
import future.backports.urllib.request
import pandas.io.common
import pandas as pd
import pymysql
import pyodbc


def get_bs_obj(link):
    request = future.backports.urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    web_page = pandas.io.common.urlopen(request)
    bs_obj = bs4.BeautifulSoup(web_page.read(), features="lxml")
    # print(bs_obj.prettify())
    return bs_obj

def get_code(bs_obj):
    content_code = list(bs_obj.find_all('h2'))[0].get_text()
    code = content_code.strip().replace(',', '')
    return code

def get_value(bs_obj):
    content_value = list(bs_obj.find_all('span', {"style": "font-weight:bold;font-size: 22pt"}))[0].get_text()
    value = content_value.strip().replace(' ', '').replace(',', '')
    return value

def get_date(bs_obj):
    content_date = list(bs_obj.find_all('font', {"size": "1"}))[0].get_text().split(' ')[-1]
    date = content_date.strip().split(' ')[-1]
    date_dt2 = datetime.strptime(date, '%d-%b-%Y')
    print(date_dt2)
    print(date_dt2.strftime('%Y-%m-%d'))
    return date_dt2.strftime('%Y-%m-%d')

def create_query(macro_id, source, date, value):
    query = 'EXECUTE TIER2.PROD.SP_INSERT_RATE ' + str(macro_id) + ', ' + str(source) + ', \'' + str(date) + '\', ' + str(value)
    print(query)
    return query

def print_details(country_name, link, id_macro_ent, source):
    country = Country_stock_index(country_name, link, id_macro_ent, source)
    print(country.country_name, country.code, country.date, country.value, country.link, country.id, country.source)
    list_query.append(create_query(country.id, country.source, country.date, country.value))
    list_name.append(country.country_name)
    list_code.append(country.code)
    list_date.append(country.date)
    list_value.append(country.value)
    list_link.append(country.link)
    list_id.append(country.id)
    list_source.append(country.source)

def get_details(data_frame):
    name_list = data_frame['Country'].values
    for name in name_list:
        country = data_frame['Country'] == name
        website = (data_frame[country])['Website'].values[0]
        id_macro_ent = (data_frame[country])['ID_macro_ent'].values[0]
        source = (data_frame[country])['Source'].values[0]
        print_details(name, website, id_macro_ent, source)

def connect_mysql_server(result):
    file = pd.read_excel(result)
    connection = pymysql.connect(host='localhost', user='root', password='139/6/4_Kitty123', db='criweb_admin')
    cursor = connection.cursor()
    sql = 'SELECT * FROM `django_content_type`;'
    cursor.execute(sql)
    count_row = cursor.execute(sql)
    print("Number of rows: ", count_row)
    # fetchone: show only one result - the first line
    # fetchall: show all the results
    # fetchmany: show the specific number of results
    data_one = cursor.fetchone()
    data_all = cursor.fetchall()
    for data in data_all:
        print(data)
        for i in data:
            print(i)
    # print(data_one)
    # print(data_all)

class Country_stock_index(object):
    def __init__(self, country_name, link, id_macro_ent, source):
        self.country_name = country_name
        self.id = id_macro_ent
        self.source = source
        bs_obj = get_bs_obj(link)
        self.code = get_code(bs_obj)
        self.date = get_date(bs_obj)
        self.value = get_value(bs_obj)
        self.link = link

    def get_country_name(self):
        return self.country_name

list_name = list()
list_code = list()
list_date = list()
list_value = list()
list_link = list()
list_id = list()
list_source = list()
list_query = list()
file_name = 'MacroData_WebsiteSources - Copy.xlsx'
df_raw = pandas.read_excel(file_name)
get_details(df_raw)
zipped = list(zip(list_id, list_name, list_code, list_date, list_value, list_link, list_source, list_query))
df_result = pd.DataFrame(zipped)
print(df_result)
headers = ['ID_macro_ent', 'Country name', 'INDEX', 'Trading Date', 'Value', 'Link', 'Source', 'Query']
df_result.to_excel('smart_data.xlsx', index=False, header=headers)
print("The Excel File has been successfully created in D:\Kitty\IT_Professionalism\Machine_Learning")
# connect_mysql_server(file_name)
