"""
    客户端
"""

from socket import *
import sys
import getpass

HOST = '176.47.7.250'
PORT = 6678
ADDR = (HOST, PORT)

s = socket()
try:
    s.connect(ADDR)
except Exception as e:
    print(e)
    sys.exit()


def main():
    while True:
        print('''
        ==============Welcome============
        --1.注册       2.登录     3.退出--
        =================================''')
        cmd = int(input('请输入选项:'))
        if cmd == '##':
            break
        elif cmd == 1:
            do_register(s)
        elif cmd == 2:
            do_login(s)
        elif cmd == 3:
            s.send(b'E')
            sys.exit('谢谢使用')
        else:
            print('请重新输入')


def do_register(s):
    while True:
        name = input('User:')
        passwd = input('passwd:')
        # passwd = getpass.getpass()
        # passwd1 = getpass.getpass('verify:')
        if (' ' in name) or (' ' in passwd):
            print('格式错误请重新输入')
            continue
        # if passwd != passwd1:
        #     print('两次密码不一致')
        #     continue
        msg = 'R %s %s' % (name, passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'ok':
            print('注册成功')
            login(name)
        else:
            print(data)
        return


def do_login(s):
    name = input('请输入用户名:')
    passwd = input('请输入密码')
    msg = 'L %s %s' % (name, passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'ok':
        print('登录成功')
        login(name)
    else:
        print(data)


def login(name):
    while True:
        print('''
        ==============Welcome============
        --1.查单词   2.历史记录     3.注销--
        =================================''')
        cmd = int(input('请输入选项:'))
        if cmd == 1:
            do_query(name)
        elif cmd == 2:
            do_hist(name)
        elif cmd == 3:
            return
        else:
            print('请重新输入')


def do_query(name):
    while True:
        word = input('请输入单词:')
        if word == '##':
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)


def do_hist(name):
    msg = 'H %s' % name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'ok':
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print(data)


if __name__ == '__main__':
    main()
