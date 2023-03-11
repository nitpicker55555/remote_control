import time
import re
import pyaudio
import wave
import pyautogui
from aip import AipSpeech
import pyperclip
import pyttsx3
def shuchu():
    # 设置录音参数
    CHUNK = 1024  # 每次读取的音频数据大小
    FORMAT = pyaudio.paInt16  # 采样位数
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率
    RECORD_SECONDS = 10  # 录音时长
    pcmE_OUTPUT_FILENAME = "output.pcm"  # 录音文件保存路径

    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 打开音频输入流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音...")

    # 读取音频数据并写入文件
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束！")

    # 关闭音频输入流和 PyAudio 对象
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 将音频数据写入文件
    with open(pcmE_OUTPUT_FILENAME, 'wb') as f:
        for data in frames:
            f.write(data)
    recon()

def recon():


    APP_ID = "30739206"
    API_KEY = "BrSeroVA74PLIRdZVVsGG2uC"
    SECRET_KEY = "lAtnKr1t1bh6CAQsaZS6mlxtW4t3Lmgg"

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取语音文件
    with open('output.pcm', 'rb') as f:
        audio_data = f.read()

    # 调用语音识别 API
    result = client.asr(audio_data, 'pcm', 16000, {
        'dev_pid': 1537,
    })

    # 打印识别结果
    print(result)
    print(result['result'][0])
    contr(result['result'][0])


def contr(text):

    pyautogui.moveTo(1414,1957)
    pyautogui.click()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('enter')

    time.sleep(15)
    pyautogui.moveTo(983, 1492)
    pyautogui.click()
    pyautogui.click()
    pyautogui.click()
    pyautogui.hotkey('ctrl','c')
    result=pyperclip.paste()

    print(result)
    fayin(result)
def fayin(text):
    engine = pyttsx3.init()

    # 设置语速和音量
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.8)

    # 将文本转化为语音

    engine.say(text)

    # 播放语音
    engine.runAndWait()
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
    index_a = s.rfind("1303385763@qq.com")
    result = s[index_a + len(str("1303385763@qq.com")):index_b]
    lines = result.splitlines()
    lines=[elem for elem in lines if elem != '']
    result="\n".join(lines)

    pyperclip.copy(result)

    print(result)
    huida(result,ques)
def refresh_ques(ques):


        pyautogui.moveTo(3274, 1697)
        pyautogui.click()
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(2429, 114, 0.5, button='left')
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
    # if "爸爸:" in i or "妈妈" in i:
    if s not in ques:
        xinwenti = s
        ques.append(s)
        print("有问题：", s, time.asctime())

    if xinwenti != "":

        comd=xinwenti.split(",")
        comd.pop(-1)
        print("新问题：", comd)
        #huida(str(time.asctime()[3]) + "来自" + laizi + "的问题已经收到，正在生成回答...")
        #wenti(xinwenti, ques)
        for i in comd:
            cc=i.split(" ")
            pyautogui.hotkey(*cc)
            time.sleep(1)


    time.sleep(1)
    refresh_ques(ques)


def shuru(ques):
    print(ques)
    s = pyperclip.paste()
    index_a = s.rfind("开始")
    index_b = s.rfind("：")
    s=s[index_a+2:]
    lines= s.splitlines()

    hang=0
    xinwenti=""
    laizi=""
    for i in lines:
        #if "咸蛋:" in i:
        if "爸爸:" in i or "妈妈" in i:
            if lines[hang+1] not in ques:

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
    pyautogui.moveTo(814, 1936)
    pyautogui.click()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.moveTo(983, 1492)
    pyautogui.click()
    refresh(ques)
def huida(result,ques=None):
    pyautogui.moveTo(3240, 1989)
    pyautogui.click()
    pyperclip.copy(result)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    if ques!=None:
        refresh_ques(ques)


ques=[]
refresh_ques(ques)
#position()