#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包构建脚本
"""

import os
import subprocess
import sys

def build_with_pyinstaller():
    """使用 PyInstaller 构建可执行文件"""
    
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src_dir = os.path.join(project_root, 'src')
    build_dir = os.path.join(project_root, 'build')
    
    print(f"项目根目录: {project_root}")
    print(f"源码目录: {src_dir}")
    print(f"构建目录: {build_dir}")
    
    # 确保构建目录存在
    os.makedirs(build_dir, exist_ok=True)
    
    # 切换到源码目录
    if not os.path.exists(src_dir):
        print(f"错误: 源码目录不存在: {src_dir}")
        return False
    
    os.chdir(src_dir)
    print(f"当前工作目录: {os.getcwd()}")
    
    # PyInstaller 构建命令
    cmd = [
        'pyinstaller',
        '--onefile',                       # 单文件打包
        '--noconsole',                     # 无控制台窗口
        '--windowed',                      # 窗口模式
        '--name=VolumeControl',            # 可执行文件名
        '--distpath=' + build_dir,         # 输出目录
        '--workpath=' + os.path.join(build_dir, 'temp'),  # 工作目录
        '--specpath=' + build_dir,         # spec文件目录
        'main.py'                          # 主程序文件
    ]
    
    print("开始使用 PyInstaller 构建...")
    print("命令:", ' '.join(cmd))
    
    try:
        # 执行构建命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PyInstaller 构建成功!")
        print("输出目录:", build_dir)
        
        # 查找生成的exe文件
        dist_dir = os.path.join(build_dir, 'VolumeControl.exe')
        if os.path.exists(dist_dir):
            # 获取文件大小
            file_size = os.path.getsize(dist_dir)
            size_mb = file_size / (1024 * 1024)
            print(f"生成的可执行文件: VolumeControl.exe")
            print(f"文件大小: {size_mb:.2f} MB")
            return True
        else:
            print("未找到生成的可执行文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print("PyInstaller 构建失败!")
        print("错误信息:", e.stderr)
        return False
    except Exception as e:
        print("构建过程中发生错误:", str(e))
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("检查并安装 PyInstaller...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                      check=True, capture_output=True)
        print("PyInstaller 安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print("PyInstaller 安装失败:", e.stderr)
        return False

if __name__ == "__main__":
    print("=== PyInstaller 打包工具 ===")
    
    # 安装 PyInstaller
    if not install_pyinstaller():
        print("PyInstaller 安装失败，终止构建")
        sys.exit(1)
    
    # 构建可执行文件
    if build_with_pyinstaller():
        print("\nPyInstaller 打包完成!")
    else:
        print("\nPyInstaller 打包失败!")
        sys.exit(1)