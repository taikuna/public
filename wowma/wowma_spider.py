import re
import requests
from bs4 import BeautifulSoup
import random
import pymysql.cursors
from fake_useragent import UserAgent
ua = UserAgent()
from time import sleep
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

f = open("Docs/spider.txt", "r")   # 'r' for reading and 'w' for writing
restart_id = f.read()
print(restart_id)
f.close()

s_id = int(restart_id)

while True:
    connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom',
                                 password='yH4i8Zs9LfFLjdQ')
    cursor = connection.cursor()
    sql = "SELECT `wowma_id` FROM `email_shashin` WHERE `id`=%s"
    cursor.execute(sql, (str(s_id),))
    result = str(cursor.fetchone()).replace("'",'').replace('(','').replace(')','').replace(',','')
    connection.close()
    cursor.close()

    port = '4000','4001','4002','4003','4004'
    proxies = {'https': "socks5://localhost:"+str(random.choice(port))}

    url = 'https://wowma.jp/bep/m/kmem?user=' + result

    headers = {'User-Agent': ua.random}
    try:
        r = requests.get(url,proxies=proxies,headers=headers)
        soup = BeautifulSoup(r.content,'html5lib')
        shop_info2 = soup.find(id='shopInfo2')
        email = shop_info2.find(text=re.compile('@'))
        #com_name = shop_info2.find('h3').next_sibling
        shop_info1 = soup.find(id='shopInfo1')
        pic = str(shop_info1).strip().split('<h3>通信販売業務責任者</h3>')[1].split('</p>')[0].replace('<p>','').strip()
        company = str(shop_info1).split('<h3>販売事業者名</h3>')[1].split('</p>')[0].replace('<p>','').replace(' ','').strip()
        shop_name = shop_info1.find('a').text
        phone = str(shop_info2).split('<h3>電話番号</h3>')[1].split('</p>')[0].replace('<p>', '').replace(' ', '').strip()
        street = str(shop_info2).split('<h3>住所</h3>')[1].split('</p>')[0].replace('<p>', '').replace(' ', '').strip()

        print(headers)
        print(url)
        print('pic //////'+pic)
        print('company ///////'+company)
        print('email /////' + email)
        print('shop /////' +shop_name)
        print('phone /////' + phone)
        print('street /////' + street)

        try:
            connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom', password='yH4i8Zs9LfFLjdQ')
            with connection.cursor() as cursor:
                # Create a new record
                sql = 'update email_shashin set shop_link = %s, pic = %s, company = %s, email = %s,shop = %s, phone = %s, street = %s where id =%s;'
                cursor.execute(sql, (url, pic,company,email,shop_name,phone,street, str(s_id)))
            connection.commit()
            connection.close()
        except pymysql.err.IntegrityError:
            pass
            print('email dublicate')
            connection.close()
            connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom', password='yH4i8Zs9LfFLjdQ')
            with connection.cursor() as cursor:
                # Create a new record
                sql = 'update email_shashin set note = %s where email =%s;'
                cursor.execute(sql, (url + pic + company + email + shop_name + phone + street, email))
            connection.commit()
            connection.close()

        f = open("Docs/spider.txt", "w")  # 'r' for reading and 'w' for writing
        f.write(str(s_id))
        f.close()

        sleep(3)
        s_id +=1

    except AttributeError:
        sleep(20)
    except requests.exceptions.ConnectionError:
        sleep(15)

