# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import requests
import time
import random
import ssl
import subprocess
from tabulate import tabulate
from fake_useragent import UserAgent
ssl._create_default_https_context = ssl._create_unverified_context
import pymysql.cursors
from time import sleep

port = '4009','4010'

url = 'https://www.whatismyip.net/'
proxies = {'https': "socks5://localhost:"+str(random.choice(port))}

url = 'https://www.whatismyip.net/'
ua = UserAgent()
header = {'User-Agent':str(ua.random)}
print(header)

r = requests.get(url,proxies=proxies,headers=header)
soup = BeautifulSoup(r.content,'html5lib')
table = soup.find_all(class_='table table-striped table-hover')[0]
df = pd.read_html(str(table),index_col= 0)
print( tabulate(df[0], headers='keys', tablefmt='grid') )

IP= df[0].at['IP Address:',1].split(' ')[0]+':'+str(port)
print(IP)

s_id = 7000
while True:
    proxies = {'https': "socks5://localhost:"+str(random.choice(port))}
    connection = pymysql.connect(host='127.0.0.1', database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
    cursor = connection.cursor()
    sql = "SELECT `id`, `URL` ,`category`,`shop`,`page` FROM `scan_rakuten` WHERE `id`=%s"
    cursor.execute(sql, (str(s_id),))
    result = cursor.fetchone()
    print(result)
    sqlinfo = str(result).replace("'",'')
    try:
        url = str(sqlinfo).split(",")[1]
        category = str(sqlinfo).split(",")[2]
        shop = str(sqlinfo).split(",")[3].replace('\u3000','')
        page = str(sqlinfo).replace(')','').split(",")[4]
        info_link = url + 'info.html'
        connection.close()
        cursor.close()

        r = requests.get(info_link,proxies=proxies)
        start = time.time()
        soup = BeautifulSoup(r.content, 'html5lib')

        emails = set()
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.text, re.I))
        emails.update(new_emails)
        print(emails)
        time = datetime.now()

        try:
            picss = soup.find('dd',text=re.compile('店舗運営責任者'))
            pic_shop = picss.get_text().replace('  ','').replace('\n','').replace('店舗運営責任者:','').strip()
            print('pic_shop is ' +pic_shop)
        except AttributeError:
            pass
            pic_shop = ''
        try:
            emails = soup.find('dd',text=re.compile('店舗連絡先:'))
            email = emails.get_text().replace('  ','').replace('\n','').replace('店舗連絡先:','').strip()
        except AttributeError:
            pass
            email = ''

        try:
            streets = soup.find('dd',text=re.compile('〒'))
            street = streets.get_text().replace('  ','').strip()
            print('street is '+ street)
        except AttributeError:
            pass
            street = ''

        try:
            pics = soup.find('dd',text=re.compile('代表者'))
            pic = pics.get_text().replace('  ','').replace('\n','').replace('代表者:','').strip()
            print('pic is ' + pic)
        except AttributeError:
            pass
            pic = ''

        try:
            c_name = soup.find('dt',text=re.compile('会社'))
            company = c_name.get_text().replace('  ','').replace('\n','').strip()
            print('company is ' + company)
        except AttributeError:
            pass
            company = ''

        try:
            phones = soup.find('dd',text=re.compile('TEL:'))
            phone = phones.get_text().replace('  ','').replace('\n','').strip()
            print('phone is ' + phone)
        except AttributeError:
            pass
            phone = ''

        t_email = str(emails).replace("{",'').replace("}",'').replace("'",'').replace(' ','')
        email_count = str(t_email).count('@')

        if email_count == 0:
            email = ''
            print('true')
        elif email_count == 1:
            counter = 0
        else: counter = email_count-1

        while True:
            email = t_email.split(',')[counter]
            connection = pymysql.connect(host='127.0.0.1', database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT IGNORE `rakuten_list` (`time`, `URL`,`company`,`pic`,pic_shop,`email`,`category`,`phone`,`street`,`shop`,`page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;"
                cursor.execute(sql, (time,url,company,pic,pic_shop,email,category,phone,street,shop,page))
            connection.commit()
            connection.close()
            cursor.close()
            print('email'+str(counter)+' is '+email)

            if counter == 0:
                break
            counter -=1

        s_id+=1
    except IndexError:
        print('ID ' + str(s_id)+' is EMPTY')
        s_id +=1
        pass
    sleep(15)
    if s_id >= 100000:
        break
