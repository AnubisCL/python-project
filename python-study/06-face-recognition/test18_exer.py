# coding=gbk

# 1.导入模块
import face_recognition
import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# 2.定义加载图片函数,加载所有已知人员图片并生成人脸编码信息
def load_img(path):
    print('正在加载已知人员图片')
    # dirpath是目录路径，dirnames是目录下子目录，filename是目录下文件
    for dirpath, dirnames, filenames in os.walk(path):
        print(dirpath, dirnames, filenames)
        # 定义一个空列表facelib，用于存储遍历到的所有人脸编码信息
        facelib = []

        # 使用for循环实现已知人脸图片目录中所有人脸编码存储到上述列表中
        for filename in filenames:
            # 拼接文件路径
            filepath = os.sep.join([dirpath, filename])
            # 加载用于进行编码的图片
            face_image = face_recognition.load_image_file(filepath)

            # 对已加载图片进行编码
            face_encoding = face_recognition.face_encodings(face_image)[0]

            # 添加图片编码信息到facelib列表中
            facelib.append(face_encoding)

        return facelib, filenames


# 3.调用加载图片函数
facelib, filenames = load_img('facelib')

# 4.调用摄像头
# 4.1 创建摄像头对象
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 4.2 使用while循环实现对摄像头持续读取
while True:
    # 读取摄像头内容，被ret及frame接收
    ret, frame = video_capture.read()
    # 缩小图片（缩小为原图的1/4），提高对比效率,(0,0)不直接指定缩小大小，由fx及fy指定
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # 将opencv BGR格式转换为RGB格式
    rgb_small_frame = small_frame[:, :, ::-1]

    # 把转换格式后的图片中找到人脸位置
    face_locations = face_recognition.face_locations(rgb_small_frame)

    # 对rgb_small_frame图片中的face_locations（位置信息）传给face_encodings生成编码信息
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # 定义一个空列表，用于存储已比对成功人员名单
    face_names = []

    # 如果摄像头中有多张人脸，可以使用for循环遍历多张人脸编码信息，达到比对的目的

    for face_encoding in face_encodings:
        # 把摄像头中出现的人脸编码信息与已知人脸信息进行比对                             (0.39)
        matches = face_recognition.compare_faces(facelib, face_encoding, tolerance=0.46)
        print(matches)
        name = '未知成员'
        # 进行判断
        if True in matches:
            # 如果摄像头里面的头像匹配了已知人物头像，则取出第一个True的位置
            first_match_index = matches.index(True)
            # 如果为True，需要取出已知人员的名字，存至face_names列表中，因此需要使用下述方法截取人员名字。
            name = filenames[first_match_index][:-4]

        # 把已对比的已知人员名字追加到face_names列表中
        face_names.append(name)
        print(face_names)

    # 对摄像头中出现的人员面部进行框选
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 因为需要进行显示，所以需要进行还原，乘4的原因是原先缩小为0.25了
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # 使用cv2模块rectangle方法实现人脸标注，矩形框，（0，0，255）为红色，2为线宽
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 生成PIL图片对象,过程中使用cv2.COLOR_BGR2RGB进行格式转换
        img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 定义字体,simhei.ttf为黑体，字号为40
        font = ImageFont.truetype('simhei.ttf', 40)

        # 创建draw对象
        draw = ImageDraw.Draw(img_PIL)

        # 添加文字,(left + 6,bottom - 6)为位置，name为已知人员名字，font为字体，fill为字的颜色
        draw.text((left + 6, bottom - 6), name, font=font, fill=(255, 255, 255))

        # 把img_PIL还原为cv2格式，便于展示
        frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    # 使用cv2模块中的imshow方法对图像进行展示
    cv2.imshow('Video', frame)

    # 退出while循环，waitKey(1)为设置阻塞时间，为1秒，如果不设置无法继续获得下一帧数据。
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

# 释放摄像头资源

video_capture.release()
