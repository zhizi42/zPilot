import socket
import json

class ConnectGame:
    def __init__(self):
        self.tcp_socket = socket.socket()#实例化一个socket对象
        self.tcp_socket.bind(("", 446))#绑定IP地址和端口
        self.tcp_socket.listen()#开始监听
        self.is_connect = False
    
    def accept(self):
        self.connect, address = self.tcp_socket.accept()#等待客户端连接
        self.is_connect = True
        
    def recv(self):
        try:
            msg = self.connect.recv(1024).decode()
            msg = json.loads(msg)
        except ConnectionResetError:
            msg = {}
            self.is_connect = False
        return msg
    
    def send(self, msg):
        if self.is_connect:
            try:
                msg = json.dumps(msg).encode()
                l = "{:0>4d}".format(len(msg)).encode()
                msg = l + msg
                send_len = self.connect.sendall(msg)
            except ConnectionResetError:
                send_len = 0
                self.is_connect = False
        else:
            send_len = 0
        return send_len