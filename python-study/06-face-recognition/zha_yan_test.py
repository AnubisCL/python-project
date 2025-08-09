# coding=gbk

# 1.导入模块
# 1.1 计算欧式距离公式所使用的模块

from scipy.spatial import distance

# 1.2 人眼检测模块
import dlib

# 1.3 cv2模块
import cv2

# 1.4 图像处理库
from imutils import face_utils


# 2.定义计算函数
def eye_aspect_ratio(eye):
    """
    计算EAR值
    :param eye: 眼部特征点数组
    :return: EAR值
    """
    A = distance.euclidean(eye[1],eye[5])
    B = distance.euclidean(eye[2],eye[4])
    C = distance.euclidean(eye[0],eye[3])
    return (A + B) / (2.0 * C)

# 3.创建人脸检测器
detector = dlib.get_frontal_face_detector()

# 4.创建预测器
predictor = dlib.shape_predictor('libs/shape_predictor_68_face_landmarks.dat')

# 5.设置眼睛纵横比的阈值,如果小于定义的0.3这个值就认为闭眼了
EAR_THRESH = 0.3

# 6.定义闭眼时长阈值，例如连续3帧，就认为真的闭眼了
EAR_CONSEC_FRAMES = 3

# 7.定义人脸特征点中对应眼睛的特征点的序号，为了与数组中的索引值有对应，这里定义的序号全部减1
# 7.1 右眼
RIGHT_EYE_START = 37 - 1
RIGHT_EYE_END = 42 - 1

# 7.2 左眼
LEFT_EYE_START = 43 - 1
LEFT_EYE_END = 48 - 1

# 8.定义连续帧计数
frame_counter = 0

# 9.定义眨眼的计数
blink_counter = 0

# 10.创建摄像头对象
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# 使用while循环对摄像头中的数据连接读取及处理
while True:
    # 定义变量
    ret,frame = cap.read()
    # 转换为灰度图像,利于比较
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # 输入灰度图像，并放大1倍,对人脸进行检测
    rects = detector(gray,1)

    # 对检测的人脸数进行判断
    if len(rects) > 0:
        # 检测人脸特征点
        shape = predictor(gray,rects[0])
        # 使用imutils模块中的face_utils.shape_to_np方法把检测到的人脸特征转化为数组
        points = face_utils.shape_to_np(shape)

        # 取出左眼特征点数据
        leftEye = points[LEFT_EYE_START:LEFT_EYE_END + 1]

        # 取出右眼特征点数据
        rightEye = points[RIGHT_EYE_START:RIGHT_EYE_END + 1]

        # 计算出左右眼EAR值
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # 求左右眼EAR平均值
        ear = (leftEAR + rightEAR) / 2.0
        # 找出左右眼的轮廓,为了演示效果，实际生产中可以不用加下面两行
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        # 绘制出左右眼轮廓,-1表示不指定画图位置，（0，255，0）表示颜色，1表示线宽，为了演示效果，实际生产中可以不用加下面两行
        cv2.drawContours(frame,[leftEyeHull],-1,(0,255,0),1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # 判断是否闭眼，如果EAR小于阈值，开始计算连续帧
        if ear < EAR_THRESH:
            frame_counter += 1
        else:
            if frame_counter >= EAR_CONSEC_FRAMES:
                print('眨眼检测成功，通过。')
                blink_counter += 1
                break
            frame_counter = 0

        # # 添加文字说明,可测试使用
        # cv2.putText(frame,"blink:{}".format(blink_counter))
    cv2.imshow('window',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()