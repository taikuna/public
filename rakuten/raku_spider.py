#楽天市場出品者情報スクレイピングツール
#  -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
import time
import random
import ssl
import subprocess
from fake_useragent import UserAgent
ssl._create_default_https_context = ssl._create_unverified_context
import pymysql.cursors
from time import sleep
ua = UserAgent()
port = 9234
sql_port = 8889
_user_agents = ua.random
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+str(port))
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)


f = open("Docs/raku_spi.txt", "r")   # 'r' for reading and 'w' for writing
txt = f.read()
print(txt)
restart_id = txt
f.close()
s_id = int(restart_id)

while True:
    connection = pymysql.connect(host='127.0.0.1',port=sql_port, database='bloomdb',user='bloom',password='password_here')
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
        start = time.time()
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        time = datetime.now()
        driver.get(info_link)
        sleep(4)

        try:
            picss = soup.find('dd',text=re.compile('店舗運営責任者'))
            pic_shop = picss.get_text().replace('  ','').replace('\n','').replace('店舗運営責任者:','').strip()
            print('pic_shop is ' +pic_shop)
        except AttributeError:
            pass
            pic_shop = ''
        try:
            emails = soup.find('a',href=re.compile('mailto:'))
            email = emails.get_text().split(',')[0]
            print('email/////  ' + str(email))
        except AttributeError:
            pass
            print('////// No email')
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

        connection = pymysql.connect(host='127.0.0.1', port=sql_port,database='bloomdb',user='bloom',password='password_here')
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT IGNORE `rakuten_list` (`time`, `URL`,`company`,`pic`,pic_shop,`email`,`category`,`phone`,`street`,`shop`,`page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;"
            cursor.execute(sql, (time,url,company,pic,pic_shop,email,category,phone,street,shop,page))
        connection.commit()
        connection.close()
        cursor.close()

        s_id+=1
        f = open("Docs/raku_spi.txt", "w")  # 'r' for reading and 'w' for writing
        f.write(str(s_id))
        f.close()

    except IndexError:
        print('ID ' + str(s_id)+' is EMPTY')
        s_id +=1
        pass
    if s_id >= 100000:
        break
