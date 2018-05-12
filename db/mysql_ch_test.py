#encoding=utf-8
import sys
import MySQLdb

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'wy123',
    'db': 'test',
    'charset': 'utf8'
}

db = MySQLdb.connect(**db_config)
cur = db.cursor()
# cur.execute('use test')
name = unicode('你好', 'utf-8')

#name = '你好'
#a = name.decode("gbk").encode("utf-8")
print type(name)
cur.execute('INSERT INTO test(teststr) VALUES(%s)', [name])
db.commit()
db.close()
