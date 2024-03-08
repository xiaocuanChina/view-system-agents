import socket


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # 设置超时时间
    try:
        sock.connect((ip, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()


# 扫描局域网内的所有可能的IP地址
# for i in range(1, 255):
ip = f"192.168.1.{i}"  # 假设你的局域网的IP地址范围是192.168.1.1到192.168.1.254
if scan_port(ip, 80):  # 假设你想要扫描的端口是80
    print(f"{ip} is open on port 80")
