import json
import os
import re
import socket
import time
import webbrowser
import pyautogui
import pyperclip
from PIL import Image
import threading
from win11toast import toast
import os
import multiprocessing
from PIL import Image, ImageDraw, ImageFont
import random
from toast_glass import input_func  # 导入MainWindow类
import subprocess
from gpt_api_singel import *
# import psutil
ask_prompt = """
用中文简短（几个字以内）回答我朋友的信息

她要我帮他抢Notfall termin，在早上，如果她问我醒了没有，你就说醒了，在抢
如果他问我抢到没有，你就说还没有

如果她说抢到了，你就说太牛啦
总之简短回复她，适当的时候鼓励她，一定简短
背景信息：
我们是好朋友，很熟悉，住在德国学生宿舍
她求了很多同学帮她一起抢
"""
messages=[]
messages.append(message_template('system', ask_prompt))
# 要打开的程序的路径
def open_file(path="C:\Program Files (x86)\Tencent\QQMusic\QQMusic1942.19.33.18\QQMusic.exe"):
    exe_path = path

    # 使用subprocess打开程序
    subprocess.Popen(exe_path)


# 要打开的程序的路径


def image_font(title,content):
    text=re.sub(r'[^\w\s]', '', title)
    print(text)


    # 生成随机背景色
    bgcolor = (random.randint(100, 255), random.randint(50, 120), random.randint(50, 150))

    print(bgcolor)
    # 创建一个新的300x300像素的图像，背景色为随机色
    image = Image.new('RGB', (300, 300), bgcolor)

    # 设置字体和字体大小，你可能需要更改此处的字体路径和大小
    font = ImageFont.truetype('C:\WINDOWS\FONTS\MSYHL.TTC', 200)

    # 创建一个可以在图像上绘图的对象
    draw = ImageDraw.Draw(image)

    # 文本内容


    # 使用 textbbox 方法获取文本的宽度和高度
    left, upper, right, lower = draw.textbbox((0, 0), text[0], font=font)
    textwidth = right - left
    textheight = lower - upper

    # 将文本画在图像的中心（你可能需要根据文本的长度和字体大小来调整位置）
    width, height = image.size
    x = (width - textwidth) / 2
    y = (height - textheight) / 2 - 55
    draw.text((x, y), text[0], font=font, fill=(255, 255, 255))

    # 保存图像
    image.save('save\\text_image.png')
    # return toast(title, content,
    #       icon=(os.getcwd() + "\\" + "save\\text_image.png"),app_id="屁真文本")
    p = multiprocessing.Process(target=toast_send, args=(content, title,os.getcwd() + "\\" + "save\\text_image.png"))
    p.start()
    print("dindsih")
    return "mp"

def toast_send(content, title,path):
    input_func(content, title, path)

def rec_ima():

    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定到指定的 IP 地址和端口
    ip_address = "0.0.0.0"  # 使用合适的 IP 地址
    port = 12345  # 使用合适的端口号
    server_socket2.bind((ip_address, port))

    # 监听连接
    while True:

        server_socket2.listen(1)

        print("等待客户端连接...")

        # 接受客户端连接
        client_socket, client_address = server_socket2.accept()

        print("与客户端连接建立：", client_address)

        # 接收数据
        data = b''  # 初始化数据为空字节串

        # 指定保存图片的文件名和路径
        save_path = "save\image.jpg"

        while True:
            chunk = client_socket.recv(1024)  # 持续接收数据
            if not chunk:
                break
            data += chunk

        # 保存接收到的数据为图片文件
        with open(save_path, "wb") as file:
            file.write(data)
        image = {

            'src': os.getcwd()+"\\"+save_path,
            'placement': 'hero'
        }



        if "arguments" in toast(str(round(os.path.getsize(os.getcwd()+"\\"+save_path) / (1024 * 1024),2))+" M", 'Image', image=image,app_id="屁真消息"):

            image = Image.open(save_path)
            # 显示图片
            image.show()
        print("图片保存成功：", save_path)


def heart(client_socket):
    while True:
        try:
            client_socket.send(("Received:").encode("utf-8"))
            time.sleep(2)
        except:
            return "false"
def send_mes():
    print("1231232")
    rece=input("input:")
    print(rece)
    #client_socket.send((rece).encode("utf-8"))
    print("123成功")
def auto_answer(query):


    messages.append(message_template('user', query))
    print(messages)
    result = chat_single(messages)[0]

    messages.append(message_template('assistant', result))

    print(result)
    return result
def write_answer(query):
    pyperclip.copy(query)
    pyautogui.hotkey("ctrl","v")
    pyautogui.hotkey('enter')
def start_server(ip, port):
    pre_data = ""

    clipboard_str = ""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(1)
    print("Server is listening on port", 8080)

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from", client_address)
    code_list=['验证码','code']
    while True:
            num=0
        # Receive data
            while num<5:
                try:
                    data = client_socket.recv(1024).decode("utf-8")
                    data=data.replace("\n","")




                    for content in data.split("****"):
                        if content.replace(pre_data,"")!="" and content.split("----")[1]!="null":
                            print("Received data:", content)
                            head=content.split('----')[0]
                            if head=='剪贴板':
                                inner_content=content.split('----')[1]
                                answer=auto_answer(inner_content)
                                time.sleep(1)
                                write_answer(answer)


                            if "剪贴板" in content:
                                if content==clipboard_str:
                                    print(content)
                                    content=""

                            if any(code in content for code in code_list):
                                try:
                                    pyperclip.copy(re.findall('\d+', content)[0])
                                    print(re.findall('\d+', content))
                                    pyautogui.hotkey("ctrl", "v")
                                    pyautogui.hotkey("enter")
                                except:
                                    pass
                            if "http" in content and "phone_clip_web" not in content:
                                url_pattern = r'(https?://\S+)'

                                # 使用正则表达式匹配URL
                                urls = re.findall(url_pattern, content)
                                print(urls)
                                webbrowser.open(urls[0])
                            clipboard_str=content
                            # Send data back
                            client_socket.send(("Received: " + content).encode("utf-8"))

                            if "arguments" in image_font(content.split("----")[0], content.split("----")[1]):
                                try:
                                    pyperclip.copy( content.split("----")[1])
                                except:
                                    pass

                            pre_data=content
                        else:
                            pass
                except Exception as e:

                    num+=1
                    print("重连",num,e)
                    time.sleep(1)
            pre_data = ""

            clipboard_str = ""
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip, port))
            server_socket.listen(1)
            print("Server is listening on port", port)

            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from", client_address)



if __name__ == "__main__":

    t2 = threading.Thread(target=rec_ima)
    t2.start()
    t1=threading.Thread(target=start_server("0.0.0.0", 8080))
    t1.start()

    print(123)

