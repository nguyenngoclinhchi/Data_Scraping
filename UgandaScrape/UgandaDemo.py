from datetime import datetime

import bs4
import future.backports.urllib.request
import pandas.io.common
import pandas as pd


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
    print(date_dt2.strftime('%Y%m%d'))
    return date_dt2.strftime('%Y%m%d')

def print_details(country_name, link, id_macro_ent):
    country = Country_stock_index(country_name, link, id_macro_ent)
    print(country.country_name, country.code, country.date, country.value, country.link, country.id)
    list_country_name.append(country.country_name)
    list_country_code.append(country.code)
    list_country_date.append(country.date)
    list_country_value.append(country.value)
    list_country_link.append(country.link)
    list_country_id.append(country.id)

def get_details(data_frame):
    name_list = data_frame['Country'].values
    for name in name_list:
        country = data_frame['Country'] == name
        website = (data_frame[country])['Website'].values[0]
        id_macro_ent = (data_frame[country])['ID_macro_ent'].values[0]
        print_details(name, website, id_macro_ent)


class Country_stock_index(object):
    def __init__(self, country_name, link, id_macro_ent):
        self.country_name = country_name
        self.id = id_macro_ent
        bs_obj = get_bs_obj(link)
        self.code = get_code(bs_obj)
        self.date = get_date(bs_obj)
        self.value = get_value(bs_obj)
        self.link = link

    def get_country_name(self):
        return self.country_name

list_country_name = list()
list_country_code = list()
list_country_date = list()
list_country_value = list()
list_country_link = list()
list_country_id = list()
file = pandas.read_excel('MacroData_WebsiteSources - Copy.xlsx')
df = pandas.DataFrame(file, columns=['ID_macro_ent', 'Country', 'Source', 'Website'])
get_details(df)

zipped = list(zip(list_country_id, list_country_name, list_country_code, list_country_value, list_country_date, list_country_link))
df = pd.DataFrame(zipped, columns=['ID_macro_ent', 'Country Name', 'Index Code', 'Value', 'Date', 'Link'])
df.to_excel('file_clean.xlsx', index=False)