# coding=gbk
# 1.导入模块
import face_recognition

# 2.创建图片对象
image = face_recognition.load_image_file('images/柴磊.jpg')

# 使用face_recognition模块中的face_encodings方法实现对人脸特证数据获取，不管图像中有多少张人脸信息，返回值都是一个列表
face_encodings = face_recognition.face_encodings(image)

# 3.使用for循环进行遍历
for face_encoding in face_encodings:
    # 输出为一个128位的向量列表，表示人脸特征
    print("信息编码长度为:{}\n编码信息为:{}".format(len(face_encoding),face_encoding))