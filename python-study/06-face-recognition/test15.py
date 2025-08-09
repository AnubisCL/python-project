# coding=gbk
# 1.导入模块
import cv2
from PIL import Image, ImageDraw
import numpy as np

# 2. 调用摄像头,如果有多个摄像头，可以通过位置进行设定，下面0即为第1个摄像头，是必填项
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 3.读取摄像头的图像信息，把frame信息转换为图片，再使用CV2把图片显示出来
while True:
    # 返回一帧的数据（以元组方式返回，使用2个变量接收）,ret返回的状态数据，frame是帧数据
    ret, frame = cap.read()
    # 传入的frame都是以Numpy数组的方式进行保存的，需要从数据当中还原数据。需要使用PIL图像进行展示，BGR是CV2模块中保存图像格式，RGB是PIL模块中保存图像格式，在转换时需要做格式上的转换
    img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # 画图
    draw = ImageDraw.Draw(img_PIL)

    # 4.在图像上添加文字

    # 添加文本内容,100,100为文字像素位置，fill为文本填充颜色
    draw.text((100, 100), 'press q to exit', fill=(255, 255, 255))

    # 将frame对象转换回CV2格式,cv2.COLOR_RGB2BGR把图像格式转换回CV2格式图像
    frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

    # 展示图片
    cv2.imshow('capture', frame)

    # 需要让while循环停止，可以使用下面语句
    if cv2.waitKey(1) & 0XFF == ord('q'):
        # 5.保存图像
        # 保存图像
        cv2.imwrite('out.jpg', frame)
        # 终止while循环
        break

# 6.释放摄像头
cap.release()

# 7.删除建立的窗口
cv2.destroyAllWindows()
