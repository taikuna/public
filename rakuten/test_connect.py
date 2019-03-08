import pymysql.cursors
s_id = 1
n_id = 306

#localconnection
#connection = pymysql.connect(host='127.0.0.1',port=8889, database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
connection = pymysql.connect(host='127.0.0.1', port=8889, database='bloomdb',user='bloom',password='yH4i8Zs9LfFLjdQ')
cursor = connection.cursor()
sql = "SELECT `id`,`time`, `URL` ,`company`,`email`,`street`,`category`,`phone`,`shop`,`page` FROM `rakuten_list` WHERE `id`=%s"
cursor.execute(sql, (str(s_id),))
result = cursor.fetchone()
print(result)
sqlinfo = str(result).replace("'",'')
connection.close()
cursor.close()

