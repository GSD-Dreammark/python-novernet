import MySQLdb
def update():
# MYSQLdb 链接SQL
    localhost="localhost";
    root="root";
    password="1234";
    db="novel"
    conn=MySQLdb.connect(localhost,root,password,db);
    cursor=conn.cursor();
    cursor.execute("select * from messages");
    dir=cursor.fetchall();
    for i in dir:
        print(i)