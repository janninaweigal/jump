# -*- coding: utf-8 -*-
__author__ = 'Lilyu'

import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import uuid


reload(sys)
sys.setdefaultencoding('utf8')
# cxfreeze D:\Users\Lilyu\PycharmProjects\untitled4\order\WebMain.py  --target-dir E:\order\ --base-name="win32gui"
app, browser = None, None
# adb shell screencap -p /sdcard/screen.png
# adb pull /sdcard/screen.png   D:/screen.png
# adb shell input swipe 320 410 320 410 1 349


def show_close():
    print('close')


class BrowserScreen(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.setWindowTitle(u'跳一跳')
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resize(1200, 800)
        path = os.getcwd()
        self.load(QUrl.fromLocalFile(path + "/testjs/a.html"))
        self.show()

    def closeEvent(self, event):
        global IS_CONNECTION
        IS_CONNECTION = 'END'
        show_close()

    def show_message(self, msg):
        pass


def remove_all_files():
    rootdir = 'D:\\'
    list_dir = os.listdir(rootdir)
    for i in range(0, len(list_dir)):
        png_check = list_dir[i]
        if "screen" in png_check and ".png" in png_check:
            os.remove("D:\\" + png_check)


class PythonJS(QObject):
    @pyqtSignature("QString", result="QString")
    def find_order_c_excel(self, order):
        return order

    @pyqtSignature("", result="QString")
    def find_new_img(self):
        remove_all_files()
        os.system("adb shell screencap -p /sdcard/screen.png")
        file_name = "screen" + str(uuid.uuid1()) + ".png"
        ret_path = "file:///D://" + file_name
        os.system("adb pull /sdcard/screen.png   D:/" + file_name)
        print(ret_path)
        return ret_path

    @pyqtSignature("QString", result="QString")
    def op_run(self, value):
        cmd = "adb shell input swipe 320 410 320 410 " + str(value)
        os.system(cmd)
        return cmd


def my_main():
    app = QApplication(sys.argv)
    browser = BrowserScreen()
    pjs = PythonJS()
    browser.page().mainFrame().addToJavaScriptWindowObject("python", pjs)
    sys.exit(app.exec_())


if __name__ == '__main__':
    my_main()