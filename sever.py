import socket
import threading
import os

# 创建多个socket对象，分别绑定到不同的端口
port1 = 8000
port2 = 1234
stop_event = threading.Event()
reboot_command="reboot_function".encode()
def shut_server(stop_event,conn1):
    while True:
        try:
              data1 = conn1.recv(1024).decode()

              data= str(data1)
        except:
            data=None
        if "shutdown_server" in data:
            print("shut")
            os. _exit(0)

def two_to_one(stop_event,conn1, conn2):
    connections[port2] = True
    print("conn2_in function")
    reboot=False
    while not stop_event.is_set():
        try:
            data = conn2.recv(1024)    #没有decode所以最后转发没有encode
        except:
            data=""
            data=data.encode()
            print("conn2 read fault")
        if not data:
            connections[port1] = None
            connections[port2] = None
            #print("disconnect sock2:coon_pre", conn2)
            conn1.send(reboot_command)
            reboot_conn()
            reboot=True
            break
        else:
            print(data, port2)
            #print(connections)
            if connections[port1] != None:
                    conn1.send(data)
    if reboot==False:
        reboot_conn()
    print("two is shutdown")


def one_to_two(stop_event,conn1, conn2):#电脑给手机发
    connections[port1] = True
    print("conn1_in function")
    reboot=False
    while not stop_event.is_set():
        try:
            data = conn1.recv(1024).decode()  #一开始就把data decode了
        except:
            data = ""
            print("conn1 read fault")
        if not data:
            connections[port1] = None
            connections[port2] = None
            #print("disconnect sock1:coon_pre", conn1)
            reboot_conn()
            reboot=True
            break
        else:
            print(data, port1)
            #print(connections)
            if data=="shutdown_server":
                stop_event.set()
            if connections[port2] != None:
                    conn2.send(data.encode())
    if reboot==False:
        reboot_conn()
    print("one is shutdown")

def reboot_conn():
    global sock1, sock2
    stop_event.set()
    print(threading.active_count())

    conn1, addr = sock1.accept()
    print('Connected by1 client1', addr)
    print("conn1", conn1)
    conn2, addr = sock2.accept()
    print('Connected by client2', addr)
    print("conn2", conn2)
    stop_event.clear()
    t3 = threading.Thread(target=shut_server, args=(stop_event, conn1))
    t2 = threading.Thread(target=two_to_one, args=(stop_event,conn1, conn2))
    t1 = threading.Thread(target=one_to_two, args=(stop_event,conn1, conn2))

    print("building thread...", connections)
    t1.start()
    t2.start()
    t3.start()
    print("build thread")
    t1.join()
    t2.join()


def main():
    global sock1, sock2
    # 创建两个套接字，分别用于监听两个端口
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.bind((host, port1))
    sock1.listen(5)
    print('Listening on port', port1)

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.bind((host, port2))
    sock2.listen(5)
    print('Listening on port', port2)

    # 等待连接，创建两个线程分别处理两个套接字上的连接
    conn1, addr1 = sock1.accept()
    t3 = threading.Thread(target=shut_server, args=(stop_event, conn1))
    t3.start()
    print('Connected by', addr1)

    conn2, addr2 = sock2.accept()
    print('Connected by', addr2)

    print(connections)

    t2 = threading.Thread(target=two_to_one, args=(stop_event,conn1, conn2))
    t1 = threading.Thread(target=one_to_two, args=(stop_event,conn1, conn2))
    t1.start()
    t2.start()


if __name__ == '__main__':
    ports = [8000, 1234]
    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in ports]
    connections = {port: None for port in ports}
    host = '0.0.0.0'
    port1 = 8000
    port2 = 1234
    main()
