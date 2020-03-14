import qrcode

# QR코드 생성기 
def qrcode_generator(url, imgname):
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