import socket


def get_IPv4_path():
    """
        获取本机IP
    :return: 本机IPv4地址
    """
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
