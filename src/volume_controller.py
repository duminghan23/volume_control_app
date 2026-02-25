#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音量控制核心逻辑模块 - 使用系统API控制音量
"""

import keyboard
import ctypes


class VolumeController:
    def __init__(self):
        try:
            # 初始化系统API
            self._init_system_api()
            print("系统音量控制器初始化成功")
            
            # 启动键盘监听
            self.start_listening()
            
        except Exception as e:
            print(f"系统音量控制器初始化失败: {e}")
            raise
    
    def _init_system_api(self):
        """初始化系统API"""
        # Windows API常量
        self.VK_VOLUME_MUTE = 0xAD
        self.VK_VOLUME_DOWN = 0xAE
        self.VK_VOLUME_UP = 0xAF
        
        # 加载user32.dll
        self.user32 = ctypes.windll.user32
    
    def _send_volume_message(self, vk_code):
        """发送音量控制消息"""
        # 使用keybd_event模拟按键
        self.user32.keybd_event(vk_code, 0, 0, 0)  # 按下
        self.user32.keybd_event(vk_code, 0, 2, 0)  # 释放
    
    def toggle_mute(self):
        """切换静音状态 - 使用系统API"""
        try:
            self._send_volume_message(self.VK_VOLUME_MUTE)
            print("系统静音状态已切换")
            return True
        except Exception as e:
            print(f"切换静音状态失败: {e}")
            return None
    
    def increase_volume(self):
        """增加音量 - 使用系统API"""
        try:
            self._send_volume_message(self.VK_VOLUME_UP)
            print("系统音量已增加")
            return True
        except Exception as e:
            print(f"增加音量失败: {e}")
            return None
    
    def decrease_volume(self):
        """降低音量 - 使用系统API"""
        try:
            self._send_volume_message(self.VK_VOLUME_DOWN)
            print("系统音量已降低")
            return True
        except Exception as e:
            print(f"降低音量失败: {e}")
            return None
    
    def start_listening(self):
        """启动键盘监听"""

        # 注册热键组合
        def on_alt_delete():
            self.toggle_mute()

        def on_alt_home():
            self.increase_volume()

        def on_alt_end():
            self.decrease_volume()

        # 监听热键组合
        keyboard.add_hotkey(hotkey='alt+delete', callback=on_alt_delete)
        keyboard.add_hotkey(hotkey='alt+home', callback=on_alt_home)
        keyboard.add_hotkey(hotkey='alt+end', callback=on_alt_end)

        print("音量控制器已启动，正在监听键盘事件...")
