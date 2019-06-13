"""
    ftp 文件服务  客户端
"""

from socket import *
import os,sys
from time import *

ADDR = ('127.0.0.1', 6789)
FILE_PATH = '/home/tarena/1902TY/month2/PYTHONNET/Fork_file/files/'

class Ftpclinet(object):
    def __init__(self,s):
        self.s = s
    def do_list(self):
        self.s .send(b'L')
        data = self.s.recv(1024).decode()
        if data == 'ok':
            fs = self.s.recv(4096).decode()
            for f in fs.split('#'):
                print(f)
        else:
            print(data)

    def do_get(self,filename):
        self.s.send(('G '+filename).encode())
        data = self.s.recv(1024).decode()
        if data == 'ok':
            f = open(filename,'wb')
            while True:
                data = self.s.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print(data)

    def do_put(self,filename):
        try:
            f = open(filename, 'rb')
        except IOError:
            print('该文件不存在')
            return
        filename = filename.split('/')[-1]
        self.s.send(('P '+filename).encode())
        data = self.s.recv(128).decode()
        if data == 'ok':
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.s.send(b'##')
                    break
            self.s.send(data)
        else:
            print(data)
        f.close()



    def do_quit(self):
        self.s.send(b'q')
        self.s.close()
        sys.exit('谢谢使用')




def main():
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return
    # 创建对象调用功能函数
    ftp = Ftpclinet(s)
    while True:
        print('\n===============选择操作===============')
        print('一,list')
        print('二,get_list')
        print('三,put_list')
        print('四,quit')
        print('===============选择操作===============')

        cmd = input('请输入命令: ')
        if cmd.strip() == '1':
            ftp.do_list()
        elif cmd.strip() =='2':
            filename = input('请输入要下载的文件名:').strip()
            ftp.do_get(filename)
        elif cmd.strip() == '3':
            filename = input('请输入要上传的文件名:').strip()
            ftp.do_put(filename)
        elif cmd.strip() == '4':
            ftp.do_quit()
        else:
            print('请输入正确命令')



if __name__ == '__main__':
    main()



# cmd = input()
# s = cmd.split(' ')[1]
# print(s)

# msg = input('请输入要下载的文件名:')
# msgs = 'N %s'%msg
# filename = msgs.split(' ')[1]
# print(filename)


