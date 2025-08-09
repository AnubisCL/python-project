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

# 3.调用加载图片函数

load_img('facelib')