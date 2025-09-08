import concurrent.futures
import os

from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.web_page import WebPage

VIDEO_ID = '114272'  # todo 1.视频id
video_line = ''  # todo 2.视频线路,可以为空，需要‘/56’

url_index = 'https://shasha.one/v/' + VIDEO_ID
video_index = 'https://shasha.one/' + VIDEO_ID + '/'
path = '/Users/anubis/PycharmProjects/python-project/drission-page/shasha/' + VIDEO_ID + '.txt'
video_path = '/Users/anubis/PycharmProjects/python-project/drission-page/shasha/' + VIDEO_ID
episode_map = {}


# 获取所有集的m3u8地址
def get_video_m3u8():
    co = ChromiumOptions().set_browser_path(r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    co.incognito()  # 匿名模式
    # co.headless(True)  # 无头模式
    co.set_argument('--no-sandbox')
    co.ignore_certificate_errors()  # 不校验证书
    page = WebPage(chromium_options=co)
    page.set.load_mode.none()
    page.get(url_index)
    items = page.eles('xpath://a[@class="seq border "]')
    episode_length = items.__len__()
    # episode_length = 1
    # episode_length = [2,3,4,5,6,7,8,9,11]    # todo 1.自定义集数，打开注释2，3

    def fetch_m3u8(id):

        # url = video_index + str(id) + video_line # todo 3.自定义集数
        url = video_index + str(id + 1) + video_line

        tab = page.new_tab(url)
        tab.listen.start(targets='.m3u8', method='GET')  # 开启监听验证码请求抓包
        # tab.listen.start(targets='cdn.wlcdn88.com', method='GET')  # 开启监听验证码请求抓包
        m3u8 = tab.listen.wait()  # 抓取m3u8请求
        m3u8_url = m3u8.url
        tab.stop_loading()
        tab.close()
        return id, m3u8_url

    # 设置线程池参数，最大线程数为10
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # future_to_id = {executor.submit(fetch_m3u8, id): id for id in episode_length} # todo 2.自定义集数
        future_to_id = {executor.submit(fetch_m3u8, id): id for id in range(episode_length)}
        for future in concurrent.futures.as_completed(future_to_id):
            id = future_to_id[future]
            try:
                episode_id, m3u8_url = future.result()
                episode_map[episode_id] = m3u8_url
            except Exception as exc:
                print(f'{id} generated an exception: {exc}')

    sorted_episode_map = dict(sorted(episode_map.items()))
    print(sorted_episode_map)
    with open(path, 'w') as f:
        for episode_id, m3u8_url in sorted_episode_map.items():
            f.write(f'{episode_id}: {m3u8_url}\n')


def download_video(use_N_m3u8DL_RE=True):
    import subprocess
    import concurrent.futures

    # 创建文件目录
    os.makedirs(video_path, exist_ok=True)

    def download_m3u8(episode_id, m3u8_url):
        output_file = f"{video_path}/{episode_id}_{VIDEO_ID}.mp4"
        command = f"ffmpeg -i {m3u8_url} -c copy {output_file}"
        # command = f"ffmpeg -i {m3u8_url} -map 0 -c copy {output_file}"
        subprocess.run(command, shell=True)

    def download_N_m3u8DL_RE(episode_id, m3u8_url):
        savepath = f"{video_path}"
        filename = f"{episode_id}_{VIDEO_ID}.mp4"
        command = f"/Users/anubis/PycharmProjects/python-project/drission-page/shasha/N_m3u8DL-RE \"{m3u8_url}\" --save-dir {savepath} --save-name {filename}"
        subprocess.run(command, shell=True)

    with open(path, 'r') as f:
        episode_map = {int(line.split(': ')[0]): line.split(': ')[1].strip() for line in f}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        if use_N_m3u8DL_RE:
            future_to_id = {executor.submit(download_N_m3u8DL_RE, episode_id, m3u8_url): episode_id for episode_id, m3u8_url in
                            episode_map.items()}
        else:
            future_to_id = {executor.submit(download_m3u8, episode_id, m3u8_url): episode_id for episode_id, m3u8_url in
                            episode_map.items()}
        for future in concurrent.futures.as_completed(future_to_id):
            id = future_to_id[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{id} generated an exception: {exc}')


def merge_video():
    import os
    import subprocess

    # 获取所有视频文件并排序
    video_files = [f for f in os.listdir(video_path) if f.endswith('.mp4')]
    video_files.sort(key=lambda x: int(x.split('_')[0]))  # 按照ID排序

    # 创建一个临时文件来存储视频文件列表
    with open('video_list.txt', 'w') as f:
        for video_file in video_files:
            f.write(f"file '{os.path.join(video_path, video_file)}'\n")

    # 使用ffmpeg合并视频
    output_file = f"{video_path}/merged_{VIDEO_ID}.mp4"
    command = f"ffmpeg -f concat -safe 0 -i video_list.txt -c copy {output_file}"
    subprocess.run(command, shell=True)

    # 删除临时文件
    os.remove('video_list.txt')


if __name__ == '__main__':
    # get_video_m3u8()
    download_video(use_N_m3u8DL_RE=True)
    # merge_video()
