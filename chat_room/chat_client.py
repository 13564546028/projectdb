"""
    聊天室用户端
"""

from socket import *
import os, sys
import signal

ADDR = ('176.47.7.250', 8889)


def udp_client():
    return socket(AF_INET, SOCK_DGRAM)


def login(s):
    while True:
        name = input('请输入昵称:')
        # 表示请求内容
        msg = 'L ' + name
        # 发送给服务器
        s.sendto(msg.encode(), ADDR)
        # 等待回复
        data, addr = s.recvfrom(1024)
        # 判断是否能进入聊天室
        if data.decode() == 'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())
    return name


def send_msg(s, name):
    while True:
        try:
            text = input('<<')
        except KeyboardInterrupt:
            text = 'quit'
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')
        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), ADDR)


def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        # 收到服务器EXIT则退出进程  不需要认为去处理僵尸进程
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + '\n<<', end=' ')


def chat(s, name):
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    pid = os.fork()
    if pid < 0:
        sys.exit('Error')
    if pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


def main():
    s = udp_client()
    name = login(s)
    chat(s, name)


main()
