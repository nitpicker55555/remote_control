:CHECK_CONNECTION
ping -n 1 www.google.com > nul
if %errorlevel% equ 0 (
    echo Network connected
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\Phone_clipboard.py
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\sever.py
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\UDP_pc.py
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\controled_computer.py
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\device_detect.py
    start /B python C:\Users\Morning\Desktop\my_project\programm_websocket\using_time.py
exit
) else (
    echo No Network :-)
    timeout /t 5 > nul
    goto CHECK_CONNECTION
)

exit
