import sqlite3

# print("Opened database successfully")

# c.execute('''CREATE TABLE ACCOUNT
#        (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
#        USER           TEXT    NOT NULL,
#        PASSWORD       TEXT    NOT NULL,
#        RECORD         TEXT    NOT NULL);''')
# print("Table created successfully")

def tb_insert(user,pwd,rd=None):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("INSERT INTO ACCOUNT (USER,PASSWORD,RECORD) VALUES ('{}', '{}', '{}')".format(user,pwd,rd))
    conn.commit()
    conn.close()

def tb_seek():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from ACCOUNT")
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r

def tb_delete(id_):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from ACCOUNT where id = '{}'".format(id_))
    conn.commit()
    conn.close()

def tb_update(item,value):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("update from ACCOUNT where {} = '{}'".format(item,value))
    conn.commit()
    conn.close()