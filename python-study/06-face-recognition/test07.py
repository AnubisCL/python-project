# coding=gbk
# 1.导入模块
import face_recognition
import cv2

# 蓝
# 2.通过face_recognition模块中load_image_file方法加载图片
image = face_recognition.load_image_file('images/lsrs.jpg')

# 3.通过face_locations方法得到图像中所有人脸信息
face_locations = face_recognition.face_locations(image)

# 4.输出每张人脸信息

for face_location in face_locations:
    # 解包操作，就可以得到每张人脸的四个位置信息
    top, right, bottom, left = face_location
    # 定义图片启始与结束位置
    start = (left, top)
    end = (right, bottom)
    # 使用cv2模块中的rectangle方法为指定的图片绘图矩形框，矩形框为红色，像素为2
    cv2.rectangle(image, start, end, (0, 0, 255), thickness=2)

# 使用cv2中imshow方法显示图片
cv2.imshow('windows', image)
# 不要让窗口退出
cv2.waitKey()
