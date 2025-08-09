import os
import hashlib
import zlib

import paramiko
from concurrent.futures import ThreadPoolExecutor
import time  # 导入 time 模块


def calculate_crc32(file_path):
    """计算文件的CRC32值"""
    crc32_value = 0
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            crc32_value = zlib.crc32(chunk, crc32_value)
    return crc32_value & 0xFFFFFFFF


def calculate_crc32_from_sftp(sftp, remote_path):
    """计算SFTP文件的CRC32值"""
    crc32_value = 0
    with sftp.open(remote_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            crc32_value = zlib.crc32(chunk, crc32_value)
    return crc32_value & 0xFFFFFFFF


def calculate_sha1(file_path):
    """计算文件的SHA1值"""
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()


def calculate_sha1_from_sftp(sftp, remote_path):
    """计算SFTP文件的SHA1值"""
    sha1_hash = hashlib.sha1()
    with sftp.open(remote_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()


def calculate_md5(file_path):
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def calculate_md5_from_sftp(sftp, remote_path):
    """计算SFTP文件的MD5值"""
    hash_md5 = hashlib.md5()
    with sftp.open(remote_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def calculate_size(file_path):
    """计算文件的大小值"""
    return os.path.getsize(file_path)

def calculate_size_from_sftp(sftp, remote_path):
    """计算SFTP文件的大小值"""
    return sftp.stat(remote_path).st_size

def check_file_integrity(sftp, remote_item_path, local_item_path, type='md5'):
    """检查文件完整性"""
    remote_file_size = sftp.stat(remote_item_path).st_size
    local_file_size = os.path.getsize(local_item_path)

    if remote_file_size == local_file_size:
        with ThreadPoolExecutor(max_workers=4) as executor:
            if type == 'size':
                print("正在计算文件size值...")
                future_remote = executor.submit(calculate_size_from_sftp, sftp, remote_item_path)
                future_local = executor.submit(calculate_size, local_item_path)
            elif type == 'md5':
                print("正在计算文件MD5值...")
                future_remote = executor.submit(calculate_md5_from_sftp, sftp, remote_item_path)
                future_local = executor.submit(calculate_md5, local_item_path)
            elif type == 'sha1':
                print("正在计算文件SHA1值...")
                future_remote = executor.submit(calculate_sha1_from_sftp, sftp, remote_item_path)
                future_local = executor.submit(calculate_sha1, local_item_path)
            elif type == 'crc32':
                print("正在计算文件CRC32值...")
                future_remote = executor.submit(calculate_crc32_from_sftp, sftp, remote_item_path)
                future_local = executor.submit(calculate_crc32, local_item_path)

            remote = future_remote.result()
            local = future_local.result()

            if remote == local:
                print(f"文件 {local_item_path} 已存在且完整，跳过下载。")
                return True
    return False


def download_sftp_folder(sftp, remote_path, local_path):
    """递归下载SFTP文件夹内容"""
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    for item in sftp.listdir_attr(remote_path):
        remote_item_path = os.path.join(remote_path, item.filename)
        local_item_path = os.path.join(local_path, item.filename)

        if S_ISDIR(item.st_mode):
            # 如果是目录，递归下载
            download_sftp_folder(sftp, remote_item_path, local_item_path)
        else:
            # 如果是文件，检查文件是否存在且完整
            if os.path.exists(local_item_path):
                if check_file_integrity(sftp, remote_item_path, local_item_path, 'size'):
                    continue

            # 下载文件
            sftp.get(remote_item_path, local_item_path)
            print(f"文件 {remote_item_path} 已下载到 {local_item_path}。")


def S_ISDIR(mode):
    """判断是否为目录"""
    import stat
    return stat.S_ISDIR(mode)


def main():
    start_time = time.time()  # 记录开始时间

    hostname = '192.168.1.6'
    port = 8022
    username = 'u0_a373'
    password = '1q2w3e4R!@'
    # remote_path = '/data/data/com.termux/files/home/back/file'
    remote_path = '/data/data/com.termux/files/home/video-hls'
    # local_path = '/Users/anubis/Downloads'
    local_path = '/Users/anubis/Downloads'

    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        download_sftp_folder(sftp, remote_path, local_path)
    finally:
        sftp.close()
        transport.close()

    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time  # 计算总耗时
    print(f"总耗时: {total_time:.2f} 秒")


if __name__ == "__main__":
    main()
# 10 - md5 : 总耗时: 69.32 秒 - 4: 总耗时: 70.94 秒
# 10 - sha1 : 总耗时: 69.46 秒
# 10 - crc32 : 总耗时: 69.68 秒
# 4 - size : 总耗时: 69.68 秒
