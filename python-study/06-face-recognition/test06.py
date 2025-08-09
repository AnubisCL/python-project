# coding=gbk
# 1.导入模块
import face_recognition
from PIL import Image

# 2.通过face_recognition模块中load_image_file方法加载图片
image = face_recognition.load_image_file('images/柴磊.jpg')

# 3.通过face_locations方法得到图像中所有人脸信息
face_locations = face_recognition.face_locations(image)

# 4.输出每张人脸信息

for face_location in face_locations:
    # 解包操作，就可以得到每张人脸的四个位置信息
    top,right,bottom,left = face_location

    # 创建人脸图片对象，把人脸从大图片中切出来，形成一张张小图
    face_image = image[top:bottom,left:right]
    #使用pil中image方法对人脸进行绘图
    pil_image = Image.fromarray(face_image)
    # 展示人脸绘图效果
    pil_image.show()
