# volume_control_app
一款简易的键盘控制系统音量的工具
运行图片：

<img width="271" height="160" alt="image" src="https://github.com/user-attachments/assets/65b8ffe7-0442-402b-ab8c-5b40ed70a0cf" />

<img width="215" height="113" alt="image" src="https://github.com/user-attachments/assets/67b9393d-cbb1-4619-9117-d26806daf7c0" />

# 音量控制托盘程序

## 项目结构

```
volume_control_app/
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── volume_controller.py # 音量控制核心逻辑
│   └── tray_app.py        # 系统托盘GUI
├── assets/                # 资源文件目录
│   └── icon.ico          # 托盘图标文件（需要手动添加）
├── build/                 # 构建输出目录
│   └── build.py          # Nuitka构建脚本
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明文档
```

## 功能特性

- 🎵 系统托盘运行，不占用桌面空间
- 🔇 Alt+Delete 切换系统静音状态
- 🔊 Alt+Home 增加音量3%
- 🔉 Alt+End 降低音量3%
- 🖱️ 右键托盘图标可退出程序
- ⚡ 支持开机自启功能（右键菜单设置）

## 使用方法

### 开发环境运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
cd src
python main.py
```

### 打包成可执行文件
```bash
# 使用构建脚本，有两个build文件，使用的两个不同的打包方案，测试的时候均可以使用
cd build
python build.py
```

## 快捷键说明

| 快捷键 | 功能 |
|--------|------|
| win+- | 切换静音/取消静音 |
| win+Plus | 增加音量3% |
| win+Home | 降低音量3% |

## 托盘菜单功能

右键点击系统托盘图标：
- **显示状态** - 显示程序运行状态
- **开机自启** - ✓ 勾选启用开机自动启动程序
- **退出** - 完全退出程序

## 注意事项

1. 程序需要管理员权限才能正常控制系统音量
2. 打包后的exe文件会生成在 `build` 目录中
3. 如需自定义图标，请将icon.ico文件放入assets目录
4. 开机自启功能会将程序路径写入Windows注册表
5. 程序支持开发环境和打包后环境的开机自启设置
