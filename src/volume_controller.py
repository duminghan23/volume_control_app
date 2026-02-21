#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音量控制核心逻辑模块
"""

import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        try:
            # 获取系统默认音频设备
            devices = AudioUtilities.GetSpeakers()
            if devices is None:
                raise Exception("无法获取音频设备")
            
            # 新版本pycaw直接使用EndpointVolume属性
            self.volume = devices.EndpointVolume
            
            # 测试连接
            self.volume.GetMute()
            print("音频控制器初始化成功")
            
            # 启动键盘监听
            self.start_listening()
            
        except Exception as e:
            print(f"音频控制器初始化失败: {e}")
            raise
    
    def toggle_mute(self):
        """切换静音状态"""
        try:
            current_mute = self.volume.GetMute()
            self.volume.SetMute(not current_mute, None)
            status = "静音" if not current_mute else "取消静音"
            print(f"系统已{status}")
            return not current_mute
        except Exception as e:
            print(f"切换静音状态失败: {e}")
            return None
    
    def increase_volume(self):
        """增加音量3%"""
        try:
            current_volume = self.volume.GetMasterVolumeLevelScalar()
            new_volume = min(1.0, current_volume + 0.03)  # 增加3%
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"音量已增加至 {int(new_volume * 100)}%")
            return new_volume
        except Exception as e:
            print(f"增加音量失败: {e}")
            return None
    
    def decrease_volume(self):
        """降低音量3%"""
        try:
            current_volume = self.volume.GetMasterVolumeLevelScalar()
            new_volume = max(0.0, current_volume - 0.03)  # 降低3%
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"音量已降低至 {int(new_volume * 100)}%")
            return new_volume
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
        keyboard.add_hotkey('win+delete', on_alt_delete)
        keyboard.add_hotkey('win+home', on_alt_home)
        keyboard.add_hotkey('win+end', on_alt_end)
        
        print("音量控制器已启动，正在监听键盘事件...")