#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统托盘应用程序模块
"""

import sys
import os
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class SystemTrayApp:
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        self.tray_icon = None
        # 初始化开机自启管理器
        from autostart_manager import AutoStartManager
        self.autostart_manager = AutoStartManager()
        self.setup_tray()
        
    def setup_tray(self):
        """设置系统托盘"""
        try:
            # 获取图标路径
            icon_path = self.get_icon_path()
            
            # 创建系统托盘图标
            self.tray_icon = QSystemTrayIcon()
            
            # 设置图标
            if icon_path and os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
                print(f"使用自定义图标: {icon_path}")
            else:
                # 如果没有图标文件，使用默认图标
                default_icon = self.app.style().standardIcon(QStyle.SP_ComputerIcon)
                self.tray_icon.setIcon(default_icon)
                print("使用系统默认图标")
            
            self.tray_icon.setToolTip('音量控制助手')
            
            # 创建右键菜单
            tray_menu = QMenu()
            
            # 显示状态动作
            status_action = QAction("显示状态", self.app)
            status_action.triggered.connect(self.show_status)
            tray_menu.addAction(status_action)
            
            tray_menu.addSeparator()
            
            # 开机自启选项
            self.autostart_action = QAction("开机自启", self.app)
            self.autostart_action.setCheckable(True)
            self.autostart_action.setChecked(self.autostart_manager.is_autostart_enabled())
            self.autostart_action.triggered.connect(self.toggle_autostart)
            tray_menu.addAction(self.autostart_action)
            
            tray_menu.addSeparator()
            
            # 退出动作
            exit_action = QAction("退出", self.app)
            exit_action.triggered.connect(self.exit_app)
            tray_menu.addAction(exit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
            print("系统托盘已启动")
            
        except Exception as e:
            print(f"系统托盘初始化失败: {e}")
    
    def get_icon_path(self):
        """获取图标文件路径"""
        # 尝试多个可能的图标位置
        current_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(current_dir, '..', 'assets', 'icon.ico'),
            os.path.join(current_dir, 'assets', 'icon.ico'),
            os.path.join(current_dir, 'icon.ico'),
            'icon.ico'
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                return path
        return None
    
    def show_status(self):
        """显示当前状态"""
        # 这里可以添加显示当前音量状态的功能
        self.tray_icon.showMessage(
            "音量控制助手",
            "程序正在运行中...",
            QSystemTrayIcon.Information,
            2000
        )
    
    def toggle_autostart(self):
        """切换开机自启状态"""
        success = self.autostart_manager.toggle_autostart()
        if success:
            # 更新菜单项的勾选状态
            is_enabled = self.autostart_manager.is_autostart_enabled()
            self.autostart_action.setChecked(is_enabled)
            
            # 显示通知
            status_text = "已启用" if is_enabled else "已禁用"
            self.tray_icon.showMessage(
                "音量控制助手",
                f"开机自启{status_text}",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            # 操作失败时恢复原状态
            current_state = self.autostart_manager.is_autostart_enabled()
            self.autostart_action.setChecked(current_state)
    
    def exit_app(self):
        """退出应用程序"""
        print("正在退出程序...")
        if self.tray_icon:
            self.tray_icon.hide()
        QCoreApplication.quit()
