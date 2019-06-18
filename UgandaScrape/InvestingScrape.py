from datetime import datetime

import bs4
import future.backports.urllib.request
import pandas.io.common
import pandas as pd
import pymysql
import pyodbc


def get_bs_obj(link):
    request = future.backports.urllib.request.Request(link, headers = {'User-Agent': 'Mozilla/5.0'})
    web_page = pandas.io.common.urlopen(request)
    bs_obj = bs4.BeautifulSoup(web_page.read(), features = "lxml")
    market = ''
    indices = ''
    for i in bs_obj.find_all("a"):
        if 'href' in i.attrs and ('/markets/' in i.attrs['href'] or '/indices/' in i.attrs['href']):
            market = i.attrs['href'] if '/markets/' in i.attrs['href'] else market
            indices = i.attrs['href'] if '/indices/' in i.attrs['href'] else indices
            print(market, indices)
    # print(bs_obj.prettify())
    return bs_obj


link = "https://www.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
get_bs_obj(link)

