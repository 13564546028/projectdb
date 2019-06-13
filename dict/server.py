"""
建表
create table user(id int auto_increment primary key,name varchar(32) not null,passwd varchar(16) not null);
create table hist(id int auto_increment primary key,name varchar(32) not null,word varchar(32) not null,time varchar(64));
create table word(id int auto_increment primary key,name varchar(32) ,mean varchar(2048) ,index(name));
"""

from pymysql import *

host = 'localhost'
user = 'root'
passwd = '123456'
dbname = 'dict'

def save_dict():
    conn = connect(host, user, passwd, dbname)
    cursor = conn.cursor()
    with open('dict.txt', 'r') as f:
        for x in f:
            x = x.split(' ')
            x1 = x[0]
            y1 = ' '.join(x[1:]).strip()
            print(x1, y1)
            sql = '''insert into word(name, mean) values('%s', '%s')''' % (x1, y1)
            cursor.execute(sql)
        conn.commit()
    print('insert ok')
    conn.close()

if __name__ == '__main__':
    save_dict()




# def query_dict(word):
#     conn = connect(host, user, passwd, dbname)
#     cursor = conn.cursor()
#     sql = '''select word.mean from word where word.name= %s''' % word
#     cursor.execute(sql)
#     result = cursor.fetchone()
#     conn.close()
#     print('%s:  %s' % (word, result))
#
#
# s = input('请输入单词')
# query_dict(s)