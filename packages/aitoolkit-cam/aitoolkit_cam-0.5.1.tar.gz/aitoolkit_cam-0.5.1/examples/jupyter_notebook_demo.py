#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jupyter Notebook 摄像头演示 - 超简版
==================================

专为中学生设计的极简摄像头使用方法。
现在所有核心功能都已经集成到主Camera类中了！

使用方法（只需要这几行）：
```python
from aitoolkit_cam import Camera

# 方法1: 一键测试（最简单）
# 现在默认就是Jupyter模式，直接在循环里show(frame)即可
with Camera(max_frames=50) as cam:
    for frame in cam:
        if cam.show(frame, window_name="一键测试"):
            break

# 方法2: 稍微自定义
with Camera(max_frames=100) as cam:
    for frame in cam:
        if cam.show(frame, window_name="自定义帧数"):
            break
```

就这么简单！不需要其他复杂的设置。
"""

from aitoolkit_cam import Camera

def demo_basic():
    """基础演示"""
    print("📱 基础演示")
    with Camera(max_frames=50) as cam:
        for frame in cam:
            if cam.show(frame, window_name="基础演示"):
                break

def demo_longer():
    """显示更长的时间"""
    print("⏳ 显示更长时间")
    with Camera(max_frames=150) as cam:
        for frame in cam:
            if cam.show(frame, window_name="稍长演示"):
                break

def demo_one_liner():
    """一行代码搞定"""
    print("⚡ 一行代码演示")
    # 严格来说不是一行，但意图是简洁
    with Camera(max_frames=50) as cam:
        for frame in cam:
            if cam.show(frame, window_name="一行代码演示"):
                break
    
# 主程序入口
if __name__ == "__main__":
    print("执行基础演示...")
    demo_basic()
    
    print("\n执行稍长时间的演示...")
    demo_longer()
    
    print("\n执行一行代码演示...")
    demo_one_liner()
    
    print("\n✅ 所有Jupyter演示完成！")

# 导入时显示使用提示
if __name__ != "__main__":
    print("🎬 超简版 Jupyter 摄像头演示已加载")
    print("🚀 一键开始：# 在循环中使用 cam.show(frame)")
    print("📖 可用函数：")
    print("  • demo_one_liner()    - 一行代码演示")
    print("  • demo_basic()    - 基础演示")
    print("  • demo_longer()   - 长时间演示")