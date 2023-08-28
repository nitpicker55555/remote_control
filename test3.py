import sys

from PyQt5.QtWidgets import QApplication
from qframelesswindow import AcrylicWindow

import sys,os
from ctypes import cdll
from ctypes.wintypes import HWND

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPainterPath
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont,QFontMetrics
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
import pygetwindow as gw


class Window(AcrylicWindow):


    def __init__(self, text_in, title, address_pic,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PyQt-Frameless-Window")
        # self.titleBar.raise_()
        # customize acrylic effect
        # self.windowEffect.setAcrylicEffect(self.winId(), "106EBE99")

        # self.move(400,300)

        self.resize(800, 200)
        # 去除边框
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # 背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置背景色
        # self.bgColor = QColor(255, 255, 255, 60)

        # 调用api
        # hWnd = HWND(int(self.winId()))  # 不能直接HWND(self.winId()),不然会报错
        # areoDll = cdll.LoadLibrary(r'C:\anaconda\Lib\site-packages\aeroDll.dll')
        # areoDll.setBlur(hWnd)
        self.label = QLabel(self)

        pixmap = QPixmap(address_pic)  # 替换为你的 PNG 图像的路径
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 将 QPixmap 缩放为适合 QLabel 的大小

        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 将 QPixmap 缩放为适合 QLabel 的大小

        # 创建一个同样大小的 QPixmap 用于绘制圆形剪裁后的图片
        target = QPixmap(pixmap.size())
        target.fill(Qt.transparent)  # 设置背景透明

        painter = QPainter(target)
        path = QPainterPath()
        path.addEllipse(0, 0, pixmap.width(), pixmap.height())  # 创建一个椭圆形路径，如果 width() 和 height() 相同则为圆形
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)  # 绘制图片到 QPixmap
        painter.end()

        def split_text(text, line_length):
            return '\n'.join(text[i:i + line_length] for i in range(0, len(text), line_length))

        # 设置剪裁后的 QPixmap 到 QLabel
        self.label.setPixmap(target)
        self.label.move(15, 50)  # 根据需要调整位置
        title_out = title
        self.label2 = QLabel(title, self)
        self.label2.setFixedWidth(600)
        self.label2.move(150, 40)  # 根据需要调整位置

        self.label2.setFont(QFont("Microsoft YaHei", 25, QFont.Bold))  # 设置字体为微软雅黑，字号为40，字体为粗体
        self.label2.setStyleSheet("color: white;")  # 设置字体颜色为白色
        self.label2.setWordWrap(True)
        text_out = text_in
        self.label3 = QLabel(text_in, self)
        self.label3.setFont(QFont("Microsoft YaHei", 25, QFont.Thin))  # 设置字体为微软雅黑，字号为40，字体为粗体
        self.label3.setStyleSheet("color: white;")  # 设置字体颜色为白色

        self.label3.setFixedWidth(600)
        self.label3.setWordWrap(True)
        print(self.label2.sizeHint().height(), "label2")
        self.label3.move(150, 60 + (self.label2.sizeHint().height()))  # 根据需要调整位置

        # print(len(text_out.split("\n")),"text_out")
        # print(len(title_out.split("\n")),"title_out")
        # self.resize(800,100+80*len(text_out.split("\n"))+45*len(title_out.split("\n")))
        # self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        font_metrics1 = QFontMetrics(self.label2.font())
        text_height1 = self.label2.sizeHint().height()
        font_metrics3 = QFontMetrics(self.label3.font())
        text_height3 = self.label3.sizeHint().height()
        print(text_height1, text_height3)

        self.resize(800, text_height1 + text_height3 + 100)
        # # self.effect_shadow.setOffset(10,1)  # 偏移
        # # self.effect_shadow.setBlurRadius(50)  # 阴影半径
        # # #self.effect_shadow.setColor(QtCore.Qt.gray)  # 阴影颜色
        # # self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowTitle('  ')

        self.timer = QTimer(self)

        # 设置 QTimer 的超时时间并连接到相应的槽函数
        self.timer.timeout.connect(self.closeWindow)
        self.timer.start(4000)  # 5 秒后关闭窗口

    def move_to_corner(self,location):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()

        # 目标位置
        if location==100000 or location<self.height()+200:
            location_real=screen_rect.bottom() - self.height() - 100
        else:
            location_real=location-self.height()
        print(location_real,"location_real",self.height(),"self.height()")
        end_pos = QPoint(screen_rect.right() - self.width() - 300, location_real)

        # 初始位置，从屏幕右边缘外开始
        start_pos = QPoint(screen_rect.left(), screen_rect.bottom() - self.height() - 20)

        # 设置动画
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(1000)  # 动画时长1秒
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.OutQuint)  # 使用弹跳效果
        self.anim.start()

    def closeWindow(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()

        # 目标位置
        start_pos = QPoint(self.geometry().x(),self.geometry().y())

        # 初始位置，从屏幕右边缘外开始
        end_pos = QPoint(screen_rect.right(), screen_rect.bottom() - self.height() - 20)

        # 设置动画
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(500)  # 动画时长1秒
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.InQuint)  # 使用弹跳效果
        self.anim.finished.connect(self.close)
        self.anim.start()



def input_func(text, title, address_pic):
    # time.sleep(4)
    all_windows = gw.getAllWindows()
    top_int=100000
    for win in all_windows:
        # if win.isVisible:窗口标题: PyQt-Frameless-Window, 位置: 1853, 731, 宽度: 533, 高度: 154
        if "PyQt-Frameless-Window" in win.title:
                if 1.55*win.top<top_int and win.top<1700:
                    top_int=1.55*win.top

    print(top_int,"top_int")
    app = QApplication(sys.argv)
    demo = Window(text, title, address_pic)
    demo.show()
    demo.move_to_corner(top_int)
    sys.exit(app.exec_())



