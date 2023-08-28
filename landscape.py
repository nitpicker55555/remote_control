import time
import re
import pyaudio
import wave
import pyautogui
from aip import AipSpeech
import pyperclip
import pyttsx3

def position():
    time.sleep(1)
    print(pyautogui.position())
def refresh(ques):
    huida=False
    for i in range(100):
        if huida!=True:
            time.sleep(2)
            pyautogui.hotkey("ctrl","a")
            pyautogui.hotkey("ctrl", "c")
            if "Regenerate" in pyperclip.paste():
                huida=True
                print("time:", i, "获得回答")
                split(ques)

    print("超时")
def split(ques):


    s = pyperclip.paste()


    index_b = s.find("Regenerate")
    index_a = s.rfind("1303385763@qq.com")#这里改成你在chatgpt的用户名
    result = s[index_a + len(str("1303385763@qq.com")):index_b]
    lines = result.splitlines()
    lines=[elem for elem in lines if elem != '']
    result="\n".join(lines)

    pyperclip.copy(result)

    print(result)
    huida(result,ques)
def refresh_ques(ques):


        pyautogui.moveTo(2374, 1147)#微信界面右下角
        pyautogui.click()
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(1817, 146, 0.5, button='left')#微信界面左上角，确保把所有信息都选中
        pyautogui.mouseUp(button='left')
        pyautogui.hotkey("ctrl", "c")
        shuru(ques)
        """
        pyautogui.moveTo(2389, 1183)
        pyautogui.doubleClick()
        pyautogui.hotkey("ctrl","c")
        #print("获得问题")
        keyy(ques)
        """

def keyy(ques):
    #print(ques)
    s = pyperclip.paste()
    hang = 0
    xinwenti = ""
    comd=[]
    laizi = ""
    if s not in ques:
        xinwenti = s
        ques.append(s)
        print("有问题：", s, time.asctime())

    if xinwenti != "":

        comd=xinwenti.split(",")
        comd.pop(-1)
        print("新问题：", comd)
        for i in comd:
            cc=i.split(" ")
            pyautogui.hotkey(*cc)
            time.sleep(1)


    time.sleep(1)
    refresh_ques(ques)


def shuru(ques):
    print(ques)
    s = pyperclip.paste()
    index_a = s.rfind("开始")#只查找”开始“以后的信息
    index_b = s.rfind("：")
    s=s[index_a+2:]
    lines= s.splitlines()

    hang=0
    xinwenti=""
    laizi=""
    for i in lines:
        if i=="955:":
        #if "爸爸:" in i or "妈妈" in i: #这里修改需要接收的问题来源

            if hang+1<len(lines) and lines[hang+1] not in ques:

                xinwenti=lines[hang+1]
                ques.append(lines[hang+1])
                laizi=lines[hang]

                print("有问题：",lines[hang],lines[hang+1])
        hang+=1
    if xinwenti!="":
        print("新问题：", xinwenti)
        huida(str(time.asctime()[3])+"来自"+laizi+"的问题已经收到，正在生成回答...")
        wenti(xinwenti,ques)
    else:
        time.sleep(3)
        refresh_ques(ques)

def wenti(text,ques):
    pyautogui.moveTo(1255, 1376)#这里是chatgpt的对话框坐标
    pyautogui.click()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.moveTo(1006, 877)#这里是chatgpt的界面，确保对话框不获得焦点，使得ctrl a全选可以选中整个页面
    pyautogui.click()
    refresh(ques)
def huida(result,ques=None):
    pyautogui.moveTo(2296, 1364)#发现新问题后，回到微信对话框的坐标，输出“问题收到”
    pyautogui.click()
    pyperclip.copy(result)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')

    if ques!=None:
        refresh_ques(ques)


ques=[]
refresh_ques(ques)
#pyautogui.moveTo(814, 1936)
#position()