#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nuitka 打包构建脚本
"""

import os
import subprocess
import sys

def build_executable():
    """使用 Nuitka 构建可执行文件"""
    
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # 上一级目录才是项目根目录
    src_dir = os.path.join(project_root, 'src')
    build_dir = os.path.join(project_root, 'build')
    main_py = os.path.join(src_dir, 'main.py')
    
    # 确保构建目录存在
    os.makedirs(build_dir, exist_ok=True)
    
    print(f"项目根目录: {project_root}")
    print(f"源码目录: {src_dir}")
    print(f"构建目录: {build_dir}")
    print(f"主程序文件: {main_py}")
    
    # 验证主程序文件是否存在
    if not os.path.exists(main_py):
        print(f"错误: 主程序文件不存在: {main_py}")
        return False
    
    # 切换到源码目录执行构建命令
    os.chdir(src_dir)
    print(f"当前工作目录: {os.getcwd()}")

    # Nuitka 构建命令
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--standalone',                    # 独立分发
        '--onefile',                       # 单文件打包
        '--windows-console-mode=disable',  # 禁用控制台窗口
        '--enable-plugin=pyqt5',           # 启用 PyQt5 插件
        '--output-dir=' + build_dir,       # 输出目录
        '--output-filename=VolumeControl', # 输出文件名
        '--company-name=MyCompany',        # 公司名称
        '--product-name=VolumeControl',    # 产品名称
        '--file-version=1.0.0',            # 文件版本
        '--product-version=1.0.0',         # 产品版本
        'main.py'                          # 主程序文件
    ]
    
    print("开始构建可执行文件...")
    print("命令:", ' '.join(cmd))
    
    try:
        # 执行构建命令
        print("正在执行构建命令...")
        result = subprocess.run(cmd, check=True)
        print("构建成功!")
        print("输出目录:", build_dir)
        
        # 查找生成的exe文件
        exe_files = [f for f in os.listdir(build_dir) if f.endswith('.exe')]
        if exe_files:
            print("生成的可执行文件:", exe_files[0])
            
    except subprocess.CalledProcessError as e:
        print("构建失败!")
        print("错误信息:", e.stderr)
        return False
    except Exception as e:
        print("构建过程中发生错误:", str(e))
        return False
    
    return True

def install_dependencies():
    """安装必要的依赖"""
    print("检查并安装依赖...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', '../requirements.txt'], 
                      check=True, capture_output=True)
        print("依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print("依赖安装失败:", e.stderr)
        return False

if __name__ == "__main__":
    print("=== 音量控制程序打包工具 ===")
    
    # 安装依赖
    if not install_dependencies():
        print("依赖安装失败，终止构建")
        sys.exit(1)
    
    # 构建可执行文件
    if build_executable():
        print("\n打包完成! 可执行文件已在 build 目录中生成")
    else:
        print("\n打包失败!")
        sys.exit(1)