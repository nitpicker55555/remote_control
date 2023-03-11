#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
from PIL import ImageGrab

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

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost',8000))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        im=ImageGrab.grab()

        filepath = "C:\zpz\Figure_1.png"
        filename="Figure_1.png"
        im.save(filepath)
        asd=True
        if os.path.isfile(filepath) and asd==True:

            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            data=file_deal(filepath)
            print(len(data))
            fhead = ('{}|{}'.format(len(data), filename).encode())
            stt="string"
            print(len(stt.encode()))


            data = struct.pack("I%ds" % (len(data),), len(data), data)
            s.send(stt.encode()+data)
            #print(fhead)
            #s.send(fhead)

            #fp = open(filepath, 'rb')
            """
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
            """


        else:
            fhead = "sdasdasdawdaw".encode('utf-8')
            s.send(fhead)
        s.close()
        break

if __name__ == '__main__':
    socket_client()