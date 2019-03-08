# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import pymysql.cursors
from time import sleep
import subprocess
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from fake_useragent import UserAgent
ua = UserAgent()
utm_medium= 'rakuten'

f = open("Docs/scan.txt", "r")   # 'r' for reading and 'w' for writing
txt = f.read()
print(txt)
restart_page = txt.split(',')[1]
restart_cat_id = txt.split(',')[0]
f.close()

p_port = '4000','4001','4002','4003','4004'

port = 9233
cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port="+str(port)+" --no-first-run --incognito -default-browser-check --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir') --proxy-server=socks5://localhost:4000"
#process = subprocess.Popen(cmd,shell=True)
#google-chrome-stable --headless --remote-debugging-port=9230 --no-first-run --incognito -default-browser-check --proxy-server=socks5://localhost:4006
_user_agents = ua.random
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+str(port))
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
cat_id = int(restart_cat_id)

while True:
    new_c = 0
    pg=1
    pg_p =1
    ID = 1
    while True:
        f = open("Docs/category.txt", "r")  # 'r' for reading and 'w' for writing
        txt = f.read()
        category_id = txt.split(',')[cat_id]
        f.close()
        print(category_id)

        url = 'https://search.rakuten.co.jp/search/mall/-/'+category_id+'/?p='+str(pg)
        print(url)
        start = time.time()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        status = soup.title.text
        print(status)
        if 'アクセスが集中しております' in status:
            print('wait a moment.....')
            sleep(60)
        else:
            try:
                search = soup.find(class_='_big section keyword _break').get_text()
                print(search)
            except AttributeError:
                pass
                search = str(cat_id)
            stop = time.time()

            for info in soup.find_all('a',{'data-track-action':'shop'}):
                time = datetime.now()
                category = search.replace('\n','')
                page =str(pg)

                try:
                    URL = info.get('href')
                except AttributeError:
                    pass
                    URL = 'None'

                try:
                    shop = info.get_text()
                    print(shop)
                except AttributeError:
                    pass
                    shop = 'None'
                company =''
                phone = ''
                street = ''
                pic = ''
                email = ''
                connection = pymysql.connect(host='127.0.0.1',port=3306, database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT IGNORE `scan_rakuten` (`time`, `URL`,`company`,`pic`,`email`,`category`,`phone`,`street`,`shop`,`page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;"
                    cursor.execute(sql, (time, URL, company,pic,email,category,phone,street,shop,page))
                    #ON DUPLICATE KEY UPDATE URL = %s
                    print(URL)

                connection.commit()
                connection.close()
                ID += 1

            print('Loading time')
            print('Page is '+str(pg))
            f = open("Docs/scan.txt", "w")  # 'r' for reading and 'w' for writing
            f.write(str(cat_id) + ',' + str(pg))
            f.close()
            pg+=1
            sleep(4)

            if pg >= 500:
                cat_id += 1
                break

