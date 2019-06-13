"""
    httpserver 3.0 主程序文件
"""

from socket import *
import sys
from threading import Thread
from config import *
import re
import json

ADDR = (HOST, PORT)


# 和frame通信
def connect_frame(env):
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
    try:
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return
    data = json.dumps(env)
    s.send(data.encode())

    # 接收webframe数据
    data = s.recv(4096 * 10).decode()
    # 返回数据字典
    return json.loads(data)


#  封装httpserver 基本功能:

class HTTPServer(object):
    def __init__(self, address):
        self.address = address
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        self.s.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    # 启动服务器
    def serve_forever(self):
        self.s.listen(5)
        print('listen the port %d....' % self.port)
        while True:
            try:
                c, addr = self.s.accept()
                print('Connect from ', addr)
            except KeyboardInterrupt:
                self.s.close()
                sys.exit('服务器异常')
            except Exception as e:
                print(e)
                continue
            # 创建新线程处理请求:
            client = Thread(target=self.handle, args=(c,))
            client.setDaemon(True)
            client.start()

    def handle(self, c):
        # 接收http 请求
        request = c.recv(4096).decode()
        # print(request)
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern, request).groupdict()
        except:
            c.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.response(c, data)

    # 讲数据为response响应格式整理发送给浏览器
    def response(self, c, data):
        if data['status'] == '200':
            responseHeaders = 'HTTP/1.1 200 Ok\r\n'
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']
        elif data['status'] == '404':
            responseHeaders = 'HTTP/1.1 404 Not Found\r\n'
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']
        elif data['status'] == '500':
            responseHeaders = 'HTTP/1.1 500 Server Error\r\n'
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']

        response_data = responseHeaders + responseBody
        c.send(response_data.encode())


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.serve_forever()
