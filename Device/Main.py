import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import funcs as fun

# UIs
main_class = uic.loadUiType('UIs/Main.ui')[0]  # 메인창


# Main
class MainWindowClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowClass()
    mainWindow.show()
    app.exec_()

