import socket
import time


class ConnectGame:
    def __init__(self):
        self.tcp_socket = socket.socket()#实例化一个socket对象
        self.tcp_socket.bind(("", 446))#绑定IP地址和端口
        self.tcp_socket.listen()#开始监听
    
    def accept(self):
        self.connect, address = self.tcp_socket.accept()#等待客户端连接
        self.time_stamp = time.time()
        
    def recv(self):
        try:
            msg = self.connect.recv(1024).decode()
        except ConnectionResetError:
            msg = ""
        return msg
    
    def send(self, msg):
        if time.time() - self.time_stamp <= 0.1:
            time.sleep(0.1)
        self.time_stamp = time.time()
        try:
            send_len = self.connect.send(msg.encode())
        except ConnectionResetError:
            send_len = 0
        return send_len
