import re
import socket
import struct
import threading

import cv2
import pyautogui
import pyperclip

import control_local
from PIL import ImageGrab
import os
import pygetwindow as gw

import music_info

"""
cd C:\\Users\\Morning\\.ssh
ssh -i ssh-key-2023-02-27.key opc@130.61.253.72
cd /home/opc/communication/
nohup python -u listen.py > out.log 2>&1 &
netstat -luntp
shutdown_sever
"""
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
host = get_lan_ip() # 设置服务器的IP地址或域名
#host="localhost"
port = 8000  # 设置服务器的端口号
RECONNECT_INTERVAL=3
# 创建TCP套接字对象
import time
stop_event = threading.Event()
def connect_to_server():
    # 创建一个套接字并连接服务器win 1enter
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("尝试连接")
        s.connect((host, port))
        print('Connected to server.')
        user_input = "computer"
        #s.send(user_input.encode())
    except ConnectionRefusedError:
        print('Connection refused, will retry in {} seconds.'.format(RECONNECT_INTERVAL))
        return None
# 定义接收服务器反馈的线程函数
def file_deal(file_path):    #读取文件的方法
    mes = b''
    try:
        file = open(file_path,'rb')
        mes = file.read()
    except:
        print('error{}'.format(file_path))
    else:
        file.close()
        return mes
def send_machine(data):
    data=data.encode()
    length=len(data)
    print(len(data))
    data = struct.pack("I%ds" % (len(data),), len(data), data)

    # stt = filepath.split(".")[0].split("\\")[-1] + "#"
    stt = "wenz"
    print(stt)

    s.send(stt.encode() + data)
def music_foru():
    global stand
    stand="no"
    #title_ori = control_local.music_name()
    #if title_ori!="":
        #stand = "music"
        #music_info.thumb()
        #image_process("tmbb.png","♫ :) "+title_ori)
        #send_machine(("♫ :) "+title_ori))
    while True:
        #title = control_local.music_name()
        #time.sleep(1)
        #title2 = control_local.music_name()
        title2=""
        title=""
        if (title2!=title and title2!=""): #切歌
            stand="music"
            try:
                music_info.thumb()
                image_process("tmbb.png","♫ :) "+title2)
                print(title2)
            except:
                print("thumb 失败")
            #send_machine(("♫ :) "+title2))
        else:
            if title2=="" or title2==None:
                stand="not music"

    #print("music stand is over")
def receive_thread(stop_event):
    global stand
    global camera_cap
    global s
    t4 = threading.Thread(target=camera_thread)

    while not stop_event.is_set():
        if s is None:
            print("连接断开，尝试重连")
            time.sleep(RECONNECT_INTERVAL)
            s = connect_to_server()
            continue
        #print("连接正常")9417941
        # 接收服务器的响应
        try:
            data = s.recv(1024).decode()
        except:
            s.close()
            s = None
            continue

        if not data:
            # 连接断开，尝试重连
            s.close()
            s = None
            continue


        if "reboot_function" in data : s=None
        if "capture_image" in data:
            image_process("Bgdd.png")

        if "capture_camera" in data:

            if t4.is_alive()!=True:
                t4 = threading.Thread(target=camera_thread)
                print("camera_thread open"+str(t4.is_alive()))
                camera_cap = True

                t4.start()


            else:
                camera_cap=True

        else:
            control_local.receive(data)
            #print(user_input)
            if (stand !="music"):
                if "get_clip" in data:
                    active_window = gw.getActiveWindow()
                    try:
                        pre_clip=pyperclip.paste()
                    except:
                        pre_clip=""
                        print("pyperclip拒绝访问")
                    pyautogui.hotkey("ctrl", "c")

                    if "Google Chrome" in active_window.title and pre_clip==pyperclip.paste():
                        pyautogui.hotkey("ctrl","l")
                    pyautogui.hotkey("ctrl", "c")
                    s.send(pyperclip.paste().encode())
                    print(pyperclip.paste())
                elif "shut_computer" in data:
                    user_input = "get it " + data
                    s.send(user_input.encode())
                    os.system("shutdown /s /t 1")
                    # pass
                else:
                    user_input="get it "+data
                    s.send(user_input.encode())
                    print(user_input)
def camera_thread():
    global camera_cap,cap

    start_time=time.time()
    camera()
    while time.time()-start_time<10:
        if camera_cap==True:
            start_time = time.time()
            camera_capture()
            print("capture_camera", time.time()-start_time)
            camera_cap = False
    cap.release()

    print("jieshu")



def camera_capture():
    global cap, ret, frame
    ret, frame = cap.read()
    cv2.imwrite("C:\zpz\came.png", frame)
    image_process("came.png")
def camera():
    global cap,ret, frame
    # 打开默认相机
    cap = cv2.VideoCapture(0)

    # 检查相机是否成功打开
    if not cap.isOpened():
        print("无法打开相机")
        exit()

    # 读取相机图像
    ret, frame = cap.read()

    # 检查图像是否读取成功
    if not ret:
        print("无法读取相机图像")
        exit()

    # 将图像保存为PNG文件


    # 在窗口中显示图像
    #cv2.imshow("Camera Capture", frame)

    # 等待按下任意键，然后关闭窗口

def image_upload(filepath):
    if os.path.isfile(filepath):
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        data = file_deal(filepath)
        print(len(data))
        data = struct.pack("I%ds" % (len(data),), len(data), data)

        stt = filepath.split(".")[0].split("\\")[-1]
        #stt="tmbb"
        print(stt)

        s.send(stt.encode() + data)
        print("发送完成"+filepath)
    else:
        print("不存在"+filepath)
def image_process(filename,title=None):
    print("start image sending")
    filepath_path="C:\zpz\\"
    filepath = filepath_path+filename
    if "Bgd" in filename:
        im = ImageGrab.grab()
        im.save("C:\zpz\Bgdd.png")
        image_upload(filepath)
    if "came" in filename:
        image_upload(filepath)
    elif "tmb" in filename:
        data = file_deal(filepath)
        print(len(data))
        data = struct.pack("I%ds" % (len(data),), len(data), data)

        # stt = filepath.split(".")[0].split("\\")[-1] + "#"
        stt = "tmbb"


        s.send(stt.encode() + data+title.encode())


    
    




def input_info(stop_event):
    while not stop_event.is_set():
        user_input=input("input:")
        print("发送成功")
        send_machine(user_input)
def main_loop():
    # 进入主循环
    connect_to_server()
    t1 = threading.Thread(target=input_info, args=(stop_event,))
    t1.start()
    t2 = threading.Thread(target=receive_thread, args=(stop_event,))
    t2.start()
    t3 = threading.Thread(target=music_foru)
    t3.start()




        # 创建接收用户输入的线程


        # 处理服务器的响应
        #print('Received:', data.decode())
    # 关闭套接字

# 等待两个线程结束
main_loop()



