#SQLデータベースの顧客EmailリストからそれぞれのAnalyticsタグを入力しHTMLを自動送信
# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime
import random
import time
from time import sleep
import pymysql.cursors

list_a =[]
def time_now():
    time = datetime.now()
    return time

time_n = str(time_now())

f = open("Docs/emailer.txt", "r")   # 'r' for reading and 'w' for writing
con_id = f.read()
f.close()

today = time_n.split(' ')[0]
s_id = int(con_id)

try:
    f = open("Docs/" + today + ".txt", "r")  # 'r' for reading and 'w' for writing
    snt = f.read().split(' ')[0]
    f.close()
    sending_counter = int(snt)

except FileNotFoundError:
    pass
    f = open("Docs/" + today + ".txt", "w+")  # 'r' for reading and 'w' for writing
    f.write('0 sent')
    f.close()
    sending_counter = 0

stop = 2000
skipping_counter = 0

#find previous sent row
def find():
    while True:
        # localconnection
        # connection = pymysql.connect(host='127.0.0.1',port=8889, database='bloomdb',user='bloom',password='password_here')
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb',user='bloom',password='password_here')
        cursor = connection.cursor()
        sql = "SELECT `id`, `company`,`pic`,`email`,`sent` FROM `email_shashin` WHERE `id`=%s"
        try:
            cursor.execute(sql, (str(s_id),))
            result = cursor.fetchone()
            print(result)
            sqlinfo = str(result)
            print(sqlinfo.split(',')[0].replace('(','') + sqlinfo.split(',')[4].replace(')',''))
            status = sqlinfo.split(',')[4].replace(')','').replace(("'",''))
            print(status)
            s_id +=1
        except TypeError:
            print('continue row = ' + str(s_id))
            cursor.execute(sql, (str(s_id),))
            result = cursor.fetchone()
            print('continuing from '+ str(result))
            break
            connection.close

