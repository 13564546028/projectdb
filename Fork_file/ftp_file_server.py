"""
    ftp 文件服务  服务端 (基于fork多进程程网络并发)
"""
from socket import *
import os
import signal
from time import *

HOST = '127.0.0.1'
PORT = 6789
ADDR = (HOST,PORT)
FILE_PATH = '/home/tarena/1902TY/month2/PYTHONNET/Fork_file/files/'

# 服务端功能类
class Ftpserver(object):
    def __init__(self,c):
        self.c = c
    def do_list(self):
        f_list= os.listdir(FILE_PATH)
        if not f_list:
            self.c.send('文件库为空'.encode())
            return
        else:
            self.c.send(b'ok')
            sleep(0.1)
        fs = ''
        for f in f_list:
            if f[0] != '.' and os.path.isfile(FILE_PATH+f):
                fs += f +'#'
        self.c.send(fs.encode())

    def do_get(self,filename):
        try:
            fd = open(FILE_PATH+filename, 'rb')
        except IOError:
            self.c.send('该文件不存在:'.encode())
            return
        else:
            self.c.send(b'ok')
            sleep(0.1)
        while True:
            data = fd.read(1024)
            if not data:
                sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(data)
        fd.close()

    def do_put(self,filename):
        if os.path.exists(FILE_PATH+filename):
            self.c.send('该文件已存在'.encode())
            return
        f = open(FILE_PATH + filename, 'wb')
        self.c.send(b'ok')
        while True:
            data = self.c.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()


def do_requests(c):
    ftp = Ftpserver(c)
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'q':
            c.close()
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == 'G':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0] == 'P':
            filename = data.split(' ')[1]
            ftp.do_put(filename)
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('listen the port %s'%PORT)

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            continue
        print('Connect from:',addr)
        pid = os.fork()
        if pid == 0:
            s.close()
            do_requests(c)
            os._exit(0)
        else:
            c.close()

if __name__ == '__main__':
    main()











































