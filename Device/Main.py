import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import funcs as fun
import Items as it

# UIs
main_class = uic.loadUiType('UIs/Main.ui')[0]  # 메인창

# Main
class MainWindowClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 기능 btn 관리
        btn_do = {
            self.btn_charge.clicked.connect(self.charge),
            self.btn_print.clicked.connect(self.print_receipt),
        }

        # 메뉴 btn 관리
        btn_menu = {
            # Coffee & Esprosso
            self.btn_cof_americano.clicked.connect(lambda: self.add_amount(it.cof_Americano)),
            self.btn_cof_brewed.clicked.connect(lambda: self.add_amount(it.cof_brewed)),
            self.btn_cof_caramel.clicked.connect(lambda: self.add_amount(it.cof_caramel)),
            self.btn_cof_cappuccino.clicked.connect(lambda: self.add_amount(it.cof_cappuccino)),
            self.btn_cof_decaf.clicked.connect(lambda: self.add_amount(it.cof_decaf)),
            self.btn_cof_latte.clicked.connect(lambda: self.add_amount(it.cof_latte)),
            self.btn_cof_mocha.clicked.connect(lambda: self.add_amount(it.cof_mocha)),

            # Teavana
            self.btn_tea_chai.clicked.connect(lambda: self.add_amount(it.tea_chai)),
            self.btn_tea_earl.clicked.connect(lambda: self.add_amount(it.tea_earl)),
            self.btn_tea_grapefruite.clicked.connect(lambda: self.add_amount(it.tea_grapefruit)),
            self.btn_tea_green.clicked.connect(lambda: self.add_amount(it.tea_green)),
            self.btn_tea_lemon.clicked.connect(lambda: self.add_amount(it.tea_lemon)),
            self.btn_tea_lime.clicked.connect(lambda: self.add_amount(it.tea_lime)),
            self.btn_tea_vanilla.clicked.connect(lambda: self.add_amount(it.tea_vanilla)),

            # Fizzio
            self.btn_fiz_pink.clicked.connect(lambda: self.add_amount(it.fiz_pink)),
            self.btn_fiz_lime.clicked.connect(lambda: self.add_amount(it.fiz_lime)),
            self.btn_fiz_black.clicked.connect(lambda: self.add_amount(it.fiz_black)),

            # Chocolate
            self.btn_cho_signature.clicked.connect(lambda: self.add_amount(it.cho_signature)),

            # Frappucino
            self.btn_fra_java.clicked.connect(lambda: self.add_amount(it.fra_java)),
            self.btn_fra_white.clicked.connect(lambda: self.add_amount(it.fra_white)),
            self.btn_fra_mocha.clicked.connect(lambda: self.add_amount(it.fra_mocha)),
            self.btn_fra_green.clicked.connect(lambda: self.add_amount(it.fra_green)),
            self.btn_fra_chocolate.clicked.connect(lambda: self.add_amount(it.fra_chocolate)),
            self.btn_fra_strawberries.clicked.connect(lambda: self.add_amount(it.fra_strawberries)),
            self.btn_fra_avocado.clicked.connect(lambda: self.add_amount(it.fra_avocado)),
        }

    # 기능 btn
    # 결제 버튼
    def charge(self):
        print('charge')

    # 영수증 프린트 버튼
    def print_receipt(self):
        print('print_receipt')

    def add_amount(self, item):
        print(item.name)
        print(item.price)
        self.selected_items.addItem(item.name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowClass()
    mainWindow.show()
    app.exec_()
