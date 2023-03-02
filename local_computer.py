import socket
import threading
import pyautogui
import pyperclip
pyautogui.FAILSAFE=False1
host = '130.61.253.72'  # 设置服务器的IP地址或域名
#host="localhost"
port = 8000  # 设置服务器的端口号
RECONNECT_INTERVAL=3
# 创建TCP套接字对象
import time
stop_event = threading.Event()
def connect_to_server():
    # 创建一个套接字并连接服务器
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("尝试连接")
        s.connect((host, port))
        print('Connected to server.')
        user_input = "computer"
        s.send(user_input.encode())
        return s
    except ConnectionRefusedError:
        print('Connection refused, will retry in {} seconds.'.format(RECONNECT_INTERVAL))
        return None
# 定义接收服务器反馈的线程函数

def receive_thread(server_data):

    if "sb" in server_data:
        move_mouse(server_data)
    else:
        print("收到命令", server_data)
        control(server_data)
def control(command):
        if command=="music_start":
            command="win,qq音乐##,enter,playpause"

        command_split = command.split(",")
        for ccs in command_split:
            if "click" in ccs:
                if "doubleclick" in ccs:
                    pyautogui.doubleClick()
                else:
                    pyautogui.click()
            else:
                if "##" in ccs:
                    pyperclip.copy(ccs.replace("##",""))
                    ccs="ctrl v"
                cc = ccs.split(" ")
                pyautogui.hotkey(*cc)
                if "," in command:time.sleep(1)
        user_input = "get it"
        if command=="shutdown_sever":user_input = "shutdown_sever"
        s.send(user_input.encode())
        print("已发送get it")
def move_mouse(distance_original):
    distancess=distance_original.split("sb")
    distancess.pop(-1)

    distances=distancess[0]
    distance=distances.split(",")
    x,y=pyautogui.position()

    print(distance)
    if len(distance)==1:
        distance.append(0.0)
    try:
        x_new=x+float(distance[0])
        y_new=y+float(distance[1])
        pyautogui.moveTo(x_new,y_new)
    except ValueError:
        print("no float")
def input_info(stop_event):
    while not stop_event.is_set():
        user_input=input("input:")
        print("发送成功")
        s.send(user_input.encode())
def main_loop():
    # 进入主循环
    s = connect_to_server()
    t1 = threading.Thread(target=input_info, args=(stop_event,))
    t1.start()

    while True:
        if s is None:
            print("连接断开，尝试重连")
            time.sleep(RECONNECT_INTERVAL)
            s = connect_to_server()
            continue
        #print("连接正常")

        # 接收服务器的响应
        data = s.recv(1024).decode()
        if not data:
            # 连接断开，尝试重连
            s.close()
            s = None
            continue
        if "reboot_function" in data : s=None
        receive_thread(data)


        # 创建接收用户输入的线程


        # 处理服务器的响应
        #print('Received:', data.decode())
    # 关闭套接字
    s.close()
# 等待两个线程结束
main_loop()



