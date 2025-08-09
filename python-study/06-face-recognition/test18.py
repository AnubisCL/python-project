# coding=gbk

# 1.导入模块
import face_recognition
import os

# 2.定义加载图片函数,加载所有已知人员图片并生成人脸编码信息
def load_img(path):
    print('正在加载已知人员图片')
    # dirpath是目录路径，dirnames是目录下子目录，filename是目录下文件
    for dirpath,dirnames,filenames in os.walk(path):
        print(dirpath,dirnames,filenames)
        # 定义一个空列表facelib，用于存储遍历到的所有人脸编码信息
        facelib = []

        # 使用for循环实现已知人脸图片目录中所有人脸编码存储到上述列表中
        for filename in filenames:
            # 拼接文件路径
            filepath = os.sep.join([dirpath,filename])
            # 加载用于进行编码的图片
            face_image = face_recognition.load_image_file(filepath)

            # 对已加载图片进行编码
            face_encoding = face_recognition.face_encodings(face_image)[0]

            # 添加图片编码信息到facelib列表中
            facelib.append(face_encoding)

            return facelib,filenames


# 3.调用加载图片函数

facelib,facenames = load_img('facelib')

print(facenames)