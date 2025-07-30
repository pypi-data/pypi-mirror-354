#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单默认演示
============

这是 AIToolkit Camera 最简单的演示，展示了如何用最少的代码启动摄像头并在本地窗口显示。

运行方式：
    python examples/simple_default_demo.py
"""

from aitoolkit_cam import Camera

def main():
    """主演示函数"""
    print("🚀 AIToolkit Camera 简单默认演示")
    print("=" * 40)
    
    try:
        # 使用 'with' 语句自动管理摄像头资源
        with Camera() as cam:
            print("📹 摄像头已启动 (默认Jupyter模式, 50帧后自动停止)")
            print("👉 在弹出的窗口中按 'q' 键可提前退出。")
            
            # 循环读取并显示每一帧
            for frame in cam:
                # 调用 show(frame) 来显示图像
                # 如果用户按 'q'，show会返回True，从而中断循环
                if cam.show(frame, window_name="默认演示"):
                    break
            
        print("\n✅ 演示完成。")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        print("💡 请检查：")
        print("  1. 摄像头是否已连接且未被其他程序占用。")
        print("  2. 驱动是否正确安装。")

if __name__ == "__main__":
    main() 