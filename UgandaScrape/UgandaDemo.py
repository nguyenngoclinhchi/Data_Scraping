import bs4
import future.backports.urllib.request
import pandas
import pandas.io.common

class country_stock_index(object):
    def __init__(self, country_name, code, date, value):
        self.country_name = country_name
        self.code = code
        self.date = date
        self.value = value

req = future.backports.urllib.request.Request('https://www.african-markets.com/en/stock-markets/use',
                                              headers={'User-Agent': 'Mozilla/5.0'})
webPage = pandas.io.common.urlopen(req)
bsObj = bs4.BeautifulSoup(webPage.read(), features="lxml")
# print(bsObj.prettify())
content_country = list(bsObj.find_all('h2'))[0].get_text()
content_value = list(bsObj.find_all('span', {"style": "font-weight:bold;font-size: 22pt"}))[0].get_text()
content_date  = list(bsObj.find_all('span', {"style": "font-size:7pt"}))[0].get_text()
# for content in content_body:
#     content.extract()
#     print(content)
print(content_country.strip().replace(',', ''))
print(content_value.strip().replace(',', ''))
print(content_date.strip().replace(',', ''))

file = pandas.read_excel('D:\\Kitty\\NUS\\2-INTERNSHIP-PART-TIME-JOB\\RMI-CRI\\MacroData_WebsiteSources.xlsx')
df = pandas.DataFrame(file, columns= ['ID_macro_ent', 'Country', 'Source'])
print (df)
