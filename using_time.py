import pygetwindow as gw
import time
import json
import signal
import sys
import subprocess
import requests


# 定义信号处理函数
def signal_handler(sig, frame):
    print('收到关闭信号，准备退出...')
    result = subprocess.run(['git', 'add','windows_record.jsonl'], capture_output=True, text=True)
    print("Exit code:", result.returncode)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    result = subprocess.run(['git', 'commit','-m',"'record jsonl'"], capture_output=True, text=True)
    print("Exit code:", result.returncode)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    # 打印执行结果
    print("Exit code:", result.returncode)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
def main():
    response = requests.get("https://ipinfo.io/")
    data = response.json()

    current_app = None
    while True:
        try:
            # 获取当前活动窗口
            active_window = gw.getActiveWindow()
            if active_window:
                active_app = active_window._hWnd
                if current_app != active_app:
                    current_app = active_app
                    with open("windows_record.jsonl", "a", encoding="utf-8") as file:
                        # file.write(f"App {active_window.title} got focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        file.write(json.dumps({active_window.title:time.strftime('%Y-%m-%d %H:%M:%S')}.update(data)))
                        file.write('\n')
                    print(f"App {active_window.title} got focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(1)
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    main()
