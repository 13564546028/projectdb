"""
    电子词典服务端
"""

from socket import *
import time
from pymysql import *
import os, sys
import signal

if len(sys.argv) < 3:
    print('''Run server as: python3 dict_server.py 0.0.0.0 6789''')
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST, PORT)
DICT_TEXT = './dict.txt'


def main():
    db = connect('localhost', 'root', '123456', 'dict', charset='utf8')
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        pid = os.fork()
        if pid == 0:
            s.close()
            do_request(c, db)
            sys.exit()
        else:
            c.close()


def do_request(c, db):
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ':', data)
        data = data.split(' ')
        if not data or data[0] == 'E':
            c.close()
            return
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_hist(c, db, data)


def do_register(c, db, data):
    # msg = data.spilt(' ')
    name = data[1]
    passwd = data[2]
    cursor = db.cursor()
    sql = """select * from user where name ='%s'""" % name
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None:
        c.send('用户名已存在'.encode())
    else:
        sql = """insert into user (name,passwd) values('%s','%s')""" % (name, passwd)
        try:
            cursor.execute(sql)
            db.commit()
            c.send(b'ok')
        except:
            db.rollback()
            c.send('注册失败'.encode())


def do_login(c, db, data):
    # msg = data.spilt(' ')
    name = data[1]
    passwd = data[2]
    cursor = db.cursor()
    sql = """select * from user where name= '%s' and passwd = '%s' """ % (name, passwd)
    r = cursor.execute(sql)
    if r:
        c.send(b'ok')
    else:
        c.send('登录失败'.encode())


def do_query(c, db, data):
    cursor = db.cursor()
    name = data[1]
    word = data[2]
    tm = time.time()
    sql = """insert into hist (name,word,time)values('%s','%s','%s')""" % (name, word, tm)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    # 文本查询
    f = open(DICT_TEXT)
    for line in f:
        w = line.split(' ')[0]
        if w > word:
            break
        elif w == word:
            c.send(line.encode())
            f.close()
            return
    c.send('没有找到该单词'.encode())


def do_hist(c, db, data):
    name = data[1]
    cursor = db.cursor()
    sql = """select * from hist where name='%s' order by id desc limit 10""" % name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send('无查询记录'.encode())
    c.send(b'ok')
    for i in r:
        msg = "%s %s %s" % (i[1], i[2], i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    time.sleep(0.1)
    c.send(b'##')

if __name__ == '__main__':
    main()
