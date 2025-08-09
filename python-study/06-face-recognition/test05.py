# coding=gbk
# 1.导入模块
import face_recognition

# 2.通过face_recognition模块中load_image_file方法加载图片
image = face_recognition.load_image_file('images/柴磊.jpg')

# 3.通过face_locations方法得到图像中所有人脸信息
face_locations = face_recognition.face_locations(image)

# 4.输出,包含top,right,bottom,left信息
for face_location in face_locations:
    top, right, bottom, left = face_location
    print("已识别人脸部位，像素区域为：Top:{},right:{},bottom:{},left:{}".format(top,right,bottom,left))