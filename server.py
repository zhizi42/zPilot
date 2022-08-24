import json
import socket
import threading


def recv(connect):
    try:
        l = connect.recv(4).decode()
        if len(l) <= 0:
            return {}
        l = int(l)
        r = connect.recv(l).decode()
    except ConnectionResetError:
        return {}
    if len(r) <= 0:
        return {}
    print("recv", r)
    r = json.loads(r)
    return r

def send(connect, data):
    d = json.dumps(data).encode()
    l = "{:0>4d}".format(len(d)).encode()
    d = l + d
    connect.send(d)

def recv_one_msg(connect):
    global plan_dict
    for k, v in plan_dict.items():
        plan = v
        plan["cs"] = k
        plan["cmd"] = "plan"
        send(connect, plan)
    while True:
        r = recv(connect)
        print("len", len(connect_list))
        command = r.get("cmd", "")
        if command == "pd" or command == "plan":
            if command == "plan":
                plan = r.copy()
                plan.pop("cs")
                plan.pop("cmd")
                plan_dict[r["cs"]] = plan
            for i in connect_list:
                if i != connect:
                    try:
                        send(i, r)
                        print("send", r)
                    except:
                        connect_list.remove(connect)
                        return
        elif command == "":
            connect_list.remove(connect)
            return

connect_list = []
plan_dict = {}

tcp_socket = socket.socket()#实例化一个socket对象
tcp_socket.bind(("", 447))#绑定IP地址和端口
tcp_socket.listen()#开始监听
print("zPilot Server 1.0")
print("Server started.")
while True:
    connect, address = tcp_socket.accept()
    connect_list.append(connect)
    threading.Thread(target=recv_one_msg, args=(connect, )).start()