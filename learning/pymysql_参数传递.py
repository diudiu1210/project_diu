import pymysql
from pymysql.cursors import DictCursor

conn=pymysql.connect(host="120.78.128.25",port=3306,
                     password="123456",user="future",
                     charset="utf8",database="futureloan",cursorclass=DictCursor)

print(conn)

cursor=conn.cursor()
mobile="13327216491"
# 1、参数传递，用format  但是一般不用，因为涉及到sql注入
# 2、args= 的形式,%s是占坑符，是execute里有的， args 可以是列表和元组或者字典，但是不能是字符串
# cursor.execute("select * from member where mobile_phone={};".format(mobie))
cursor.execute("select * from member where mobile_phone=%s;",args=[mobile])

one=cursor.fetchone()
print(one)

