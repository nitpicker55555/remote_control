import socket

# 定义需要监听的端口
import time

ports = [8000, 9000]

# 创建多个socket对象，分别绑定到不同的端口
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in ports]
for i, sock in enumerate(socks):
    sock.bind(('localhost', ports[i]))
    sock.listen(1)

# 定义一个字典，用于存储每个端口的客户端连接对象
connections = {port: None for port in ports}

def handle_client(sock, port):
    # 处理客户端连接
    #如果connect=True则只进行connect，如果是false说明所有端口都已连接，只进行信息交互
    #问题在于conn在连接了以后就不能再次accept,所以 每次send时发现对方已经掉线，则handle函数重连，重连结束就去send接受并转发信息，send的conn由handle return传递。主函数不需要for来检查none，只由send函数来检查。由主函数for循环handle，handle调用send
    #主函数for 调用handle


        conn, addr = sock.accept()
        connections[port] = conn
        print(connections)
        print(f"Connected to client on port {port} from {addr}")
        data = conn.recv(1024)
        print(data, port)
        send(sock,port,conn)



def send(sock, port,conn):
    data = conn.recv(1024)
    if not data:
        print(f"Client on port {port} disconnected")
        conn.close()
        connections[port] = None
        handle_client(sock, port)
    # 将从一个端口接收到的数据转发到其他端口的连接中
    else:
        print(data, port)
        for other_port, other_conn in connections.items():
            print(other_port, other_conn)
            if other_port != port and other_conn != None:
                print(data)
                other_conn.send(data)
while True:
    # 循环监听多个端口的客户端连接
    print("while 循环")
    for i, port in enumerate(ports):
        if connections[port]==None:
            print(port,"正在等待连接")
        handle_client(socks[i], port)



