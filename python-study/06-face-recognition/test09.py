# coding=gbk

# 1.导入模块
import face_recognition
from PIL import Image,ImageDraw

# 2.读取要处理的图片，生成图片对象
image = face_recognition.load_image_file('images/柴磊.jpg')

# 3.使用face_recognition模块中的face_landmarks方法处理图片对象，得到图片中全部人脸的特征数据。
face_landmarks_list = face_recognition.face_landmarks(image)

# 4.基于图片特征创建一个多维数组
pil_image = Image.fromarray(image)

# 5.基于上述数组创建PIL图像
d = ImageDraw.Draw(pil_image)

# 6.通过for循环遍历每张人脸上的特征绘图
for face_landmarks in face_landmarks_list:
    # 五官列表
    facial_features = [
        'chin',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'left_eye',
        'right_eye',
        'bottom_lip'
    ]
    # 通过for循环输出每张人脸五官在列表中的数据，并绘制出具体的位置
    for facial_feature in facial_features:
        print("{}每个人脸五官显示的位置:{}".format(facial_feature,face_landmarks[facial_feature]))