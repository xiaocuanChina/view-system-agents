from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QToolTip, QLineEdit

from tool.LabelTool import set_proxy_server_info_label, set_ipv4_add_str_label, set_agent_state_label, \
    set_refresh_btn_label
from tool.ipTool import get_IPv4_path
from tool.strTool import *
from tool.proxyTool import *


class MyWindow(QWidget):
    # logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self):
        super().__init__()

        self.edit_server_btn = None
        self.show_text_edit = None
        self.separate_text_edit = None
        self.port_text_edit = None
        self.server_text_edit = None
        self.ipv4_add_str = None
        self.proxy_server_info_str = None
        self.copy_server_btn = None
        self.refresh_btn = None
        self.copy_ip_btn = None
        self.agent_state = None
        self.refresh_time = None
        self.windows_top_btn = None

        # 获取主屏幕对象
        screen = QGuiApplication.primaryScreen()
        # 从主屏幕对象获取屏幕几何信息(包括屏幕分辨率)
        screen_geometry = screen.geometry()
        # 从屏幕几何信息中获取屏幕宽度
        screen_width = screen_geometry.width()
        # 从屏幕几何信息中获取屏幕高度
        screen_height = screen_geometry.height()

        # 窗口宽度
        self.WIDGET_WIDTH = 360
        # 窗口高度
        self.WIDGET_HEIGHT = 120
        # 窗口默认x轴
        self.WINDOW_X = (screen_width - self.WIDGET_WIDTH) // 2
        # 窗口默认y轴
        self.WINDOW_Y = (screen_height - self.WIDGET_HEIGHT) // 2
        # 设置标题
        self.TITLE = '系统代理信息'
        # 文本宽度（一行数量）
        self.TEXT_WIDTH = 17

        # 设置窗口的基本属性
        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WIDGET_WIDTH, self.WIDGET_HEIGHT)
        self.setWindowTitle(self.TITLE)

        self.initUI()

    def initUI(self):

        # 构建网络代理.png的绝对路径
        window_icon_path = get_package_icon_path("image/网络代理.png")
        self.setWindowIcon(QIcon(window_icon_path))

        # 禁用最小化、最大化和关闭按钮
        # self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        ipv4_add = get_IPv4_path()
        self.ipv4_add_str = QLabel(f"本机IPv4地址: {ipv4_add}", self)

        # 代理服务器信息
        # 如何配置代理服务器喝配置代理服务器的分别显示见【刷新按钮】附近的if判断
        # ------- 代理服务器信息 -------
        local_server, local_port = get_local_proxy_windows()
        self.proxy_server_info_str = QLabel(f"代理服务器信息: {local_server}:{local_port}", self)
        self.copy_server_btn = QPushButton('复制本地地址', self)
        tip_str = "复制的代理服务器地址仅在本机使用，如果需要获取局域网内可使用的服务器ip以及端口请查看自己代理软件的配置对应端口"
        self.copy_server_btn.setToolTip(split_string_by_length(tip_str, self.TEXT_WIDTH))
        self.copy_server_btn.setIcon(QIcon(get_package_icon_path('image/复制.png')))  # 替换为你的图标文件路径
        self.copy_server_btn.clicked.connect(self.copy_proxy_server_address)
        self.edit_server_btn = QPushButton('调整代理服务器', self)
        self.edit_server_btn.setIcon(QIcon(get_package_icon_path('image/编辑.png')))  # 替换为你的图标文件路径
        self.edit_server_btn.clicked.connect(self.edit_server_info)

        # ------- 配置代理服务器 -------
        # tip_str = "输入完代理服务器地址之后<span style='color:red;'>点击刷新</span>即可自动为您配置代理服务器地址"
        self.server_text_edit = QLineEdit(self)
        self.server_text_edit.setPlaceholderText("请输入服务器")  # 设置背景文字
        # self.server_text_edit.setToolTip(split_string_by_length(tip_str, self.TEXT_WIDTH))
        self.separate_text_edit = QLabel(f":", self)
        self.port_text_edit = QLineEdit(self)
        self.port_text_edit.setPlaceholderText("请输入端口号")  # 设置背景文字
        # self.port_text_edit.setToolTip(split_string_by_length(tip_str, self.TEXT_WIDTH))

        # self.copy_server_btn = QPushButton('复制局域网', self)
        # self.copy_server_btn.setToolTip('复制（局域网）代理服务器地址到剪贴板')
        # self.copy_server_btn.setIcon(QIcon(get_package_icon_path('image/复制.png')))  # 替换为你的图标文件路径
        # item_copy_str = f"{server}:{port}"
        # self.copy_server_btn.clicked.connect(lambda: self.copy_str(item_copy_str, self.copy_server_btn))

        # IPv4地址信息
        self.copy_ip_btn = QPushButton('一键复制', self)
        self.copy_ip_btn.setToolTip('仅复制IPv4地址')
        self.copy_ip_btn.setIcon(QIcon(get_package_icon_path('image/复制.png')))
        self.copy_ip_btn.clicked.connect(lambda: copy_str(ipv4_add, self.copy_ip_btn))

        # 代理状态
        self.agent_state = QLabel(f'当前代理状态：{get_agent_status()}', self)
        self.refresh_time = QLabel('', self)
        self.refresh_time.hide()

        start_btn = QPushButton('开启代理', self)
        start_btn.setIcon(QIcon(get_package_icon_path('image/开启.png')))  # 替换为你的图标文件路径
        start_btn.clicked.connect(self.button1Clicked)

        stop_btn = QPushButton('关闭代理', self)
        stop_btn.setIcon(QIcon(get_package_icon_path('image/关闭.png')))
        stop_btn.clicked.connect(self.button2Clicked)

        # 功能按钮
        exit_btn = QPushButton('退出', self)
        exit_btn.setIcon(QIcon(get_package_icon_path('image/退出.png')))
        exit_btn.clicked.connect(self.button3Clicked)

        self.refresh_btn = QPushButton('刷新', self)
        self.refresh_btn.setIcon(QIcon(get_package_icon_path('image/刷新.png')))
        self.refresh_btn.clicked.connect(self.refresh)

        self.windows_top_btn = QPushButton('点我置顶', self)
        self.windows_top_btn.setIcon(QIcon(get_package_icon_path('image/置顶-false.png')))
        self.windows_top_btn.clicked.connect(self.set_windows_top)

        if local_server and local_port:
            self.show_text_edit = False
            self.server_text_edit.hide()
            self.port_text_edit.hide()
            self.separate_text_edit.hide()
        else:
            self.show_text_edit = True
            self.refresh_btn.setText("点我保存")
            self.refresh_btn.setIcon(QIcon(get_package_icon_path('image/保存.png')))
            self.proxy_server_info_str.setText("请设置代理服务器信息: ")
            self.copy_server_btn.hide()
            self.edit_server_btn.hide()

        # 创建垂直布局，并将文本标签和按钮添加到布局中
        y_box = QVBoxLayout()

        # ipv4布局
        ipv4_add_x_box = QHBoxLayout()
        ipv4_add_x_box.addWidget(self.ipv4_add_str)
        ipv4_add_x_box.addWidget(self.copy_ip_btn)
        y_box.addLayout(ipv4_add_x_box)

        # 代理服务器信息布局
        proxy_server_x_box = QHBoxLayout()  # 创建水平布局
        proxy_server_x_box.addWidget(self.proxy_server_info_str)
        proxy_server_x_box.addWidget(self.copy_server_btn)
        proxy_server_x_box.addWidget(self.edit_server_btn)

        proxy_server_x_box.addWidget(self.server_text_edit)
        proxy_server_x_box.addWidget(self.separate_text_edit)
        proxy_server_x_box.addWidget(self.port_text_edit)

        y_box.addLayout(proxy_server_x_box)

        # 代理状态布局
        agent_state_x_box = QHBoxLayout()  # 创建水平布局
        agent_state_x_box.addWidget(self.agent_state)
        agent_state_x_box.addWidget(start_btn)
        agent_state_x_box.addWidget(stop_btn)
        y_box.addLayout(agent_state_x_box)

        # 功能按钮布局
        function_but_x_box = QHBoxLayout()  # 创建水平布局
        function_but_x_box.addWidget(self.windows_top_btn)
        function_but_x_box.addWidget(self.refresh_btn)
        function_but_x_box.addWidget(exit_btn)
        y_box.addLayout(function_but_x_box)

        # 设置窗口布局
        self.setLayout(y_box)

    def button1Clicked(self):
        set_agent_status(True)
        self.refresh()

    def button2Clicked(self):
        set_agent_status(False)
        self.refresh()

    def button3Clicked(self):
        self.close()

    def refresh(self):
        """
        刷新的方法
        """
        # 刷新IPv4的地址
        set_ipv4_add_str_label(self.ipv4_add_str)

        # 如果设置代理服务器的文本框内容不为空
        validate_server = self.server_text_edit.text()
        validate_port = self.port_text_edit.text()
        if validate_server and validate_port:
            set_local_proxy_windows(validate_server, validate_port)
            self.server_text_edit.hide()
            self.port_text_edit.hide()
            self.separate_text_edit.hide()

            self.copy_server_btn.show()
            self.edit_server_btn.show()
            # 刷新服务器地址
            set_proxy_server_info_label(self.proxy_server_info_str)

        # 刷新代理状态
        set_agent_state_label(self.agent_state)

        # 设置按钮刷新时间
        set_refresh_btn_label(self.refresh_btn)

    def set_windows_top(self):
        """
        设置窗口置顶
        :return:
        """
        # 获取窗口标志
        flags = self.windowFlags()

        # 检查窗口是否置顶
        if flags & QtCore.Qt.WindowStaysOnTopHint:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, False)
            self.windows_top_btn.setIcon(QIcon(get_package_icon_path('image/置顶-false.png')))
        else:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.windows_top_btn.setIcon(QIcon(get_package_icon_path('image/置顶-true.png')))
        self.show()

    def copy_proxy_server_address(self):
        """
        需要复制的代理服务器地址
        """
        copy_server, copy_port = get_local_proxy_windows()
        proxy_server_address = f"https://{copy_server}:{copy_port}"
        copy_str(proxy_server_address)
        # 更新复制按钮的文本和图标
        self.copy_server_btn.setText("复制成功")
        self.copy_server_btn.setIcon(QIcon(get_package_icon_path('image/成功.png')))

    def edit_server_info(self):
        """
        修改代理服务器配置
        """
        # 核心代码 设置不同组件的显隐藏
        self.copy_server_btn.hide()
        self.edit_server_btn.hide()
        self.server_text_edit.show()
        self.separate_text_edit.show()
        self.port_text_edit.show()

        # 获取默认的代理服务器信息
        default_server, default_port = get_local_proxy_windows()
        self.server_text_edit.setText(default_server)
        self.port_text_edit.setText(default_port)

        # 设置在“修改服务器状态”下的显示的内容
        self.proxy_server_info_str.setText("请设置代理服务器信息: ")
        self.refresh_btn.setText("点我保存")
        self.refresh_btn.setIcon(QIcon(get_package_icon_path('image/保存.png')))
        self.proxy_server_info_str.setText("请设置代理服务器信息: ")
