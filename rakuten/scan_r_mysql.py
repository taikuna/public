# -*- coding: utf-8 -*-
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import pandas as pd
from pandas.io import sql
import pymysql.cursors
from time import sleep
from fake_useragent import UserAgent
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

port = '4000','4001','4002'
ua = UserAgent()
header = {'User-Agent':str(ua.random)}
print(header)

url = 'https://www.whatismyip.net/'
proxies = {'https': "socks5://localhost:"+str(random.choice(port))}
r = requests.get(url,proxies=proxies)
soup = BeautifulSoup(r.content,'lxml')
table = soup.find_all(class_='table table-striped table-hover')[0]
df = pd.read_html(str(table),index_col= 0)

IP= df[0].at['IP Address:',1].split(' ')[0]+':'+str(port)
print(IP)
csv_input = pd.read_csv(filepath_or_buffer='cat_list.csv', sep=",")
row = 1

while True:
    new_c = 0
    pg=1
    list_a=[]
    pg_p =1
    ID = 1
    while True:
        proxies = {'https': "socks5://localhost:"+str(random.choice(port))}
        print(proxies)
        urls = csv_input.values[row,1]
        cat_no = urls.split('/')[4]
        print(cat_no)
        keyword= csv_input.values[row,2]
        url = 'https://search.rakuten.co.jp/search/mall/-/'+str(cat_no)+'/?p='+str(pg)
        print(url)
        start = time.time()
        r = requests.get(url,proxies=proxies)
        soup = BeautifulSoup(r.content,'html5lib')
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
                search = str(cat_no)
            stop = time.time()

            for info in soup.find_all('a',{'data-track-action':'shop'}):
                time = datetime.now()
                category = search.replace('\n','')
                page =str(pg)
                IP =IP

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
                connection = pymysql.connect(host='127.0.0.1',port=3307, database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT IGNORE `scan_rakuten` (`time`, `URL`,`company`,`pic`,`email`,`category`,`phone`,`street`,`shop`,`page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;"
                    cursor.execute(sql, (time, URL, company,pic,email,category,phone,street,shop,page))
                    #ON DUPLICATE KEY UPDATE URL = %s
                    print(URL)

                connection.commit()

                ID += 1

            print('Loading time')
            print('Page is '+str(pg))
            pg+=1

            if pg >= 100:
                row+=1
                connection.close()
                break