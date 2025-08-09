import socket


def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except:
        return None


if __name__ == '__main__':
    print(get_local_ip())
