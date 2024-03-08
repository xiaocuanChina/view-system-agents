import os
import sys

from PyQt5.QtGui import QGuiApplication


def get_package_icon_path(path):
    if getattr(sys, 'frozen', False):
        # 如果是PyInstaller打包的程序
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行的脚本
        base_path = os.path.abspath(".")

    icon_path = os.path.join(base_path, path)
    return icon_path


def copy_str(s):
    # 获取剪贴板实例
    clipboard = QGuiApplication.clipboard()
    # 设置剪贴板内容
    clipboard.setText(s)


def split_string_by_length(input_str, length):
    result = [input_str[i:i + length] for i in range(0, len(input_str), length)]
    return '\n'.join(result)


if __name__ == '__main__':
    s = "复制的代理服务器地址仅在本机使用，如果需要获取局域网内可使用的服务器ip以及端口以及ip请查看自己代理软件的配置以及对应端口"
    print(split_string_by_length(s, 8))
