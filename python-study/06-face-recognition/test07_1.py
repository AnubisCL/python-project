# coding=gbk
import face_recognition
import cv2
from PIL import Image, ImageDraw

# 蓝
image = face_recognition.load_image_file('images/our01.jpg')

face_locations = face_recognition.face_locations(image)

text = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
index = 0
for face_location in face_locations:
    # 解包操作，就可以得到每张人脸的四个位置信息
    top, right, bottom, left = face_location
    # 定义图片启始与结束位置
    start = (left, top)
    end = (right, bottom)
    # 使用cv2模块中的rectangle方法为指定的图片绘图矩形框，矩形框为红色，像素为2
    cv2.putText(image, 'Persion', (left, top - 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    image2 = cv2.rectangle(image, start, end, (0, 0, 255), thickness=2)

pil_image = Image.fromarray(image2)

d = ImageDraw.Draw(pil_image)
pil_image.show()
