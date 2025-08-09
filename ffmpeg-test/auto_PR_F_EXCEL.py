"""
@description: 使用 paddleocr 识别每一帧中的文本，并提取 C109 和 00:00:00:00后，对视频进行分割，并保存为 mp4 和 wav 文件
@author: anubis
"""

import concurrent
import os
import queue

# import cv2
from moviepy.editor import VideoFileClip
import re
# from paddleocr import PaddleOCR

parent_video_path = '/Users/anubis/PycharmProjects/python-project/ffmpeg-test/109-118.mp4'  # FIXME 处理视频文件
clip_mp4_path = '/Users/anubis/PycharmProjects/python-project/ffmpeg-test/mp4/'  # FIXME 视频文件保存位置
clip_wav_path = '/Users/anubis/PycharmProjects/python-project/ffmpeg-test/wav/'  # FIXME 音频文件保存位置
x, y, w, h = 170, 100, 600, 140  # FIXME # 保存裁剪后的文本区域图像
keyword = "00:00:00:00"  # FIXME 需要匹配的关键字

video_clip = VideoFileClip(parent_video_path)  # 视频对象
video_frames = int(video_clip.duration * video_clip.fps)  # 视频总帧数
timers = queue.Queue()  # 线程安全List


def get_suffix(text):
    """
    FIXME 获取帧中的文本，并提取 C109 和 00:00:00:00
    :param text:
    :return:
    """
    cleaned_text = text.replace("\n", "").replace(" ", "")
    pattern = r'C\d{3}'
    suffix_text = re.search(pattern, cleaned_text).group()
    pattern_time = r'\d{2}[:.]\d{2}[:.]\d{2}[:.]\d{2}'
    time_text = re.search(pattern_time, cleaned_text).group()
    new_text = re.sub(r'[:.]', r':', time_text)  # 文本保底处理
    return suffix_text, new_text


def video_info(clip):
    """
    打印视频的基本信息
    :param clip: 视频
    :return:
    """
    # 获取视频的总帧数
    frames = int(clip.duration * clip.fps)
    # 打印视频的基本信息
    print(f"视频总时长：{clip.duration} 秒")
    print(f"视频帧率：{clip.fps}")
    print(f"视频尺寸：{clip.size}")
    print(f"视频总帧数：{frames}")


def save_segment(start_frame, end_frame, frame_rate, suffix):
    """
    使用 ffmpeg 将视频分割为多段
    ffmpeg -i 109.mp4 -filter_complex "[0:v]select='between(n,0,99)',setpts=N/FRAME_RATE/TB[v]" -map "[v]" output_0_99.mp4
    ffmpeg -i 109.mp4 -filter_complex "[0:a]aselect='between(n,0,198)',asetpts=N/SR/TB[a]" -map "[a]" -acodec pcm_s16le output_0_99.wav

    ffmpeg -i 109.mp4 -filter_complex "[0:v]select='between(n,0,99)',setpts=N/FRAME_RATE/TB[v]" -map "[v]" output_0_99.mp4
    ffmpeg -i 109.mp4 -filter_complex "[0:a]aselect='between(n,0,19200)',asetpts=N/SR/TB[a]" -map "[a]" -acodec pcm_s16le output_0_99.wav
    音频采样率： 48000 Hz  音频帧数量 = 视频帧数量 * 音频采样率 / 视频帧率
    ffmpeg -i output_0_99.mp4 -acodec pcm_s16le -vn output_0_99.wav
    :param start_frame: 开始帧
    :param end_frame: 结束帧
    :param frame_rate: 帧率
    :param suffix: 文件前缀
    :return:
    """
    # command_vide = f'ffmpeg -i {parent_video_path} -ss {start_frame / frame_rate} -to {end_frame / frame_rate} -c:v copy {clip_mp4_path}{suffix}_{end_frame - start_frame}f.mp4'
    mp4Path = f'{clip_mp4_path}{suffix}_{end_frame - start_frame}f'
    # command_vide = f'ffmpeg -i {parent_video_path} -filter_complex "[0:v]select=\'between(n,{start_frame},{end_frame - 1})\',setpts=N/FRAME_RATE/TB[v]" -map "[v]" {mp4Path}.mp4'
    # os.system(command_vide)
    # command_sound = f'ffmpeg -i {mp4Path}.mp4 -vn -acodec pcm_s16le {clip_wav_path}WG_EP220_{suffix}.wav'
    # os.system(command_sound)

    clip1 = VideoFileClip(mp4Path + '.mp4')  # 读取视频对象
    shenyin = clip1.audio
    shenyin.write_audiofile(f'{clip_wav_path}WG_EP220_{suffix}.wav')  # 提取保存视频音频

