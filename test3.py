import socket
import pyautogui
import threading
def execute_hotkey(data):
    if "quick" in data:
        if "down" in data:
            pyautogui.scroll(-90)
        else:
            pyautogui.scroll(90)
    else:
        pyautogui.hotkey(data)


# 在新线程中执行
def move_mouse(distance_original):
    # print(distance_original)


    # distances = distancess
    distance = distance_original.split(",")
    x, y = pyautogui.position()

    # print(distance)
    if len(distance) == 1:
        distance.append(0.0)
    try:
        x_new = x + float(distance[0])/8
        y_new = y + float(distance[1])/8
        pyautogui.moveTo(x_new, y_new)
    except ValueError:
        print("no float")

def udp_server(ip='0.0.0.0', port=8888):
    # 创建一个UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定socket到指定的地址和端口
    server_socket.bind((ip, port))
    print(f"UDP server listening on {ip}:{port}")

    try:
        while True:
            # 接收数据
            data, addr = server_socket.recvfrom(1024)  # 使用1024作为缓冲区大小
            # print(f"Received '{data.decode()}' from {addr}")
            if "," in data.decode():
                threading.Thread(target=move_mouse, args=(data.decode(),)).start()
            else:

                threading.Thread(target=execute_hotkey, args=(data.decode(),)).start()
            # pyautogui.hotkey(data.decode())

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    udp_server()
