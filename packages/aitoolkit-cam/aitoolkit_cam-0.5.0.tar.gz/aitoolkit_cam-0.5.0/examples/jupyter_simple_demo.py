#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jupyter 超简单演示
================

展示如何使用 en_jupyter 模式让摄像头编程变得安全简单。

使用方法：
    在 Jupyter Notebook 中运行以下任意代码块
"""

from aitoolkit_cam import Camera

def demo_basic():
    """最基础的演示"""
    print("🎨 基础演示")
    # 使用with语句，自动管理资源，显示50帧后停止
    with Camera(max_frames=50) as cam:
        for frame in cam:
            if cam.show(frame, window_name="基础演示"):
                break

def demo_custom_frames():
    """自定义帧数演示"""
    print("🎮 自定义帧数演示") 
    # 显示100帧
    with Camera(max_frames=100) as cam:
        for frame in cam:
            if cam.show(frame, window_name="自定义帧数演示"):
                break

def demo_with_effect():
    """带效果的演示"""
    print("🎨 效果演示")
    
    import cv2
    
    def gray_effect(frame):
        """灰度效果"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    # 默认Jupyter模式 + 效果
    with Camera() as cam:
        for frame in cam:
            # 应用效果
            processed_frame = gray_effect(frame)
            if cam.show(processed_frame, window_name="灰度效果演示"):
                break

def demo_one_liner():
    """一行代码演示"""
    print("⚡ 一行代码演示")
    # 简洁的写法
    with Camera() as cam:
        for frame in cam:
            if cam.show(frame, window_name="一行代码演示"):
                break

# 对比：传统方式 vs Jupyter模式
def compare_modes():
    """对比不同模式"""
    print("📊 模式对比")
    
    print("\n传统模式（需要手动退出）：")
    print("with Camera(en_jupyter=False) as cam:")
    print("    for frame in cam:")
    print("        if cam.show(frame): break")
    
    print("\nJupyter模式（现在是默认模式, 自动退出）：")
    print("with Camera() as cam:")
    print("    for frame in cam:")
    print("        if cam.show(frame): break")

# 使用说明
if __name__ != "__main__":
    print("🎬 Jupyter 超简单演示已加载")
    print("📖 可用函数：")
    print("  • demo_basic()        - 基础演示")
    print("  • demo_custom_frames() - 自定义帧数")  
    print("  • demo_with_effect()  - 带效果演示")
    print("  • demo_one_liner()    - 一行代码演示")
    print("  • compare_modes()     - 模式对比")
    print()
    print("🚀 快速开始（现在更简单）：")
    print("  Camera().show()")

if __name__ == "__main__":
    print("🧪 运行基础演示...")
    demo_basic() 