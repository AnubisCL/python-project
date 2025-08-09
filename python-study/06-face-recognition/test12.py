# coding=gbk
# 1.导入模块
import face_recognition
import cv2
from PIL import Image, ImageDraw


# 2.添加一张多人照片图片
image1 = face_recognition.load_image_file('images/lsrs.jpg')

# 3.添加一张单人照片图片
image2 = face_recognition.load_image_file('facelib/李硕然.bmp')

# 4.创建多人照片编码信息对象
known_face_encodings = face_recognition.face_encodings(image1)

# 5.创建单人照片编码信息对象,取出数组中第一个元素。
compare_face_encoding = face_recognition.face_encodings(image2)[0]
face_locations = face_recognition.face_locations(image2)

# 6.使用face_recognition模块中compare_faces方法进行信息编码比对，tolerance值为0.42
matches = face_recognition.compare_faces(known_face_encodings,compare_face_encoding, tolerance=0.46)
i = 0

# for face_location in face_locations:
#     # 解包操作，就可以得到每张人脸的四个位置信息
#     top, right, bottom, left = face_location
#     # 定义图片启始与结束位置
#     start = (left, top)
#     end = (right, bottom)
#     # 使用cv2模块中的rectangle方法为指定的图片绘图矩形框，矩形框为红色，像素为2
#     image3 = cv2.rectangle(image1, start, end, (0, 0, 255), thickness=2)
#     cv2.putText(image1, matches[++i], (left, top-30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

print(matches)

# pil_image = Image.fromarray(image2)
#
# d = ImageDraw.Draw(pil_image)
# pil_image.show()