import qrcode
from PIL import Image, ImageDraw
import requests
import datetime
from google.cloud import storage
device_id = 'ABC123'


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


# 영수증 이미지를 gcs에 올리고 링크를 받아 API서버에 튜플 생성을 요청하고, qrcode로 생성할 url을 받아온다
def upload_receipt_data(receipt_img):
    try:
        now = datetime.datetime.now()
        image_name = '{}_{}{}{}_{}{}{}'.format(device_id, now.year, now.month, now.day, now.hour, now.minute, now.second)
        file_name = open(receipt_img, 'rb')                           # 업로드할 이미지의 파일 객체
        blob_name = 'receipts/{}.jpg'.format(image_name)  # 업로드할 이미지의 gcs 경로

        # gcs에 이미지 업로드 요청
        try:
            upload_file_gcs(file_name, blob_name)
        except Exception as ex:
            print('Hey! upload: ', ex)

        # gcs에 저장된 이미지의 link url 반환 요청
        try:
            link_url = get_linkurl_gcs(blob_name)
            print(link_url)
        except Exception as ex:
            print('Hey!: return', ex)
    except Exception as ex:
        print('Hey!: ', ex)

    try:
        upload_url = 'http://dsc-ereceipt.appspot.com/api/main/upload_img/'
        headers = {'Contest-Type': 'application/json'}
        data = {
           "receipt_img_url": link_url,
            "device_id": device_id
        }
        res = requests.post(
            upload_url,
            headers=headers,
            data=data
        )
        print(res.status_code, res.text)
        return res.text[1:-1]
    except Exception as ex:
        print('Hey!: ', ex)


# 스토리지 파일 업로드 함수
def upload_file_gcs(file_name, destination_blob_name, bucket_name='dsc_ereceipt_storage'):
    # file_name : 업로드할 파일명
    # destination_blob_name : 업로드될 경로와 파일명
    # bucket_name : 업로드할 버킷명
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file_name)

    print(
        "File {} uploaded to {}".format(
            file_name, destination_blob_name
        )
    )


# 스토리지에 업로드된 파일의 링크url을 가져오는 함수
def get_linkurl_gcs(blob_name, bucket_name='dsc_ereceipt_storage'):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    print(
        "Blob {}'s url : {}".format(
            blob_name, blob.public_url
        )
    )

    return blob.public_url



