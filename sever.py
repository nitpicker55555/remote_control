import socket
import threading
import os
import time
# 创建多个socket对象，分别绑定到不同的端口
global conn1,stop_event,shut_sever_detect
reboot_command="reboot_function".encode()
stop_event=threading.Event()
def two_to_one():
    global conn1, conn2,sock2,stop_event,shut_sever_detect
    reboot=False
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock2.bind((host, port2))
    sock2.listen(5)
    print('Listening on port', port2)
    conn2, addr2 = sock2.accept()
    print('Connected by two', addr2,time.asctime())
    connections[port2] = True
    while not stop_event.is_set():
        try:
            data = conn2.recv(1024)    #没有decode所以最后转发没有encode
        except:
            data=""
            data=data.encode()
            print("conn2 read fault")
        if not data:
            connections[port2] = None
            print("disconnect sock2:coon_pre", conn2,time.asctime())
            #conn1.send(reboot_command)
            conn2.close()
            print("conn2 close")
            reboot_conn("two")
            reboot=True
            break
        else:
            try:
                data_de=data.decode()
            except:
                data_de=""
            if "shutdown_sever" in data_de:
                conn1.close()
                print("conn1 close")
                conn2.close()
                print("conn2 close")
                print("shut")

                # stop_event.is_set()
                os._exit(0)
            if "sb" not in data_de:
                print(data, port2)
            #print(connections)
            if connections[port1] != None:
                try:
                    conn1.send(data)
                except:
                    print("conn1发送失败")
    if reboot==False:
        reboot_conn("two")
    print("two is shutdown")


def one_to_two():#电脑给手机发 #第一个端口
    global conn1, conn2, sock1,stop_event,shut_sever_detect

    reboot=False
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind((host, port1))
    sock1.listen(5)
    print('Listening on port', port1)
    conn1, addr1 = sock1.accept()
    print('Connected by one', addr1,time.asctime())
    connections[port1] = True
    while not stop_event.is_set():
        try:
            data = conn1.recv(1024) #一开始就把data decode了
        except:
            data = ""
            print("conn1 read fault")
        if not data:
            connections[port1] = None
            print("disconnect sock1:coon_pre", conn1,time.asctime())
            conn1.close()
            reboot_conn("one")
            print("conn1 close")
            reboot=True
            break
        else:
            try:
                data_de = data.decode()
                if len(data_de)<40:
                    print(data_de, port1)
            except:
                data_de = ""
            if "shutdown_sever" in data_de:
                conn1.close()
                print("conn1 close")
                conn2.close()
                print("conn2 close")
                print("shut")

                # stop_event.is_set()
                os._exit(0)
            else:
                # print(connections)
                if connections[port2] != None:
                    try:
                        conn2.send(data)
                    except:
                        print("conn2发送失败")
    if reboot==False:
        reboot_conn("one")
    print("one is shutdown")

def reboot_conn(term):
    print(connections)
    if term=="one":

        t1 = threading.Thread(target=one_to_two)
        t1.start()
        print("building thread..."+term)
    else:
        t2 = threading.Thread(target=two_to_one)
        print("build thread..." + term)
        t2.start()
    print("thread estabilished...", connections)
def reboot_check():
    while True:
        start_time = time.time()
        while time.time()-start_time<7200:
                 pass
        print("2 hour and reboot")
        stop_event.is_set()


def main():

    # 创建两个套接字，分别用于监听两个端口

    # 等待连接，创建两个线程分别处理两个套接字上的连接


    t2 = threading.Thread(target=two_to_one)
    t1 = threading.Thread(target=one_to_two)
    t3 = threading.Thread(target=reboot_check)
    t1.start()
    t2.start()
    t3.start()


if __name__ == '__main__':
    port1 = 8000
    port2 = 1234
    ports = [port1, port2]
    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in ports]
    connections = {port: None for port in ports}
    host = '0.0.0.0'

    main()
