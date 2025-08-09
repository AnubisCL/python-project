# coding=gbk

# 1.导入模块
import face_recognition

# 2.读取要处理的图片，生成图片对象
image = face_recognition.load_image_file('images/柴磊.jpg')

# 3.使用face_recognition模块中的face_landmarks方法处理图片对象，得到图片中全部人脸的特征数据。
face_landmarks_list = face_recognition.face_landmarks(image)

# 4.测试输出
print(face_landmarks_list)