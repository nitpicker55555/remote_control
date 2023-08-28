import pyautogui
import pyperclip
import time
pyautogui.FAILSAFE=False

#import music_info




#def music_name():

   # return music_info.title()
#def music_tmb():
   # music_info.thumb()
def receive(data):
    if "sb" in data:
        move_mouse(data)
    else:
        print("收到命令", data)
        return control(data)
def control(command):
    if command == "music_start":
        command = "win,qq音乐##,enter,playpause"


    command_split = command.split(",")
    for ccs in command_split:
        if "click" in ccs:
            if "rightclick" in ccs:
                pyautogui.rightClick()
            else:
                pyautogui.click()
        else:
            if "##" in ccs:
                pyperclip.copy(ccs.replace("##", ""))
                ccs = "ctrl v"
            cc = ccs.split(" ")
            pyautogui.hotkey(*cc)
            if "," in command: time.sleep(1)

def move_mouse(distance_original):
    distancess = distance_original.split("sb")
    distancess.pop(-1)

    distances = distancess[0]
    distance = distances.split(",")
    x, y = pyautogui.position()

    print(distance)
    if len(distance) == 1:
        distance.append(0.0)
    try:
        x_new = x + float(distance[0])
        y_new = y + float(distance[1])
        pyautogui.moveTo(x_new, y_new)
    except ValueError:
        print("no float")
