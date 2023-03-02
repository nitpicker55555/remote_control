import socket

host = 'localhost'  # 设置服务器的IP地址或域名
port = 1234  # 设置服务器的端口号

# 创建TCP套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
client_socket.connect((host, port))
test_data="control_terminal"
client_socket.send(test_data.encode())
# 循环等待用户输入数据并发送到服务器

# 从用户输入中获取数据wi
user_input = input("输入消息：")

# 发送数据到服务器
client_socket.send(user_input.encode())

# 接收服务器的返回数据
server_data = client_socket.recv(1024).decode()

# 输出服务器返回的数据
print("收到回复：", server_data)

# 关闭套接字
client_socket.close()
