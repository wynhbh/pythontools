import MySQLdb

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'cuckoo',
    'passwd': 'analysis',
    'db': 'cuckoo'
}

conn = MySQLdb.connect(**db_config)

#create table
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#insert data
#cur.execute("insert into student values('2','Tom','3 year 2 class','9')")

#search
with open('md5_taskid','w') as w:
    for i,line in enumerate(open('positives_filter_20','rU')):
        md5 = line.strip().split(',')[0]
        sql_str = "select tasks.id from tasks where tasks.sample_id = (select samples.id from samples where samples.md5 = '%s')" % (md5)
        cur = conn.cursor()
        cur.execute(sql_str)
        w.write(md5+':'+' '.join([str(i[0]) for i in cur.fetchall()])+'\n')
    
# update
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")
    
#delete
#cur.execute("delete from student where age='9'")

cur.close()
conn.commit()
conn.close()