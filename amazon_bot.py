from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage


def sending_a_mail(float_price):
    """
    Function sends email to the specific adress using gmail
    :param float_price: 
    :return: 
    """
    USERNAME = 'your gmail username'
    PASSWORD = 'your gmail password'

    msg = EmailMessage()
    msg['Subject'] = "Price DROP"
    msg['From'] = USERNAME
    msg['To'] = 'email'
    msg.set_content(f'Your item price has dropped to: {float_price} €')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(USERNAME, PASSWORD)
        smtp.send_message(msg)

#Url of specific item you want to track price of
url = 'https://www.amazon.de/-/pl/dp/B078Y9QT8P/ref=sr_1_3?__mk_pl_PL=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=osu&qid=1608658371&sr=8-3'

#Webdriver config
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver.exe', options=options)

driver.get(url)
driver.refresh()
soup = BeautifulSoup(driver.page_source, 'lxml')

#Getting current price of an item
price = soup.find(id="price_inside_buybox")
float_price = price.text[0:6].replace(',', '.')

if float(float_price) < 39.99:
    #If there is a price drop function sends an email with the currenc price
    sending_a_mail(float_price)
    print("done")
else:
    print('Nothing changed')
