#!/bin/usr/python
# -*- coding: utf-8 -*-
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

def db_conn():
    conn = MySQLdb.connect(**db_config)
    return conn
# create table
# cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

# insert data
# cur.execute("insert into student values('2','Tom','3 year 2 class','9')")

# search

def db_search():

    conn = db_conn()

    sql_str = "insert into test(teststr)values(%s)"
    values = ()
    cur = conn.cursor()
    cur.execute(sql_str, values)


# update
# cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

# delete
# cur.execute("delete from student where age='9'")

    cur.close()
    conn.commit()
    conn.close()


def db_save(r):

    conn = db_conn()

    sql_str = "insert into test(teststr)values(%s)"
    s1 = unicode('功','utf-8')
    cur = conn.cursor()
    cur.execute(sql_str, [s1.encode('utf-8')])

    # update
    # cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

    # delete
    # cur.execute("delete from student where age='9'")

    cur.close()
    conn.commit()
    conn.close()

def db_run():

    s1 = '功'
    s2 = u'功'
    s3 = s1.decode('utf-8')
    s4 = s2.encode('utf-8')

    print repr(s3), repr(s4)
    print len(s3), len(s4)
    print type(s3), type(s4)

    db_save(s2)


def main(argv):
    db_run()


if __name__ == '__main__':
    main(sys.argv)
