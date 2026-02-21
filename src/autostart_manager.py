#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开机自启管理模块
"""

import os
import sys
import winreg
from pathlib import Path

class AutoStartManager:
    def __init__(self):
        self.app_name = "VolumeControl"
        self.registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        
    def get_exe_path(self):
        """获取当前可执行文件路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe文件
            return sys.executable
        else:
            # 开发环境
            return os.path.abspath(sys.argv[0])
    
    def is_autostart_enabled(self):
        """检查是否已设置开机自启"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                current_exe = self.get_exe_path()
                return value == current_exe
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"检查开机自启状态失败: {e}")
            return False
    
    def enable_autostart(self):
        """启用开机自启"""
        try:
            exe_path = self.get_exe_path()
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, exe_path)
            print(f"已设置开机自启: {exe_path}")
            return True
        except Exception as e:
            print(f"设置开机自启失败: {e}")
            return False
    
    def disable_autostart(self):
        """禁用开机自启"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, self.app_name)
            print("已取消开机自启")
            return True
        except FileNotFoundError:
            # 如果键值不存在，说明已经禁用
            return True
        except Exception as e:
            print(f"取消开机自启失败: {e}")
            return False
    
    def toggle_autostart(self):
        """切换开机自启状态"""
        if self.is_autostart_enabled():
            return self.disable_autostart()
        else:
            return self.enable_autostart()