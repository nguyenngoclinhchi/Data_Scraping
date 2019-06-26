import smtplib
from tabulate import tabulate

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MY_ADDRESS = 'e0196722@u.nus.edu'
PASSWORD = '139/6/4_DuongVanDuong123'


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
            table = tabulate(text_1, headers = header, tablefmt = "github")
            print(table)
            f.write(table)
            f.write("\r\n")
    f.write("Regards, \nChi.")
    f.close()
    
def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode = 'r', encoding = 'utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """
    
    with open(filename, 'r', encoding = 'utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main(trading_date, country_detail):
    names, emails = get_contacts('mycontacts.txt')  # read contacts
    generate_message_txt(country_detail)
    message_template = read_template('message.txt')
    
    # set up the SMTP server
    s = smtplib.SMTP(host = 'smtp-mail.outlook.com', port = 587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    
    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message
        
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME = name.title(), TRADING_DATE=trading_date)
        
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


if __name__ == '__main__':
    main()
    