# -*- coding:utf-8 -*-
"""
    聊天室服务端
    Chat room server
    env: python3.5
    exc: for socket and fork
"""

from socket import *
import  os

ADDR = ('127.0.0.1',6789)
# 存储用户信息的字典
user = {}

def udp_server():
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    return s

def do_login(s,name,addr):
    if (name in user) or ('管理' in name):
        s.sendto('该用户名已存在!'.encode(),addr)
        return
    s.sendto(b'OK',addr)
    # 先通知其他人
    msg = '\n欢迎%s进入聊天室'%name
    for i in user:  # 遍历用户字典中所有用户
        s.sendto(msg.encode(),user[i])
    # 把用户信息加入字典
    user[name] = addr

def do_chat(s,name,text):
    msg = '\n%s : %s'%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,name):
    msg = '\n%s 退出了聊天室'%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    del user[name]

def request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msglist = data.decode().split(' ')
        # 区分请求类型
        if msglist[0] == 'L':
            do_login(s,msglist[1],addr)
        elif msglist[0] == 'C':
            # 重组消息
            text = ' '.join(msglist[2:])
            do_chat(s,msglist[1],text)
        elif msglist[0] == 'Q':
            do_quit(s,msglist[1])

def main():
    s = udp_server()
    # request(s)
# 单独创建管理员
    pid = os.fork()
    if pid < 0:
        print('Error')

    elif pid == 0:
        while True:
            msg = input('管理消息:')
            msg = 'C 管理员消息 '+msg
            s.sendto(msg.encode(),ADDR)
    else:
        request(s)  # 接收请求

main()


































































