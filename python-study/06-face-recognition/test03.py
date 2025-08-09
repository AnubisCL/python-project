# coding=gbk
# 1.导入模块
import face_recognition

# 2.通过face_recognition模块中load_image_file方法加载图片
image = face_recognition.load_image_file('images/柴磊.jpg')

# 3.输入图片内容，以便验证
print(image)