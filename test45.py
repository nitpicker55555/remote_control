import pyperclip
s=pyperclip.paste()
start="start"
index_a = s.rfind(start)#只查找”开始“以后的信息
index_b = s.rfind("：")
s=s[index_a+len(start):]
chat_items= s.splitlines()

print(chat_items)
# 遍历每个条目并提取时间、日期、姓名和发言
for item in chat_items:
    if item!="":
        # 解析时间、日期、姓名和发言
        time_str, name_and_message = item.split('] ')
        time_str = time_str[1:]  # 去除时间字符串开头的 "["
        time, date = time_str.split(', ')
        name, message = name_and_message.split(': ', 1)

        if name=="Nicolai":
            print(message)