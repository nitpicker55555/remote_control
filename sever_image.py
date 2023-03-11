#!/usr/bin/env python
# -*- coding=utf-8 -*-
import socket
import threading
import time
import sys
import os
import struct

def socket_service():
    try:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', 8000))#这里换上自己的ip和端口
        s.listen(10)
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost',1234))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print ("Waiting...")

    #conn, addr = s.accept()
    conn=s
    addr="123"
    t = threading.Thread(target=deal_data, args=(conn, addr))
    t.start()

def deal_data(conn, addr):
    #print ('Accept new connection from {0}'.format(addr))

    fileinfo_size = struct.calcsize('128sl')

    #print(buf)
    #print(buf.decode())

    filesize_int = struct.calcsize("I")


    buf_int = conn.recv(filesize_int+6)
    print(buf_int[:6])
    print(int.from_bytes(buf_int[6:10], byteorder='little'))

    print("filesize_int",filesize_int)
    (filesize,), data = struct.unpack("I", buf_int[:filesize_int]), buf_int[filesize_int:]
    print("filesize",filesize)
    print("data", data)
    print(len(data))
    #if filesize>100:

    #filesize_str, filename = buf.decode().split('|')


    new_filename = os.path.join(('./'), ('new.png'))  #图片名字
    print ('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

    recvd_size = 0  # 定义已接收文件的大小
    fp = open(new_filename, 'wb')
    print ("start receiving...")
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            #print(recvd_size)
            data = conn.recv(1024)
            recvd_size += len(data)
        else:
            data = conn.recv(filesize - recvd_size)
            recvd_size = filesize
        fp.write(data)
    fp.close()
    print ("end receive...")
    #else:
    #    print(buf)

    conn.close()
    #break


if __name__ == '__main__':
    socket_service()