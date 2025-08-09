import os
import hashlib
import zlib
import paramiko
from concurrent.futures import ThreadPoolExecutor
import time
import queue

def create_sftp_connection(hostname, port, username, password):
    """创建一个SFTP连接"""
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def close_sftp_connection(sftp):
    """关闭SFTP连接"""
    sftp.close()
    sftp.get_channel().get_transport().close()

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

def check_file_integrity(sftp_pool, remote_item_path, local_item_path, type='md5'):
    """检查文件完整性"""
    remote_file_size = sftp_pool.get().stat(remote_item_path).st_size
    local_file_size = os.path.getsize(local_item_path)

    if remote_file_size == local_file_size:
            if type == 'size':
                print(f"正在计算文件size值: {local_item_path}...")
                future_remote = calculate_size_from_sftp(sftp_pool.get(), remote_item_path)
                future_local = calculate_size(local_item_path)
            elif type == 'md5':
                print(f"正在计算文件MD5值: {local_item_path}...")
                future_remote = calculate_md5_from_sftp(sftp_pool.get(), remote_item_path)
                future_local = calculate_md5(local_item_path)
            elif type == 'sha1':
                print(f"正在计算文件SHA1值: {local_item_path}...")
                future_remote = calculate_sha1_from_sftp(sftp_pool.get(), remote_item_path)
                future_local = calculate_sha1(local_item_path)
            elif type == 'crc32':
                print(f"正在计算文件CRC32值: {local_item_path}...")
                future_remote = calculate_crc32_from_sftp(sftp_pool.get(), remote_item_path)
                future_local = calculate_crc32(local_item_path)


            remote = future_remote.result()
            local = future_local.result()

            # 将使用的SFTP连接放回池中
            sftp_pool.put(future_remote._args[0])
            sftp_pool.put(future_local._args[0])

            if remote == local:
                print(f"文件 {local_item_path} 已存在且完整，跳过下载。")
                return True
    return False

def download_file(sftp_pool, remote_item_path, local_item_path):
    """下载单个文件"""
    try:
        if os.path.exists(local_item_path):
            if check_file_integrity(sftp_pool, remote_item_path, local_item_path, 'size'):
                return

        # 获取SFTP连接
        sftp = sftp_pool.get()

        # 下载文件
        print(f"开始下载文件: {remote_item_path} 到 {local_item_path}")
        sftp.get(remote_item_path, local_item_path)
        print(f"文件 {remote_item_path} 已下载到 {local_item_path}。")

        # 将使用的SFTP连接放回池中
        sftp_pool.put(sftp)
    except KeyboardInterrupt:
        print("下载任务被用户中断。")
    except Exception as e:
        print(f"下载文件 {remote_item_path} 时出错: {e}")

def download_sftp_folder(sftp_pool, remote_path, local_path):
    """递归下载SFTP文件夹内容"""
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # 获取SFTP连接
    sftp = sftp_pool.get()

    items = sftp.listdir_attr(remote_path)
    files_to_download = []

    print(f"开始处理目录: {remote_path}")

    for item in items:
        remote_item_path = os.path.join(remote_path, item.filename)
        local_item_path = os.path.join(local_path, item.filename)

        if S_ISDIR(item.st_mode):
            # 如果是目录，递归下载
            print(f"递归处理目录: {remote_item_path}")
            download_sftp_folder(sftp_pool, remote_item_path, local_item_path)
        else:
            # 如果是文件，添加到下载队列
            files_to_download.append((sftp_pool, remote_item_path, local_item_path))

    # 将使用的SFTP连接放回池中
    sftp_pool.put(sftp)

    # 使用线程池下载文件
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            print(f"开始下载文件，共 {len(files_to_download)} 个文件")
            executor.map(lambda args: download_file(*args), files_to_download)
    except KeyboardInterrupt:
        print("线程池任务被用户中断。")

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
    remote_path = '/data/data/com.termux/files/home/back/file'
    local_path = '/Users/anubis/Downloads'

    # 创建SFTP连接池
    sftp_pool = queue.Queue(maxsize=12)
    for _ in range(sftp_pool.maxsize):
        sftp_pool.put(create_sftp_connection(hostname, port, username, password))

    try:
        download_sftp_folder(sftp_pool, remote_path, local_path)
    finally:
        # 关闭所有SFTP连接
        while not sftp_pool.empty():
            close_sftp_connection(sftp_pool.get())

    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time  # 计算总耗时
    print(f"总耗时: {total_time:.2f} 秒")

if __name__ == "__main__":
    main()
