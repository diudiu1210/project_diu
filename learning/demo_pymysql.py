import pymysql
from pymysql.cursors import DictCursor

"""
数据库操作：
1、建立数据库连接：conn=pymysql.connect(host....)
2、建立游标,所有的操作都是建立在游标对象上 cursor=conn.cursor()
3、执行execute  sql语句： cursor.execute("select...;")
4、获取游标结果： cursor.fetone()  cursor.fetall()
5、关闭游标，关闭连接： cursor.close()    conn.close()

在初始化的时候，使用cursorclass=DictCursor，让本来all里打印出来的类型是元组，能让元组转化为字典，可读性强，
如果打印的数据有多条，就是把多个字典放一起用列表的方式打印出来
注意charset="utf8"  不能写成“utf-8"
"""
# 建立连接
conn=pymysql.connect(host="120.78.128.25",port=3306,
                     password="123456",user="future",
                     charset="utf8",database="futureloan",cursorclass=DictCursor)

print(conn)
# 建立游标，发起请求，游标对象，相当于光标，共用一个游标进行多次数据查询
cursor=conn.cursor()
# 执行sql语句
cursor.execute("select * from member limit 2;")
# 获取游标结果
one=cursor.fetchone()

# 如果同时执行one和all的话，one打印第一条信息，all只会打印第二条信息，而第一条不会打印，因为游标在第一条的后面
# 如果需要打印one 同时又不影响打印all所有，就需要在one后面再重新新建一次游标,然后执行execute，在获取all的结果
cursor_1=conn.cursor()
cursor_1.execute("select * from member limit 3")
all=cursor_1.fetchall()

print(one)
print(all)
# 最后关闭游标，关闭连接
cursor.close()
cursor_1.close()
conn.close()
