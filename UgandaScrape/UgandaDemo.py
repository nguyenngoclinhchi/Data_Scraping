import bs4
import future.backports.urllib.request
import pandas.io.common


def get_bs_obj(link):
    request = future.backports.urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    web_page = pandas.io.common.urlopen(request)
    bs_obj = bs4.BeautifulSoup(web_page.read(), features="lxml")
    # print(bs_obj.prettify())
    return bs_obj

def get_code(bs_obj):
    content_code = list(bs_obj.find_all('h2'))[0].get_text()
    print(content_code.strip().replace(',', ''))
    return content_code

def get_value(bs_obj):
    content_value = list(bs_obj.find_all('span', {"style": "font-weight:bold;font-size: 22pt"}))[0].get_text()
    print(content_value.strip().replace(',', ''))
    return content_value

def get_date(bs_obj):
    content_date = list(bs_obj.find_all('span', {"style": "font-size:7pt"}))[0].get_text()
    print(content_date.strip().replace(',', ''))
    return content_date


class country_stock_index(object):
    def __init__(self, country_name, link):
        self.country_name = country_name
        bs_obj = get_bs_obj(link)
        self.code = get_code(bs_obj)
        self.date = get_date(bs_obj)
        self.value = get_value(bs_obj)
        self.link = link

    def get_country_name(self):
        return self.country_name


# for content in content_body:
#     content.extract()
#     print(content)

file = pandas.read_excel('MacroData_WebsiteSources.xlsx')
df = pandas.DataFrame(file, columns= ['ID_macro_ent', 'Country', 'Source'])
# print (df)

