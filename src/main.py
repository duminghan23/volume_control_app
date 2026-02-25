#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音量控制托盘应用程序
"""

import sys
from PyQt5.QtWidgets import QApplication
from tray_app import SystemTrayApp
from volume_controller import VolumeController


def main():
    app = QApplication(sys.argv)
    
    # 创建系统托盘应用
    tray_app = SystemTrayApp()
    
    # 启动音量控制监听
    volume_controller = VolumeController()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
