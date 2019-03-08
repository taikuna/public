# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import pymysql
from fake_useragent import UserAgent
ua = UserAgent()
import subprocess

utm_medium= 'wowma'

port = 9230

# for GCP chrome
#google-chrome-stable --headless --remote-debugging-port=9230 --no-first-run --incognito -default-browser-check --proxy-server=socks5://localhost:4006

# for mac local
cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port="+str(port)+" --no-first-run --incognito -default-browser-check --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir') --proxy-server=socks5://localhost:4000"
#process = subprocess.Popen(cmd,shell=True)

_user_agents = ua.random
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+str(port))
#chrome_options.add_argument('headless')
#chrome_options.add_argument('window-size=1200x600')
#chrome_options.add_argument("--proxy-server=socks5://localhost:"+random.choice(p_port));
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

while True:
    f = open("Docs/scan.txt", "r")   # 'r' for reading and 'w' for writing
    txt = f.read()
    print(txt)
    restart_page = txt.split(',')[1]
    restart_cat_id = txt.split(',')[0]
    f.close()
    cat_id = int(restart_cat_id)

    connection = pymysql.connect(host='127.0.0.1',port=3307, database='bloomdb', user='bloom',
                                 password='yH4i8Zs9LfFLjdQ')
    cursor = connection.cursor()

    sql = "SELECT `cat_no` FROM `wowma_category` WHERE `id`=%s"
    cursor.execute(sql, (str(cat_id),))
    result = str(cursor.fetchone()).replace("'", '').replace('(', '').replace(')', '').replace(',', '')
    connection.close()
    cursor.close()
    cat_no = int(result)
    print(result)

    pg = int(restart_page)
    stop = 50

    while True:
        print('category num ' + str(cat_no) + ' page ' + str(pg) + ' starting....')
        url = 'https://wowma.jp/bep/m/klist3?at=FP&sort1=ppop30%2Cd&categ_id=' + str(
            cat_no) + '&e_scope=O&srm=Y&non_gr=ex&page=' + str(pg) + '&clk=page_next' + str(pg)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        title = soup.title.text.split('の人気商品一覧')[0]
        page = soup.find(class_='headingSeachCount').text
        print(title + page)

        for img in soup.find_all(class_='productImage'):
            shop_link = img.find('img').get('src')
            if 'image.wowma.jp/' in shop_link:
                shop_id = shop_link.split('/')[7]
                if 'image.wowma.jp' in shop_id:
                    shop_id = shop_link.split('/')[8]

                print(shop_id)
                connection = pymysql.connect(host='127.0.0.1', port=3307, database='bloomdb', user='bloom',
                                             password='yH4i8Zs9LfFLjdQ')
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT IGNORE `email_shashin` (`wowma_id`,`page`,`category`,`utm_medium`) VALUES (%s, %s, %s, %s) ;"
                    cursor.execute(sql, (shop_id, page, title, utm_medium))
                    # ON DUPLICATE KEY UPDATE URL = %s

                connection.commit()
                connection.close()

        pg += 1
        sleep(4)
        f = open("Docs/scan.txt", "w")  # 'r' for reading and 'w' for writing
        f.write(str(cat_id)+','+str(pg))
        f.close()
        if pg >= stop:
            cat_id += 1
            f = open("Docs/scan.txt", "w")  # 'r' for reading and 'w' for writing
            f.write(str(cat_id)+','+'0')
            f.close()

            break
