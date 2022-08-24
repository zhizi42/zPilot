import json
import os
import re
import shutil
import sys
import threading

import wx

import connect_game
import connect_server
import gui


def msg_box(title, sentence):
    wx.MessageBox(sentence, title, wx.OK)

plan_data = {}
def connect_recv_server():
    try:
        server_conn.init(settings_dict.get("addr", "zhizi42.f3322.net"))
    except ConnectionRefusedError:
        msg_box("连接失败", "服务器拒绝连接，请确定服务器在线。")
        return
    except TimeoutError:
        msg_box("连接失败", "连接服务器超时，请确定服务器在线。")
        return
    global is_connect_server
    is_connect_server = True
    while True:
        r = server_conn.recv()
        command = r.get("cmd", "")
        if command == "pd":
            if settings_dict.get("send_game", True):
                game_conn.send(r)
        elif command == "plan":
            cs = r["cs"]
            r.pop("cs")
            r.pop("cmd")
            global plan_data
            plan_data[cs] = r
            send_data = {"cmd": "model", "cs": cs, "model": r["model"]}
            game_conn.send(send_data)
        elif command == "":
            is_connect_server = False
            return

def recv_game():
    while True:
        game_conn.accept()
        for k, v in plan_data.items():
            send_data = {"cmd": "model", "cs": k, "model": v["model"]}
            game_conn.send(send_data)
        while True:
            game_data = game_conn.recv()
            if len(game_data) <= 0:
                break
            cs = settings_dict.get("cs", "")
            if cs == "":
                continue
            text_label = main_frame.get_text_state()
            text = "经度：\t{}\t\t纬度：\t{}\n高度：\t{}\t\t\t地速：\t{}"
            text = text.format(game_data["lon"], game_data["lat"], int(float(game_data["alt"])), int(float(game_data["gs"])))
            button_connect = main_frame.get_button_connect()
            if is_connect_server:
                button_connect.SetLabel("断开连接")
                text_server = "已连接服务器名称：\t{}\t\t呼号：\t{}\n".format(settings_dict.get("name", "Zhizi Flight"), cs)
                text = text_server + text
            else:
                button_connect.SetLabel("连接")
            text_label.SetLabel(text)
            if settings_dict.get("send_server", True):
                send_pilot_data = game_data
                send_pilot_data["cs"] = cs
                send_pilot_data["cmd"] = "pd"
                server_conn.send(send_pilot_data)


class Give(gui.frame_give):
    
    def show_bitmap(self):
        self.bitmap_give.SetBitmap(wx.Bitmap(RES_PATH + "/give_img.png"))


class FlightPlan(gui.frame_flight_plan):
    
    def get_values(self):
        dep_airport = self.text_ctrl_dep_airport.GetValue()
        arr_airport = self.text_ctrl_arr_airport.GetValue()
        model = self.text_ctrl_model.GetValue()
        alt = self.text_ctrl_alt.GetValue()
        dep_time = self.text_ctrl_dep_time.GetValue()
        arr_time = self.text_ctrl_arr_time.GetValue()
        fuel_time = self.text_ctrl_fuel_time.GetValue()
        d = {"dep_airport": dep_airport, "arr_airport": arr_airport, "model": model, "alt": alt, "dep_time": dep_time, "arr_time": arr_time, "fuel_time": fuel_time}
        return d
    
    def upload_plan(self, event):
        d = self.get_values()
        
        d["cmd"] = "plan"
        cs = settings_dict.get("cs")
        if cs == "":
            msg_box("呼号为空", "呼号为空，请先设置呼号！")
            return
        d["cs"] = cs
        if is_connect_server:
            server_conn.send(d)
            msg_box("上传成功", "上传飞行计划成功！")
        else:
            msg_box("上传失败", "未连接服务器，上传飞行计划失败。")
    
    def show_plan_help(self, event):
        t = """机场请填写ICAO代码。
机型可以是下列机型中的一个：
A318,A319,A320,A321,A333,A346,A359
B77L(B777-200LR),B77W(B777-300ER),B738,B748,B788
巡航高度请填写英尺
起降时间请填写24小时制当地时间，无冒号，如0900，2100
燃料续航时间请填写分钟"""
        msg_box("飞行计划帮助", t)
        
    def text_to_icao(self, text):
        return re.sub(r"[^a-zA-Z]", "", text).upper()[:4]
    
    def dep_airport_change(self, event):
        t = self.text_ctrl_dep_airport.GetValue()
        self.text_ctrl_dep_airport.ChangeValue(self.text_to_icao(t))
        self.text_ctrl_dep_airport.SetInsertionPointEnd()
    
    def arr_airport_change(self, event):
        t = self.text_ctrl_arr_airport.GetValue()
        self.text_ctrl_arr_airport.ChangeValue(self.text_to_icao(t))
        self.text_ctrl_arr_airport.SetInsertionPointEnd()
    
    def model_change(self, event):
        t = self.text_ctrl_model.GetValue()
        t = re.sub(r"[^a-zA-Z0-9]", "", t).upper()[:4]
        self.text_ctrl_model.ChangeValue(t)
        self.text_ctrl_model.SetInsertionPointEnd()
    
    def alt_change(self, event):
        t = self.text_ctrl_alt.GetValue()
        t = re.sub(r"[^\d]", "", t)[:5]
        self.text_ctrl_alt.ChangeValue(t)
        self.text_ctrl_alt.SetInsertionPointEnd()
    
    def dep_time_change(self, event):
        t = self.text_ctrl_dep_time.GetValue()
        t = re.sub(r"[^\d]", "", t)[:4]
        self.text_ctrl_dep_time.ChangeValue(t)
        self.text_ctrl_dep_time.SetInsertionPointEnd()
    
    def arr_time_change(self, event):
        t = self.text_ctrl_arr_time.GetValue()
        t = re.sub(r"[^\d]", "", t)[:4]
        self.text_ctrl_arr_time.ChangeValue(t)
        self.text_ctrl_arr_time.SetInsertionPointEnd()
    
    def fuel_time_change(self, event):
        t = self.text_ctrl_fuel_time.GetValue()
        t = re.sub(r"[^\d]", "", t)[:3]
        self.text_ctrl_fuel_time.ChangeValue(t)
        self.text_ctrl_fuel_time.SetInsertionPointEnd()


