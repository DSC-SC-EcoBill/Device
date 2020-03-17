import qrcode
from PIL import Image, ImageDraw
import requests


# 영수증 이미지 생성
def receipt_generator(total_amount, items, prices):
    # 영수증 내용 작성
    receipt_start = '''
            DSC Sahmyook Doyoubucks
    Address : 815, Hwarang-ro, Nowon-gu, Seoul
    TEL : (02)3399-3636
    ------------------------------------------
    Items                           Price  
    '''

    # item 목록 작성
    receipt_body = [receipt_start, ]
    for _ in range(len(items)):
        receipt_body.append('''
    {0:<28}    {1}
        '''.format(items[_], prices[_]))

    receipt_end = '''
    ------------------------------------------
    Total                           {} won
    ------------------------------------------
                    Thank you!
    '''.format(total_amount)
    receipt_body.append(receipt_end)

    # 영수증 내용 합치기
    receipt_result = ''.join(receipt_body)

    # Image 생성
    img = Image.new('RGB', size=(300, 311), color='White')
    d = ImageDraw.Draw(img)
    d.text((0, 0), receipt_result, fill='black', spacing=0)
    img.save('receipts/receipt.jpg')


# QR코드 생성
def qrcode_generator(url, imgname):
    if url is not None:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=7,
            border=2
        )
        qr.add_data(url)
        qr.make()
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('qrcodes/{}.jpg'.format(imgname))
    else:
        print(url)


# API에 영수증 이미지 업로드
def upload_receipt(receipt_img):
    try:
        upload_url = 'http://127.0.0.1:8000/api/main/upload_receipt/'

        files = open(receipt_img, 'rb')
        upload = {'file': files}

        res = requests.post(upload_url, files=upload)
        # res = requests.post(upload_url)
        print(res.json())

        qr_url = res.json()
        return qr_url

    except Exception as ex:
        print('야 API에 영수증 올리다 에러났다 ㅠㅠ ', ex)


