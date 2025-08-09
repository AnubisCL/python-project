# coding=gbk
# 1.导入dlib模块
import dlib

# 2.导入文件读取模块
from skimage import io

# 3.创建一个脸部检测器，其包含了脸部检测算法
detector = dlib.get_frontal_face_detector()

# 4.创建一个图片显示窗口
win = dlib.image_window()

# 5.创建图片对象
img = io.imread('images/柴磊.jpg')

# 6.使用脸部检测器读取待检测的图像数据，第2个参数代表读取图片像素放大1倍,以便能够收到到更多的照片细节
# 返回结果为一组人脸区域的数组

dets = detector(img, 1)

# print(dets)

# 7. 在窗口中需要设置的图片
win.set_image(img)

# 8.使用矩形边框实现对人脸框选
win.add_overlay(dets)

# 9.保留窗口以便能够查看到图片内容，即窗口保留不会自动消失。
dlib.hit_enter_to_continue()