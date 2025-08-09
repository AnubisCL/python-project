import re

import requests
from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def getCodeText():
    # 下载验证码图片
    url = 'https://vidhub.tv/verify/index.html'
    r = requests.get(url)
    with open('code.jpg', 'wb') as f:
        f.write(r.content)
    # 打开图片并进行二值化处理
    im = Image.open('/Users/anubis/PycharmProjects/python-project/drission-page/code.jpg')
    im = im.convert('L')
    threshold = 127
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')
    # 使用pytesseract将图片转换为文本
    text = pytesseract.image_to_string(im)
    text = re.sub(r'[^\w]', '', text)
    print('\tcode => ', text)
    return text


if __name__ == '__main__':
    getCodeText()
