from datetime import datetime
from tabulate import tabulate
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime as dt
import bs4
import future.backports.urllib.request
import pandas.io.common
import pandas as pd
import pymysql
import pyodbc
import win32com.client
import smtplib

MY_ADDRESS = 'e0196722@u.nus.edu'
PASSWORD = '139/6/4_DuongVanDuong'


def generate_message_txt(details):
    f = open("message.txt", "w+")
    f.write("Dear ${PERSON_NAME},\r\n")
    f.write("The following economies were trading on ${TRADING_DATE}:\r\n")
    for detail in details:
        for i in detail:
            header = ['ID', 'ID_macro_ent', 'Source', 'REVISION_ID', 'FLAG', 'Data_date', 'Value', 'Update_lock']
            text = str(i).replace('False', '0')
            text_1 = [text.replace("(", "").replace(")", "").split(", ")]
            print(text_1)
            table = tabulate(text_1, headers=header, tablefmt="github")
            print(table)
            f.write(table)
            f.write("\r\n")
    f.write("Regards, \nChi.")
    f.close()


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_previous_working_day(working_date):
    if working_date.weekday() == 0:
        return (working_date - dt.timedelta(days=3)).strftime('%Y-%m-%d')
    else:
        return (working_date - dt.timedelta(days=1)).strftime('%Y-%m-%d')


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
    query = 'EXECUTE TIER2.PROD.SP_INSERT_RATE ' + str(macro_id) + ', ' + str(source) + ', \'' + str(
        date) + '\', ' + str(value)
    print(query)
    return query


def print_details(country_name, link, country_macro_ent, source):
    country_obj = country_stock_index(country_name, link, country_macro_ent, source)
    print(country_obj.country_name, country_obj.code, country_obj.date, country_obj.value, country_obj.link,
          country_obj.id,
          country_obj.source)
    list_query.append(create_query(country_obj.id, country_obj.source, country_obj.date, country_obj.value))
    list_name.append(country_obj.country_name)
    list_code.append(country_obj.code)
    list_date.append(country_obj.date)
    list_value.append(country_obj.value)
    list_link.append(country_obj.link)
    list_id.append(country_obj.id)
    list_source.append(country_obj.source)


def get_details(data_frame):
    name_list = data_frame['Country'].values
    for name in name_list:
        condition = data_frame['Country'] == name
        website = (data_frame[condition])['Website'].values[0]
        id_macro = (data_frame[condition])['ID_macro_ent'].values[0]
        source = (data_frame[condition])['Source'].values[0]
        print_details(name, website, id_macro, source)


def connect_mysql_server(result):
    connection = pymysql.connect(host='localhost', user='LinhChi', password='139/6/4_Chi', db='criweb_admin')
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


def connect_microsoft_server_management(country_id, country_date, sql):
    output = list()
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=dirac\dirac2012;'
                                'Database=Tier2;'
                                'Trusted_Connection=yes;')
    cursor = connection.cursor()
    test_sql = "SELECT * FROM Tier2.dat.macro WHERE id_macro_ent=" + country_id + " and Data_date=" + "'" + country_date + "'"

    print(sql)

    cursor.execute(sql)
    for row in cursor:
        print(row)
        output.append(row)

    # cursor.execute(test_sql)
    # for row in cursor:
    #     print(row)
    #     output.append(row)

    return output


def read_email_get_trading_economies():
    non_trading_countries = list()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    count = 0
    for folder in inbox.folders:
        count = count + 1
        print(folder)
        if count == 1:
            # change the count interval if changing into another outlook account,
            # 3 is only for rmioc account -- "Macro Data" is the third mail group in rmioc
            mails = folder.items
            mails.Sort("[ReceivedTime]", True)
            mail = mails.GetFirst()
            while mail.subject == 'Macro Data Validation Completed':
                mail = mails.GetNext()
            print("----------------------------------------- Email Detected --------------------------------------")
            print(mail)
            status = mail.body[22:28]
            status_new = mail.body[44:46]
            if status == 'Failed':
                print("Macro Data Downloading failed")

            else:
                if status_new == "All":
                    print("All Econs are Trading")

                else:
                    print(mail.HTMLbody)
                    a = mail.HTMLbody
                    # print(a)
                    bs_obj = bs4.BeautifulSoup(a, features="lxml")
                    print(bs_obj.prettify())
                    table_list = bs_obj.find_all("table")
                    table_trading = table_list[-1]
                    # print(table_trading.prettify())
                    tr_list = table_trading.find_all("tr")
                    for tr in tr_list:
                        td_list = tr.find_all("td")
                        detail = list()
                        for td in td_list:
                            p_element = td.find("p")
                            if p_element is not None:
                                print(p_element.text.strip())
                                detail.append(p_element.text.strip())
                            else:
                                detail.append(td.text.strip())
                        print(detail)
                        non_trading_countries.append(detail)
    print(non_trading_countries)
    non_trading_countries = pd.DataFrame(non_trading_countries)
    return non_trading_countries


def send_email(trading_date, detail):
    names, emails = get_contacts('mycontacts.txt')  # read contacts
    generate_message_txt(detail)
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(), TRADING_DATE=trading_date)
        # Prints out the message body for our sake
        print(message)
        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "The following economies were trading on " + trading_date
        msg['Content-type'] = "text/html"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
    # Terminate the SMTP session and close the connection
    s.quit()


class country_stock_index(object):
    def __init__(self, country_name, link, id_macro, source):
        self.country_name = country_name
        self.id = id_macro
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
df_result.columns = headers
df_result.set_index('Country name', inplace=True)

country_detail = list()
df_result.to_excel('smart_data.xlsx', index=False)
date = str(get_previous_working_day(pd.datetime.today()))
country_list = read_email_get_trading_economies()
print(country_list)
country_list.columns = ['Date', 'Country', 'Market', 'Type', 'Holiday']
print(country_list)
countries = country_list[country_list['Holiday'] == '']['Country'].tolist()
for country in countries:
    if country in df_result.index:
        print('-------------------------------------------------------------------------------------------------------')
        print('Country: ', country)
        sql_query = df_result.loc[country, 'Query']
        id_macro_ent = str(df_result.loc[country, 'ID_macro_ent'])
        if str(df_result.loc[country, 'Trading Date']) == date:
            print('Executing SQL Server Management Query')
            country_output = connect_microsoft_server_management(id_macro_ent, date, sql_query)
            country_detail.append(country_output)
        else:
            country_output = "The website has not update information for" + country + "on the date: " + date
send_email(date, country_detail)
