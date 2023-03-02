import socket

# 创建 TCP/IP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到端口
server_address = ('0.0.0.0', 1234)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# 监听来自客户端的连接
sock.listen(2)

while True:
    # 等待连接
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)

        # 接收数据
        data = connection.recv(1024)


        print('Received {!r}'.format(data))

        # 发送数据
        if str("LAPTOP-AN4QTF3N") in str(data):
           connection.sendall(bytes("get it"))

    finally:
        # 清理连接
        connection.close()
