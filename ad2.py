import socket
import threading

host = '127.0.0.1'  # 设置服务器的IP地址或域名
port = 1234  # 设置服务器的端口号

# 创建TCP套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
client_socket.connect((host, port))

# 定义接收用户输入的线程函数
def input_thread():
    while True:
        # 从用户输入中获取数据
        user_input = input("输入消息：")

        # 发送数据到服务器
        client_socket.send(user_input.encode())

# 定义接收服务器反馈的线程函数
def receive_thread():
    while True:
        # 接收服务器的返回数据
        server_data = client_socket.recv(1024).decode()

        # 输出服务器返回的数据
        print("收到回复：", server_data)

# 创建接收用户输入的线程
input_thread = threading.Thread(target=input_thread)
input_thread.daemon = True
input_thread.start()

# 创建接收服务器反馈的线程
receive_thread = threading.Thread(target=receive_thread)
receive_thread.daemon = True
receive_thread.start()

# 等待两个线程结束
input_thread.join()
receive_thread.join()

# 关闭套接字
client_socket.close()
