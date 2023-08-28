import socket
import os
from win11toast import toast
# 创建一个 TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到指定的 IP 地址和端口
ip_address = "0.0.0.0"  # 使用合适的 IP 地址
port = 12345  # 使用合适的端口号
server_socket.bind((ip_address, port))

# 监听连接
server_socket.listen(1)

print("等待客户端连接...")

# 接受客户端连接
client_socket, client_address = server_socket.accept()

print("与客户端连接建立：", client_address)

# 接收数据
data = b''  # 初始化数据为空字节串

# 指定保存图片的文件名和路径
save_path = "save/image.jpg"

while True:
    chunk = client_socket.recv(1024)  # 持续接收数据
    if not chunk:
        break
    data += chunk

# 保存接收到的数据为图片文件
with open(save_path, "wb") as file:
    file.write(data)

print("图片保存成功：", save_path)

# 关闭连接
client_socket.close()
server_socket.close()
