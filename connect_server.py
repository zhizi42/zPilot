import socket
import json

class Connect:
    def __init__(self) -> None:
        self.connect = socket.socket()
        self.is_connect = False
    
    def init(self, server_address):
        self.connect.connect((server_address, 447))
        self.is_connect = True
        
        
    def send(self, data):
        if self.is_connect:
            try:
                msg = json.dumps(data).encode()
                l = "{:0>4d}".format(len(msg)).encode()
                msg = l + msg
                send_len = self.connect.sendall(msg)
            except (ConnectionResetError, OSError):
                send_len = 0
                self.close()
        else:
            send_len = 0
        return send_len
    
    def recv(self):
        try:
            l = int(self.connect.recv(4).decode())
            r = self.connect.recv(l).decode()
            if len(r) <= 0:
                r = {}
                self.is_connect = False
            else:
                r = json.loads(r)
        except (ConnectionResetError, OSError):
            r = {}
            self.close()
        except json.JSONDecodeError:
            r = {}
        return r
    
    def close(self):
        try:
            self.connect.shutdown(2)
            self.connect.close()
        except:
            pass
        self.connect = socket.socket()
        self.is_connect = False