#-*- coding: utf-8 -*-
import sys,MySQLdb

conn=MySQLdb.connect(host="127.0.0.1",user="webdb",passwd="web123",db="web",charset="utf8")    #需要设定一下charset为utf-8
cursor=conn.cursor()    #生成连接的指针对象

#进行字符串编码转换并进行插入
a = "浦发银行"
a = a.decode("gbk").encode("utf-8")    #编码转换为utf-8
sql="insert into stocklist (stockno,stockname) values (%s,%s)"    #生成sql语句
param=('600000',a)    #生成sql语句的参数
n = cursor.execute(sql,param)    #执行sql语句
#以上操作等价于n = cursor.execute("insert into stocklist (stockno,stockname) values ('430004','"+ "浦发银行".decode("gbk").encode("utf-8") + "')")

print n
conn.commit() #提交操作结果

#进行查询操作检查刚刚执行的插入操作结果
n = cursor.execute("select * from stocklist")
for row in cursor.fetchall():
    print row[0] + row[1]
cursor.close()    #关闭指针
conn.close()    #关闭连接