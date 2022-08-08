import json
import threading
import time

import connect_game
import connect_server


def recv_server(conn):
    while True:
        r = conn.recv()
        if len(r) <= 0:
            return
        print("recv:" + r)
        r = r.split(":")
        if r[0] == "PING":
            conn.send("PONG", r[-1])
        elif r[0] == "PD":
            if is_connect_game:
                msg = {"action":"pilot_data", "cs":r[6], "lat":r[9], "lon":r[10], "alt":r[11], "gs":r[12]}
                msg = json.dumps(msg)
                print(msg)
                game_conn.send(msg)
        #elif r[0] == "PLAN"

def recv_game():
    while True:
        game_conn.accept()
        global is_connect_game
        is_connect_game= True
        my_pilot_data = {}
        while True:
            r = game_conn.recv()
            print(r)
            if len(r) <= 0:
                is_connect_game = False
                break
            r = json.loads(r)
            precise = ["lat", "lon"]
            imprecise = ["alt", "the", "phi", "psi", "gs"]
            for i in (precise + imprecise):
                modify = False
                if i in precise:
                    if my_pilot_data.get(i, 114514) != r[i]:
                        modify = True
                        break
                elif i in imprecise:
                    if abs(float(my_pilot_data.get(i, 114514)) - float(r[i])) >= 1:
                        modify = True
                        break
            #if modify:
            my_pilot_data = r
            #server_conn.send("PD", "S", "CCA0042", "0", "1", my_pilot_data["lat"], my_pilot_data["lon"], my_pilot_data["alt"], my_pilot_data["gs"])
            

def start_connect_server():
    global server_conn
    while True:
        server_conn = connect_server.Connect(server_address = "sim.skylineflyleague.cn", id = "1", cs = "0042", rn = "zhizi42")
        recv_server(server_conn)
        #server_conn.send("PD", "0", "0042", "0", "0", "27.91", "120.85", "0", "0")

print("zPilot alpha.\nspecial thanks CCA1570.")
is_connect_game = False
game_conn = connect_game.ConnectGame()
threading.Thread(target=start_connect_server).start()
threading.Thread(target=recv_game).start()