def filter_dirty_frame(lst, gap=1):
    """
    过滤重复的 '00:00:00:00' 帧
    :param lst: 过滤list
    :param gap: 相邻阈值
    :return:
    """
    lst_new = []
    # 使用双指针遍历列表
    left = 0
    right = 1
    while right < len(lst):
        lst_new.append(lst[right]['idx'] - lst[left]['idx'])
        left += 1  # 移动左指针
        right += 1  # 移动右指针

    i = 0
    for index, e in enumerate(lst_new):
        if e == gap:
            del lst[index - i]  # 根据原始列表的索引进行删除操作
            i += 1
    return lst


def preprocess_image_paddle(image):
    """
    使用 paddleocr 识别帧中的文本
    :param image:
    :return:
    """
    # 裁剪文本区域
    text_region = image[y:y + h, x:x + w]
    # 使用默认模型路径
    # paddleocr = PaddleOCR(lang='en', show_log=False, use_gpu=True, ir_optim=True, cpu_threads=20)
    # result = paddleocr.ocr(text_region)
    text = ''
    # for i in range(len(result[0])):
    #     text = text + (result[0][i][1][0])  # 拼接识别结果
    return text


def process_frame(idx, frame):
    """
    处理每一帧
    :param idx: 帧 index
    :param frame: 帧 image
    :return:
    """
    text = preprocess_image_paddle(frame)
    try:
        suffix, time = get_suffix(text)
    except Exception as e:
        print(f"处理第:{idx + 1}帧,识别异常：{text}")
        # 裁剪文本区域
        text_region = frame[y:y + h, x:x + w]
        # cv2.imwrite(f"{idx}_error.jpg", text_region)
        return
    # 打印识别结果
    # print(f"处理第:{idx + 1}帧,识别结果:{suffix}-{time}")
    if time in keyword or video_frames == idx or idx == 0:
        timers.put({'idx': idx, 'time': time, 'suffix': suffix})


def foreach_video_thread():
    """
    使用多线程遍历视频的每一帧
    :return:
    """
    frames = list(video_clip.iter_frames(fps=25))
    # 开启线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_frame, idx, frame): (idx, frame) for idx, frame in enumerate(frames)}
        for future in concurrent.futures.as_completed(futures):
            idx, frame = futures[future]
            future.result()


if __name__ == '__main2__':
    '''
    视频总时长：7.83 秒
    视频帧率：25.0
    视频尺寸：[1920, 1080]
    视频总帧数：195
    [
    {'idx': 0, 'time': '00:00:00:00', 'suffix': 'C109'},
    {'idx': 99, 'time': '00:00:00:00', 'suffix': 'C109'},
    {'idx': 195, 'time': '00:00:00:00', 'suffix': 'C110'}
    ]
    '''
    # 多线程解析视频帧 存入 timers
    foreach_video_thread()
    # timers 排序
    sorted_list = []
    while not timers.empty():
        sorted_list.append(timers.get())
    sorted_list.sort(key=lambda x: x['idx'])
    # sorted_list 过滤重复 '00:00:00:00' 帧
    filter_list = filter_dirty_frame(sorted_list, gap=1)
    video_info(video_clip)
    # 分割视频与音频
    # for i, clip in enumerate(filter_list):
    for i in range(1, len(filter_list)):
        save_segment(filter_list[i - 1]['idx'], filter_list[i]['idx'], video_clip.fps, filter_list[i]['suffix'])

if __name__ == '__main__':
    filter_list = [
        {'idx': 0,     'time': '00:00:00:00', 'suffix': 'C109-P1'},
        {'idx': 9852,  'time': '00:00:04:00', 'suffix': 'C109-P2'},
        {'idx': 10087, 'time': '00:00:00:00', 'suffix': 'SC126'},
        {'idx': 10199, 'time': '00:00:00:00', 'suffix': 'SC127'},
        {'idx': 10315, 'time': '00:00:00:00', 'suffix': 'SC128'},
        {'idx': 10468, 'time': '00:00:00:00', 'suffix': 'SC129'},
        {'idx': 10540, 'time': '00:00:00:00', 'suffix': 'SC131'},
        {'idx': 10625, 'time': '00:00:00:00', 'suffix': 'SC132'}
    ]
    video_info(video_clip)
    # 分割视频与音频
    # for i, clip in enumerate(filter_list):
    for i in range(1, len(filter_list)):
        save_segment(filter_list[i - 1]['idx'], filter_list[i]['idx'], video_clip.fps, filter_list[i]['suffix'])
