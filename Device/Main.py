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

    total_amount = 0    # 전체 결제 금액
    items_name = []     # 선택한 메뉴들
    items_price = []    # 선택한 메뉴들의 금액

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # QRcode_IMG를 Default한 이미지로 변경
        qPixmapVar = QPixmap()
        qPixmapVar.load('qrcodes/blank.jpg')
        self.QRcode_IMG.setPixmap(qPixmapVar)
        self.Receipt_IMG.setPixmap(qPixmapVar)

        # 기능 btn 관리
        btn_do = {
            self.btn_charge.clicked.connect(self.charge),
            self.btn_clear.clicked.connect(self.clearList),
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
        # 영수증 이미지 생성
        fun.receipt_generator(self.total_amount, self.items_name, self.items_price)
        qPixmapVar = QPixmap()
        receipt_img = 'receipts/receipt.jpg'
        qPixmapVar.load(receipt_img)
        self.Receipt_IMG.setPixmap(qPixmapVar)
        self.Receipt_IMG.repaint()

        # api에 영수증 업로드
        qr_url = fun.upload_receipt_data(receipt_img)

        # QR code 생성 및 저장
        qr_name = 'test'
        fun.qrcode_generator(qr_url, qr_name)

        # QR code 이미지 불러오기
        qPixmapVar = QPixmap()
        qPixmapVar.load('qrcodes/{}.jpg'.format(qr_name))
        qPixmapVar.scaled(200, 200)
        self.QRcode_IMG.setPixmap(qPixmapVar)
        self.QRcode_IMG.repaint()

    # 리스트, lcd number clear
    def clearList(self):
        self.selected_items_name.clear()
        self.selected_items_price.clear()

        self.items_name.clear()
        self.items_price.clear()

        self.total_amount = 0

        self.show_amount.display(self.total_amount)
        self.show_amount.repaint()

    # 리스트에 선택한 항목과 금액을 올리고, lcd에 금액 출력
    def add_amount(self, item):
        # 리스트 위젯에 추가
        self.selected_items_name.addItem(item.name)
        self.selected_items_price.addItem(str(item.price))

        # 아이템과 가격을 저장하는 list에 저장
        self.items_name.append(item.name)
        self.items_price.append(item.price)

        # 최 금액 저장종
        self.total_amount = self.total_amount + item.price

        # lcd창에 최종금액 출력
        self.show_amount.display(self.total_amount)
        self.show_amount.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowClass()
    mainWindow.show()
    app.exec_()
