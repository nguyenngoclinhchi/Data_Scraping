import win32com.client
import bs4


def main():
    country =list()
    outlook=win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox=outlook.GetDefaultFolder(6)
    
    count=0
    for folder in inbox.folders:
        count=count+1
        print(folder)
        if count ==1:
            ## change the count interval if changing into another outlook account,
            ## 3 is only for rmioc account -- "Macro Data" is the third mail group in rmioc
            count_1 =0
            mails=folder.items
            mails.Sort("[ReceivedTime]", True)
            mail=mails.GetFirst()
            if mail.subject =='Macro Data Validation Completed':
            
                mail=mails.GetNext()
                
                print(mail)
                
            else:
                status=mail.body[22:28]
                status_new=mail.body[44:46]
                if status =='Failed':
                    print("Macro Data Downloading failed")
                    
                else:
                    if status_new=="All":
                        print("All Econs are Trading")
                    
                    else:
                        print(mail.HTMLbody)
                        a = mail.HTMLbody
                        print(a)
                        bs_obj = bs4.BeautifulSoup(a, features = "lxml")
                        # print(bs_obj.prettify())
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
                            print(detail)
                            if detail.__len__() == 2:
                                country.append(detail[-1])
                            del detail
    print(country)
    return country

if __name__ == '__main__':
    main()
