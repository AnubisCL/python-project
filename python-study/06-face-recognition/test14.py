# coding=gbk

# 1. 导入模块
import face_recognition
import cv2

# 2.创建未知图片对象
unknown_image = face_recognition.load_image_file('images/lsrs.jpg')

# 3. 创建已知图片对象
known_image = face_recognition.load_image_file('facelib/李硕然.bmp')

# 4.创建空列表，用于添加对比结果
results = []

# 5.使用face_recognition模块face_encodings方法获取已知人脸编码信息
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# 6.使用face_recognition模块face_encodings方法获取未知图片人脸编码信息
unknown_face_encodings = face_recognition.face_encodings(unknown_image)

# 7.使用face_recognition模块face_locations方法获取未知图片人脸位置信息
face_locations = face_recognition.face_locations(unknown_image)

# 8.使用for循环遍历未知图片中人脸，对每张人脸进行编码，然后比对已知图片人脸与未知图片中人脸
for i in range(len(face_locations)):
    # 每张人脸位置数据
    top, right, bottom, left = face_locations[i]
    # 找出未知图片中人脸位置
    face_image = unknown_image[top:bottom, left:right]

    # 对未知图片中人脸进行分别编码
    face_encoding = face_recognition.face_encodings(face_image)
    # 判断人脸编码结果是否为非空
    if face_encoding:
        result = {}
        # 使用已知图片人脸与未知图片人脸进行对比，tolerance为0.42
        matches = face_recognition.compare_faces([unknown_face_encodings[i]], known_face_encoding, tolerance=0.44)
        # 判断matches为True，即可把下列信息添加到result列表中
        if True in matches:
            print('在未知图片中找到了已知面孔')
            result['face_encoding'] = face_encoding
            result['is_view'] = True
            result['location'] = face_locations[i]
            result['face_id'] = i + 1
            results.append(result)
            # 判断result列表中'is_view'是否为空，如果不为空，则证明已匹配到人脸
            if result['is_view']:
                print('已知面孔匹配照片上的第{}张脸'.format(result['face_id']))

# 9.在未知图片中勾勒出已知图片人脸

# 9.1 获取在未知图片中找到的人脸位置信息存入列表中
view_face_locations = [i['location'] for i in results if i['is_view']]

# 9.2 判断上述列表是否大于0，如果大于0，则从上述列表中获取人脸位置数据，用于添加矩形框
if len(view_face_locations) > 0:
    for location in view_face_locations:
        top, right, bottom, left = location
        start = (left, top)
        end = (right, bottom)
        # 矩形框
        cv2.rectangle(unknown_image, start, end, (0, 0, 255), thickness=2)

        # 定义字体
        font = cv2.FONT_HERSHEY_COMPLEX

        # 在矩形框添加文字，left+6及bottom+16是文字在矩形框边上的位置，1.0是字号，255，255，255是矩形框颜色
        cv2.putText(unknown_image, 'LiShuoRan', (left + 6, top -16), font, 0.5, (0, 255, 0), 1)

# 10.图片展示
cv2.imshow('windows', unknown_image)
cv2.waitKey()
