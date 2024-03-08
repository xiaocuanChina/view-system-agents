import socket
import winreg

from tool.ipTool import get_IPv4_path


def get_agent_status():
    """
    获得代理状态
    """
    # 获取注册表中的key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
    proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
    winreg.CloseKey(key)
    if proxy_enable == 1:
        return "<span style='color:#51c259;'>开启</span>"
    else:
        return "<span style='color:#fc1e1e;'>关闭</span>"


def set_agent_status(agent_status):
    """
    设置代理状态
    :param agent_status: 代理状态
        - True: 开启代理
        - False: 关闭代理
    :return: None
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
    # 设置状态
    # 打开代理设置的注册表键
    setting_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0,
                                 winreg.KEY_SET_VALUE)
    # 将 ProxyEnable 设置为 1，启用代理
    winreg.SetValueEx(setting_key, 'ProxyEnable', 0, winreg.REG_DWORD, int(agent_status))

    winreg.CloseKey(key)

    return get_agent_status()


def get_local_proxy_windows():
    """
    获取本地使用的代理服务器 IP 和端口 (Windows)

    Returns:
        代理服务器 IP 和端口，例如 ("127.0.0.1", 8080)
    """

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
    try:
        proxy_server, proxy_enable = winreg.QueryValueEx(key, "ProxyServer")
        if proxy_enable == 1:
            server_and_port_info = proxy_server.split(":")
            server = server_and_port_info[0]
            port = server_and_port_info[1]
            return server, port
    finally:
        winreg.CloseKey(key)