class Settings(gui.frame_settings):
    
    def set_value(self):
        self.text_ctrl_name.SetValue(settings_dict.get("name", "Zhizi Flight"))
        self.text_ctrl_addr.SetValue(settings_dict.get("addr", "zhizi42.f3322.net"))
        self.text_ctrl_callsign.SetValue(settings_dict.get("cs", ""))
        self.check_box_send_server.SetValue(settings_dict.get("send_server", True))
        self.check_box_send_game.SetValue(settings_dict.get("send_game", True))
    
    def get_settings(self):
        name = self.text_ctrl_name.GetValue()
        addr = self.text_ctrl_addr.GetValue()
        call_sign = self.text_ctrl_callsign.GetValue()
        send_server = self.check_box_send_server.GetValue()
        send_game = self.check_box_send_game.GetValue()
        d = {"name": name, "addr": addr, "cs": call_sign, "send_server": send_server, "send_game": send_game}
        return d
    
    def save_settings(self, event):
        global settings_dict
        settings_dict = self.get_settings()
        if not os.access(DATA_PATH, os.F_OK):
            os.makedirs(DATA_PATH)
        with open(DATA_PATH + "data.json", "w") as f:
            f.write(json.dumps(settings_dict))
        
    
    def on_close(self, event):
        global settings_dict
        settings_dict = self.get_settings()
        event.Skip()
    
    def show_about(self, event):
        msg_box("关于", "zPilot alpha\n特别感谢7502\ncode by AI丿质子")
    
    def show_give(self, event):
        give_app = wx.App()
        give_frame = Give(None)
        give_frame.show_bitmap()
        give_frame.Show()
        give_app.MainLoop()
        sys.exit()
    
    def join_group(self, event):
        os.system('start "" "https://jq.qq.com/?_wv=1027&k=2C21A82V"')
    
    def install_plugin(self, event):
        game_path = self.dir_picker_game.GetPath().replace("\\", "/")
        try:
            if os.path.exists(game_path + "/Resources/plugins/zConnect"):
                shutil.rmtree(game_path + "/Resources/plugins/zConnect")
            shutil.copytree(RES_PATH + "/zConnect", game_path + "/Resources/plugins/zConnect")
        except:
            msg_box("安装失败", "安装X-Plane插件失败，请检查目录是否正确")
        else:
            msg_box("安装成功", "安装X-Plane插件成功")


class Main(gui.frame_main):
    
    def start_connect(self, event):
        if is_connect_server:
            server_conn.close()
            self.button_connect.SetLabel("连接")
        else:
            threading.Thread(target=connect_recv_server, daemon=True).start()
    
    def show_settings(self, event):
        settings_app = wx.App()
        settings_frame = Settings(None)
        settings_frame.set_value()
        settings_frame.Show()
        settings_app.MainLoop()
        sys.exit()
    
    def get_text_state(self):
        return self.text_state
    
    def show_doc(self, event):
        doc = """使用说明：
第一次使用请先在设置界面选择X-Plane路径安装插件
并填写服务器地址和你的呼号
进入游戏后插件会自动连接应用
应用主界面会显示飞机的信息
主界面可以点连接按钮连接服务器
成功连接服务器后主界面也会显示连接的服务器名字"""
        msg_box("使用说明", doc)
    
    def get_button_connect(self):
        return self.button_connect
    
    def show_flight_plan(self, event):
        plan_app = wx.App()
        plan_frame = FlightPlan(None)
        plan_frame.Show()
        plan_app.MainLoop()
        sys.exit()

DATA_PATH = os.path.expanduser("~/AppData/Local/zPilot/").replace("\\", "/")
try:
    RES_PATH = sys._MEIPASS.replace("\\", "/")
except:
    RES_PATH = os.path.split(sys.argv[0])[0].replace("\\", "/")

settings_dict = {}
json_data_path = DATA_PATH + "data.json"
if os.path.exists(json_data_path):
    with open(json_data_path, "r") as f:
        settings_dict = json.loads(f.read())

game_conn = connect_game.ConnectGame()
server_conn = connect_server.Connect()
is_connect_server = False
threading.Thread(target=recv_game, daemon=True).start()

main_app = wx.App()
main_frame = Main(None)
main_frame.Show()
main_app.MainLoop()