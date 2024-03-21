from datetime import datetime

from PyQt5.QtGui import QIcon

from tool.ipTool import get_IPv4_path
from tool.proxyTool import get_local_proxy_windows, get_agent_status
from tool.strTool import get_package_icon_path


def set_proxy_server_info_label(label):
    """
    修改代理服务器label内容
    """
    server, port = get_local_proxy_windows()
    label.setText(f"代理服务器信息: {server}:{port}")


def set_ipv4_add_str_label(label):
    """
    修改显示IPv4地址label内容
    """
    ipv4_add = get_IPv4_path()
    label.setText(f"本机IPv4地址: {ipv4_add}")


def set_agent_state_label(label):
    """
    修改代理状态的label内容
    """
    state = get_agent_status()
    label.setText(f'当前代理状态：{state}')


def set_refresh_btn_label(label):
    """
    修改刷新时间的label内容
    """
    curr_time = datetime.now()
    refresh_time = curr_time.strftime("%H:%M:%S")
    show_time_str = f'刷新：{refresh_time}.{curr_time.microsecond // 1000}'
    label.setText(show_time_str)
    label.setIcon(QIcon(get_package_icon_path('')))
