import socket

class Connect:
    def __init__(self, id, server_address, cs, rn) -> None:
        self.server_address = server_address
        self.client_id = id
        self.call_sign = cs
        self.real_name = rn
        self.init()
    
    def init(self):
        self.connect = socket.socket()
        self.connect.connect((self.server_address, 3011))
        self.send("ADDCLIENT", self.client_id, "localhost", self.call_sign, "1", "1", "1", self.real_name)
        
    def send(self, command, *args):
        msg = command + ":*:zPilot:U114514:1:" + (":".join(args))
        print("send:" + msg)
        msg = msg.encode("GBK")
        self.connect.sendall(msg)
    
    def recv(self):
        r = self.connect.recv(1024).decode("GBK")
        return r