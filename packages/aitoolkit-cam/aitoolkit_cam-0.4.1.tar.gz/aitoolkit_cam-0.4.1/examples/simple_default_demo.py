#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单默认演示
============

这是 AIToolkit Camera 最简单的演示，展示如何用最少的代码启动摄像头。

运行方式：
    python simple_default_demo.py

特点：
- 最少代码
- 自动资源管理
- 安全退出
"""

from aitoolkit_cam import Camera
import atexit

def main():
    """主演示函数"""
    print("🚀 AIToolkit Camera 简单演示")
    print("=" * 30)
    
    try:
        # 使用 with 语句自动管理摄像头资源
        with Camera() as cam:
            print("📹 摄像头已启动")
            print("🎮 按 'q' 键退出，或等待200帧后自动停止")
            
            # 循环读取并显示每一帧
            for frame in cam:
                # 调用 show(frame) 来显示图像
                # 如果用户按 'q'，show会返回True，从而中断循环
                if cam.show(frame):
                    break
            
        print("\n✅ 演示完成")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        print("💡 请检查：")
        print("  1. 摄像头是否连接")
        print("  2. 摄像头是否被其他程序占用")
        print("  3. 权限是否正确")

if __name__ == "__main__":
    main() 