while True:
    from datetime import datetime
    from time import sleep
    clock = datetime.now().strftime('%H')
    if int(clock) >= 16:
        print('Its '+str(clock)+' Oclock! emailer is sleeping....')
        sleep(1800)
        break
    elif int(clock) <= 7:
        sleep(1800)
        break
    else:
        print('Its '+str(clock)+' Oclock! emailer is working....')
    # localconnection
    # connection = pymysql.connect(host='127.0.0.1',port=8889, database='bloomdb',user='bloom',password='password_here')
    def email():
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb',user='bloom',password='password_here')
        #sql = "SELECT `id`, `company`,`pic`,`email`,`sent`,`utm_medium` FROM `email_shashin` WHERE `id`=%s"
        sql = "SELECT `email` FROM `email_shashin` WHERE `id`=%s"
        cursor = connection.cursor()
        cursor.execute(sql, (str(s_id)))
        try:
            result = str(cursor.fetchone()).split("'")[1]
        except IndexError:
            pass
            result = 'NONE'
        return result


    def company():
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom',
                                     password='password_here')
        # sql = "SELECT `id`, `company`,`pic`,`email`,`sent`,`utm_medium` FROM `email_shashin` WHERE `id`=%s"
        sql = "SELECT `company` FROM `email_shashin` WHERE `id`=%s"
        cursor = connection.cursor()
        cursor.execute(sql, (str(s_id)))
        result = str(cursor.fetchone()).split("'")[1]
        return result

    def source():
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom',
                                     password='password_here')
        # sql = "SELECT `id`, `company`,`pic`,`email`,`sent`,`utm_medium` FROM `email_shashin` WHERE `id`=%s"
        sql = "SELECT `utm_medium` FROM `email_shashin` WHERE `id`=%s"
        cursor = connection.cursor()
        cursor.execute(sql, (str(s_id)))
        result = str(cursor.fetchone()).split("'")[1]
        return result

    def sent():
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom',
                                     password='password_here')
        # sql = "SELECT `id`, `company`,`pic`,`email`,`sent`,`utm_medium` FROM `email_shashin` WHERE `id`=%s"
        sql = "SELECT `sent` FROM `email_shashin` WHERE `id`=%s"
        cursor = connection.cursor()
        cursor.execute(sql, (str(s_id)))
        result = str(cursor.fetchone())
        return result


    def pic():
        connection = pymysql.connect(host='127.0.0.1', database='bloomdb', user='bloom',
                                     password='password_here')
        # sql = "SELECT `id`, `company`,`pic`,`email`,`sent`,`utm_medium` FROM `email_shashin` WHERE `id`=%s"
        sql = "SELECT `pic` FROM `email_shashin` WHERE `id`=%s"
        cursor = connection.cursor()
        cursor.execute(sql, (str(s_id)))
        result = str(cursor.fetchone()).split("'")[1]
        return result

    email = email()
    if 'NONE' in str(email):
        sent = 'email invild'

    else:
        sent = sent()
        source = source()
        company =company()
        pic = pic()

    if 'None' in sent :

        print('ID: ' +str(s_id)+'//////'+email + '//////' + company + '///////'+pic + '/////'+source+'///'+sent)
        pone = time.time()
        sender = "contact@bloom-vn.net"
        to = email
        department = ''
        from_ = source
        user_id = s_id
        date = datetime.now().date()

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "画像加工サービス初回無料のご案内"
        msg['From'] = sender
        msg['To'] = to

        # Create the body of the message (a plain-text and an HTML version).
        text = ''
        ua_tag = 'https://shashinkakouyasan.net/ec/?utm_source=mail&utm_medium=eigyou_'+str(source)+'&utm_campaign='+str(user_id)+'&utm_term=mail_eigyou&utm_content=20190120_trial_notice'
        contact_tag ='https://shashinkakouyasan.net/contact/?utm_source=mail&utm_medium=eigyou_'+str(source)+'&utm_campaign='+str(user_id)+'&utm_term=mail_eigyou&utm_content=20190120_trial_notice'

        html = """<html><head><meta http-equiv="Content-Type" content="text/html charset=UTF-8" /></head>
        <body>
        <table style="border-collapse: collapse;" border="0" width="100%" cellspacing="0" cellpadding="0" bgcolor="#e0e0e0">
    <tbody>
    <tr>
    <td><center style="width: 100%;"><!-- Visually Hidden Preheader Text : BEGIN -->
    <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">画像加工業者より、失礼します。</div>
    <!-- Visually Hidden Preheader Text : END -->
    <div style="max-width: 680px;"><!-- [if (gte mso 9)|(IE)]>
        <table cellspacing="0" cellpadding="0" border="0" width="680" align="center">
        <tr>
        <td>
        <![endif]--> <!-- Email Header : BEGIN -->
    <table style="max-width: 680px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="padding: 20px 0; text-align: center;"><img src="https://shashinkakouyasan.net/unsubscribe/emailcontents/logo.png" alt="alt_text" width="200" height="40" border="0" /></td>
    </tr>
    </tbody>
    </table>
    <!-- Email Header : END --> <!-- Email Body : BEGIN -->
    <table style="max-width: 680px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff"><!-- Hero Image, Flush : BEGIN -->
    <tbody>
    <tr>
    <td class="full-width-image" align="center"><img style="width: 100%; max-width: 680px; height: auto;" src="https://shashinkakouyasan.net/unsubscribe/emailcontents/img_slide01_dis.jpg" alt="alt_text" width="680" border="0" /></td>
    </tr>
    <!-- Hero Image, Flush : END --> <!-- 1 Column Text : BEGIN -->
    <tr>
    <td>
    <div><!-- [if mso]>
                                <table border="0" cellspacing="0" cellpadding="0" align="center" width="500">
                                <tr>
                                <td align="center" valign="top" width="500">
                                <![endif]--></div>
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td style="padding: 40px; text-align: left; font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555;">"""+company+"""  """+department+"""<br />"""+pic+""" 様<br /><br />初めまして。写真加工屋さんです。<br />この度は、弊社の画像加工サービスの初回3枚<strong>無料</strong>トライアルをご案内をさせていただきたく、メールをさせていただきました。 <br /><br />弊社はベトナムのデータセンターにて、業務を行っており、日本人スタッフが常に複数常駐していますので海外アウトソーシングでも安心、お客様のコスト削減、業務効率化へ貢献出来ればと存じます。<br />詳細につきましてはリンクボタンからウェブサイトをご覧ください。<br /><br /><!-- Button : Begin -->
    <table style="margin: auto;" border="0" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 詳細を見る <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    <br /><br />ECサイトの簡単な商品画像であれば、
    <strong>切り抜き80円から</strong>
    承ります。すべて丁寧に手作業いたしますので、自動ツールとの品質の差をお確かめください。お客様のご要望にも柔軟に対応いたしますので、お気軽にご相談ください<br /><br />写真加工屋さんからのメールを受信したくない方はこのメールの一番下の<a href="https://shashinkakouyasan.net/unsubscribe/?ID="""+str(user_id)+"""&email="""+to+"""">メール配信を停止する</a>リンクからお願いします。<br />
    <table style="margin: auto;" border="0" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+contact_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 今すぐ相談 <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table><!-- Thumbnail Left, Text Right : BEGIN --></td>
    </tr>
    <tr>
    <td dir="ltr" style="padding: 10px 0;" align="center" valign="top" bgcolor="#ffffff" width="100%" height="100%"><!-- [if mso]>
                            <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                            <tr>
                            <td align="center" valign="top" width="660">
                            <![endif]-->
    <table style="max-width: 660px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="font-size: 0; padding: 10px 0;" align="center" valign="top"><!-- [if mso]>
                                        <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                                        <tr>
                                        <td align="left" valign="top" width="220">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 33.33%; min-width: 160px; vertical-align: top; width: 100%;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td dir="ltr" style="padding: 0 10px 10px 10px;"><img class="center-on-narrow" style="border: 0; width: 100%; max-width: 200px; height: auto;" src="https://www.bloom-vn.com/images/main/10.png" alt="" width="200" /></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        <td align="left" valign="top" width="440">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 66.66%; min-width: 320px; vertical-align: top;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="center-on-narrow" dir="ltr" style="font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555; padding: 10px 10px 0; text-align: left;"><strong style="color: #2e4b91;">対応窓口は日本人</strong> <br /><br />ベトナム、ホーチミンに常に日本人が複数駐在しておりますので、言葉の壁はありません。 <br /><br /><!-- Button : Begin -->
    <table class="center-on-narrow" style="float: left;" border="0" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 詳細 <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    <!-- Button : END --></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        </tr>
                                        </table>
                                        <![endif]--></td>
    </tr>
    </tbody>
    </table>
    <!-- [if mso]>
                            </td>
                            </tr>
                            </table>
                            <![endif]--></td>
    </tr>
    <!-- Thumbnail Left, Text Right : END --> <!-- Thumbnail Right, Text Left : BEGIN -->
    <tr>
    <td dir="rtl" style="padding: 10px 0;" align="center" valign="top" bgcolor="#ffffff" width="100%" height="100%"><!-- [if mso]>
                            <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                            <tr>
                            <td align="center" valign="top" width="660">
                            <![endif]-->
    <table style="max-width: 660px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="font-size: 0; padding: 10px 0;" align="center" valign="top"><!-- [if mso]>
                                        <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                                        <tr>
                                        <td align="left" valign="top" width="220">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 33.33%; min-width: 160px; vertical-align: top; width: 100%;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td dir="ltr" style="padding: 0 10px 10px 10px;"><img class="center-on-narrow" style="border: 0; width: 100%; max-width: 200px; height: auto;" src="https://www.bloom-vn.com/images/main/8.png" alt="" width="200" /></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        <td align="left" valign="top" width="440">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 66.66%; min-width: 320px; vertical-align: top;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="center-on-narrow" dir="ltr" style="font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555; padding: 10px 10px 0; text-align: left;"><strong style="color: #2e4b91;">365日営業・年中無休体制</strong> <br /><br />平日の10時～17時に受付、作業は土日も休まず対応しております。 金曜日に依頼して週明け月曜日に納品もご相談下さい。 <br /><br /><!-- Button : Begin -->
    <table class="center-on-narrow" style="float: left;" border="0" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 詳細 <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    <!-- Button : END --></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        </tr>
                                        </table>
                                        <![endif]--></td>
    </tr>
    </tbody>
    </table>
    <!-- [if mso]>
                            </td>
                            </tr>
                            </table>
                            <![endif]--></td>
    </tr>
    <!-- Thumbnail Right, Text Left : END --> <!-- Button : END --> <!-- Thumbnail Left, Text Right : BEGIN -->
    <tr>
    <td dir="ltr" style="padding: 10px 0;" align="center" valign="top" bgcolor="#ffffff" width="100%" height="100%"><!-- [if mso]>
                            <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                            <tr>
                            <td align="center" valign="top" width="660">
                            <![endif]-->
    <table style="max-width: 660px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="font-size: 0; padding: 10px 0;" align="center" valign="top"><!-- [if mso]>
                                        <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                                        <tr>
                                        <td align="left" valign="top" width="220">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 33.33%; min-width: 160px; vertical-align: top; width: 100%;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td dir="ltr" style="padding: 0 10px 10px 10px;"><img class="center-on-narrow" style="border: 0; width: 100%; max-width: 200px; height: auto;" src="https://www.bloom-vn.com/images/main/9.png" alt="" width="200" /></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        <td align="left" valign="top" width="440">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 66.66%; min-width: 320px; vertical-align: top;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="center-on-narrow" dir="ltr" style="font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555; padding: 10px 10px 0; text-align: left;"><strong style="color: #2e4b91;">お取引先は100%日本企業</strong> <br /><br />つまり安心の日本クオリティ。日本品質を常時安定して供給致します。 <br /><br /><!-- Button : Begin -->
    <table class="center-on-narrow" style="float: left;" border="0" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 詳細 <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    <!-- Button : END --></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        </tr>
                                        </table>
                                        <![endif]--></td>
    </tr>
    </tbody>
    </table>
    <!-- [if mso]>
                            </td>
                            </tr>
                            </table>
                            <![endif]--></td>
    </tr>
    <!-- Thumbnail Left, Text Right : END --> <!-- Thumbnail Right, Text Left : BEGIN -->
    <tr>
    <td dir="rtl" style="padding: 10px 0;" align="center" valign="top" bgcolor="#ffffff" width="100%" height="100%"><!-- [if mso]>
                            <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                            <tr>
                            <td align="center" valign="top" width="660">
                            <![endif]-->
    <table style="max-width: 660px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="font-size: 0; padding: 10px 0;" align="center" valign="top"><!-- [if mso]>
                                        <table border="0" cellspacing="0" cellpadding="0" align="center" width="660">
                                        <tr>
                                        <td align="left" valign="top" width="220">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 33.33%; min-width: 160px; vertical-align: top; width: 100%;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td dir="ltr" style="padding: 0 10px 10px 10px;"><img class="center-on-narrow" style="border: 0; width: 100%; max-width: 200px; height: auto;" src="https://www.bloom-vn.com/images/main/11.png" alt="" width="200" /></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        <td align="left" valign="top" width="440">
                                        <![endif]-->
    <div class="stack-column" style="display: inline-block; margin: 0 -2px; max-width: 66.66%; min-width: 320px; vertical-align: top;">
    <table border="0" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="center-on-narrow" dir="ltr" style="font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555; padding: 10px 10px 0; text-align: left;"><strong style="color: #2e4b91;">個人情報保護を含め流出対策は万全の日本基準</strong> <br />大手スタジオ様のデータ流出防止基準に沿って運用を行っています。<br /><br /><!-- Button : Begin -->
    <table class="center-on-narrow" style="float: left;" border="0" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> 詳細 <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    <!-- Button : END --></td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if mso]>
                                        </td>
                                        </tr>
                                        </table>
                                        <![endif]--></td>
    </tr>
    </tbody>
    </table>
    <!-- [if mso]>
                            </td>
                            </tr>
                            </table>
                            <![endif]--></td>
    </tr>
    <!-- Thumbnail Right, Text Left : END --> <!-- Background Image with Text : BEGIN -->
    <tr>
    <td style="text-align: center; background-position: center center !important; background-size: cover !important;" valign="middle" bgcolor="#2e4b91"><!-- [if gte mso 9]>
                            <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:680px;height:175px; background-position: center center !important;">
                            <v:fill type="tile" src="assets/Hybrid/Image_680x230.png" color="#222222" />
                            <v:textbox inset="0,0,0,0">
                            <![endif]-->
    <div><!-- [if mso]>
                                <table border="0" cellspacing="0" cellpadding="0" align="center" width="500">
                                <tr>
                                <td align="center" valign="top" width="500">
                                <![endif]-->
    <table style="max-width: 600px; margin: auto;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="text-align: left; padding: 40px 20px; font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #ffffff;" valign="middle"><center><strong>- 最近のお取引実績 -</strong></center><br /><br /><strong>ECささげ業務代行会社様</strong><br />商品写真の切り抜き、トリミング、リサイズ。 インドの写真加工会社から弊社への乗り換え。 加工品質が向上し、NG率も大幅にダウン。<br /><hr width="100%" /><br /><strong>アパレル通販会社様 </strong><br />商品画像の切り抜き、ハンガー消し、ごみ取り。 社員デザイナーが行なっていたレタッチ業務を弊社にアウトソーシング。 業務効率化、コストダウン。<hr width="100%" /><br /><strong>大手アパレル会社様</strong><br />商品写真の白抜き、リネーム。 運営ブランドがAmazonへの新規出店するのに伴い、写真加工を弊社にアウトソーシング。<hr width="100%" /><br /><strong>アパレルブランド運営会社様</strong><br />モデル写真の美肌レタッチ、商品写真の切り抜き、色調補正。 他の写真加工会社から弊社への乗り換えによりコストダウン。<hr width="100%" /><br /></td>
    </tr>
    </tbody>
    </table>
    <!-- [if (gte mso 9)|(IE)]>
                                </td>
                                </tr>
                                </table>
                                <![endif]--></div>
    <!-- [if gte mso 9]>
                            </v:textbox>
                            </v:rect>
                            <![endif]--></td>
    </tr>
    <!-- Background Image with Text : END --> <!-- Background Image with Text : BEGIN --></tbody>
    </table>
    <table style="max-width: 600px; margin: auto;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="text-align: left; padding: 40px 20px; font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555;" valign="middle"><center><strong>- 数多くの企業様に選ばれています -</strong></center><br /><br /><strong>商品撮影会社様 </strong><br />商品写真の切り抜き、トリミング、リサイズ。 撮影後の写真加工を弊社にアウトソーシング。 カメラマンが撮影に集中できるようになり、業務効率化、コストダウン。<hr width="100%" /><br /><strong>グラビアサイト運営会社様</strong><br />グラビアアイドルの美肌レタッチ、体型補正。 社員レタッチャー、アルバイトレタッチャーの人手不足を解決するため、弊社へのアウトソーシング。 業務のスピード化、コストダウン。<hr width="100%" /><br /><strong>アプリ開発会社様 </strong><br />アイドル系アプリに使用する人物写真の美肌レタッチ、切り抜き。 他の写真加工会社から弊社への乗り換えによりコストダウン。<hr width="100%" /><br /><strong>建築写真撮影会社様 </strong><br />マンション竣工写真の電線消し。 撮影後の写真加工を弊社にアウトソーシング。 品質向上、業務効率化、コストダウン。<hr width="100%" /><br />その他にも<strong>多数の実績</strong>がございます。 お気軽にお問い合わせください。 何卒よろしくお願い致します。<br /><br /><!-- Button : Begin -->
    <table style="margin: auto;" border="0" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td class="button-td" style="border-radius: 3px; background: #2e4b91; text-align: center;"><a href="""+ua_tag+""" a class="button-a" style="background: #2e4b91; border: 15px solid #2e4b91; padding: 0 10px; color: #ffffff; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;"> <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> ウェブサイト <!-- [if mso]>&nbsp;&nbsp;&nbsp;&nbsp;<![endif]--> </a></td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
    </table>
    <!-- [if (gte mso 9)|(IE)]>
                                </td>
                                </tr>
                                </table>
                                <![endif]--> <!-- [if gte mso 9]>
                            </v:textbox>
                            </v:rect>
                            <![endif]--></td>
    </tr>
    <!-- Background Image with Text : END --></tbody></table>
        <!-- Email Body : END --> <!-- Email Footer : BEGIN --> <br />
    <table style="max-width: 680px;" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="padding: 0px 0px; width: 100%; font-size: 12px; font-family: sans-serif; mso-height-rule: exactly; line-height: 18px; text-align: center; color: #888888;">株式会社ブルーム 本社<br /><span class="mobile-link--footer">〒370-2462 群馬県富岡市下丹生24-3</span> <br />データセンター - ホーチミン<br />Quang Trung Software City, Tan Chanh Hiep Ward, District 12, Ho Chi Minh City, Vietnam<br><br><strong><a href="https://shashinkakouyasan.net/unsubscribe/?ID="""+str(user_id)+"""&email="""+to+"""">メール配信を停止する</a></strong><br><br></td>
    </tr>
    </tbody>
    </table>
    <!-- Email Footer : END --> <!-- [if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->

    </div>
    </center></td>
    </tr>
    </tbody>
    </table>
        </body>
        <img src="https://www.google-analytics.com/collect?v=1&t=event&tid=UA-128489516-1&cid=724649eb-7f23-4eef-a0e1-d1b773f43461&ea=open&ec=email&el=20190120_trial_notice"/>
    </html>"""

        try:
            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            # Send the message via local SMTP server.
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()

            mail.starttls()
            #visit https://www.google.com/settings/security/lesssecureapps to enable access from less secure apps
            mail.login(sender, 'password_here')
            mail.sendmail(sender, to, msg.as_string())
            mail.quit()
            # localconnection
            # connection = pymysql.connect(host='127.0.0.1',port=8889, database='bloomdb',user='bloom',password='password_here')
            connection = pymysql.connect(host='127.0.0.1', database='bloomdb',user='bloom',password='password_here')
            with connection.cursor() as cursor:
                # Create a new record
                sql = 'update email_shashin set sent = %s where id =%s;'
                cursor.execute(sql,(time_now(),str(s_id)))
            connection.commit()
            connection.close()

            print(str(sending_counter)+'/'+str(stop)+' 件' +to + " " + company+' 送信完了')
            f = open("Docs/" + today + ".txt", "w+")  # 'r' for reading and 'w' for writing
            f.write(str(sending_counter)+' sent')
            f.close()

            f = open("Docs/emailer.txt", "w+")  # 'r' for reading and 'w' for writing
            f.write(str(s_id))
            f.close()

            time.sleep(random.randint(3, 6))
            pend = time.time()
            print(str(pend-pone)+'秒')
            s_id +=1
            sending_counter +=1
        except smtplib.SMTPDataError:
            pass
            print('daily limit reached, emailer sleeping...........')
            sleep(3600)

    else:
        pass
        print('skipping.....')
        print(str(email)+' has sent at '+str(sent))
        skipping_counter +=1
        s_id +=1
