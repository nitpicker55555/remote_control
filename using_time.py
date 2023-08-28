import pygetwindow as gw
import time

def main():
    current_app = None
    while True:
        try:
            # 获取当前活动窗口
            active_window = gw.getActiveWindow()
            if active_window:
                active_app = active_window._hWnd
                if current_app != active_app:
                    current_app = active_app
                    with open("windows_record.txt", "a", encoding="utf-8") as file:
                        file.write(f"App {active_window.title} got focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        file.write('\n')
                    print(f"App {active_window.title} got focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(1)
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    main()
