import threading
import time

import cv2
def camera():
    global cap,ret, frame
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
def capture():
    global cap,ret, frame
    if not cap.isOpened():
        print("无法打开相机")
        exit()

    # 读取相机图像


    # 检查图像是否读取成功
    if not ret:
        print("无法读取相机图像")
        exit()

    # 将图像保存为PNG文件
    cv2.imwrite("C:\zpz\came.png", frame)

    # 在窗口中显示图像
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
def thread():
    global camera_stop
    start_time=time.time()



    while time.time()-start_time < 5:
        if camera_stop == True:
            ret, frame = cap.read()
            cv2.imwrite("C:\zpz\came.png", frame)
            data=file_deal("C:\zpz\came.png")
            print(len(data))

            start_time = time.time()
            print("caca", start_time)
            camera_stop=False
    print("jieshu")
    cap.release()

def ind():
    global camera_stop
    while 1:
        asd=input()
        if asd=="ca":
            camera_stop=True
        if asd=="ac":
            print(t1.is_alive())
global camera_stop
camera_stop = False
camera()
t1 = threading.Thread(target=thread)
t1.start()
ind()


# 检查相机是否成功打开



# 等待按下任意键，然后关闭窗口
