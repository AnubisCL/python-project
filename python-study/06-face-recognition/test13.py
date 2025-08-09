# coding=gbk

# 1. 导入模块
import face_recognition

# 2.创建未知图片对象
unknown_image = face_recognition.load_image_file('images/our.jpg')

# 3. 创建已知图片对象
known_image = face_recognition.load_image_file('images/柴磊.jpg')

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
    top,right,bottom,left = face_locations[i]
    # 找出未知图片中人脸位置
    face_image = unknown_image[top:bottom,left:right]

    # 对未知图片中人脸进行分别编码
    face_encoding = face_recognition.face_encodings(face_image)
    # 判断人脸编码结果是否为非空
    if face_encoding:
        result = {}
        # 使用已知图片人脸与未知图片人脸进行对比，tolerance为0.42
        matches = face_recognition.compare_faces([unknown_face_encodings[i]],known_face_encoding,tolerance=0.46)
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