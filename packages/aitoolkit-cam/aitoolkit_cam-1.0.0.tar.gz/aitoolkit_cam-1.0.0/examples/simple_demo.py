#!/usr/bin/env python3
"""
精简摄像头演示 - 专为中学生设计
==============================

这个示例展示了最简单的使用方法：
1. 创建Camera对象（自动检测摄像头）
2. 启动Web服务器
3. 使用for循环获取帧
4. 显示到Web浏览器

专为ARM64+Armbian系统优化
适合中学生学习编程使用
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from aitoolkit_cam import Camera

def main():
    """主演示函数"""
    print("🎓 中学生摄像头演示 - 精简版")
    print("=" * 50)
    
    try:
        # 第1步：创建摄像头对象（零配置！）
        print("📷 正在初始化摄像头...")
        cam = Camera(source=0, auto_stop_frames=500)  # 无客户端时500帧后自动停止
        
        # 第2步：启动Web服务
        print("🚀 启动Web服务...")
        url = cam.start()
        
        print(f"\n✅ 启动成功！")
        print(f"🌐 浏览器访问: {url}")
        print(f"📱 手机也可以访问这个网址")
        print(f"⏹️  按 Ctrl+C 停止程序")
        print("-" * 50)
        
        # 第3步：视频流处理
        frame_count = 0
        with cam:  # 使用上下文管理器，自动清理资源
            for frame in cam:  # 简单的for循环！
                # 显示到Web（自动处理）
                cam.show(frame, mode="web")
                
                # 统计信息
                frame_count += 1
                if frame_count % 30 == 0:  # 每30帧显示一次
                    print(f"📊 已处理 {frame_count} 帧")
                
                # 注意：默认max_frames=50，会自动停止
        
        print("✅ 演示完成！")
        
    except KeyboardInterrupt:
        print("\n👋 用户按下Ctrl+C，程序退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n💡 故障排除:")
        print("   1. 检查摄像头是否正确连接")
        print("   2. 确认用户有摄像头访问权限")
        print("   3. 检查端口9000是否被占用")
        if sys.platform.startswith('linux'):
            print("   4. ARM64系统检查: ls /dev/video*")
            print("   5. 驱动检查: lsmod | grep uvcvideo")

def advanced_demo():
    """进阶演示：添加图像处理"""
    print("\n🎓 进阶演示：图像处理")
    print("=" * 30)
    
    try:
        import cv2
        
        # 无帧数限制的演示
        with Camera(max_frames=None) as cam:  # 无限制运行
            url = cam.start()
            print(f"🌐 访问地址: {url}")
            print("💡 这次会一直运行，按Ctrl+C停止")
            
            for frame in cam:
                # 添加简单的文字（中学生喜欢的功能）
                cv2.putText(frame, "Hello Camera!", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 也可以添加其他效果：
                # 灰度: gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 边缘: edges = cv2.Canny(frame, 50, 150)
                
                cam.show(frame, mode="web")
                
    except KeyboardInterrupt:
        print("\n👋 进阶演示结束")
    except Exception as e:
        print(f"❌ 进阶演示失败: {e}")

if __name__ == "__main__":
    # 基础演示
    main()
    
    # 如果想尝试进阶功能，可以取消注释
    # print("\n" + "="*50)
    # advanced_demo() 