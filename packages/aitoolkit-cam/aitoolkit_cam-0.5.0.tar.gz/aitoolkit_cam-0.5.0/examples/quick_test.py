#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速摄像头测试脚本
=================

这个脚本演示了 AIToolkit Camera 的基本用法，包括：
1. 摄像头初始化和检测
2. 基本的图像显示
3. 简单的图像效果
4. 安全的资源管理

使用方法：
    python quick_test.py

特性：
- 自动检测可用摄像头
- 安全的资源清理
- 错误处理和恢复
- 实时帧率显示
"""

import sys
import cv2
import time
import atexit
from aitoolkit_cam import Camera

# 全局摄像头变量
cam = None

def cleanup():
    """程序退出时的清理函数"""
    global cam
    if cam is not None:
        print("\n正在清理摄像头资源...")
        cam.stop()
        print("摄像头已安全关闭")

def test_camera_detection():
    """测试摄像头检测功能"""
    print("🔍 检测可用摄像头...")
    
    try:
        camera_count = Camera.get_camera_count()
        print(f"找到 {camera_count} 个可用摄像头")
        
        if camera_count == 0:
            print("❌ 没有找到可用的摄像头设备")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 摄像头检测失败: {e}")
        return False

def test_basic_display():
    """测试基本显示功能"""
    global cam
    
    print("\n📹 启动基本显示测试...")
    
    try:
        # 创建摄像头对象
        cam = Camera(width=640, height=480)
        print(f"摄像头分辨率: {cam.width}x{cam.height}")
        
        # 启动摄像头
        if not cam.start():
            print("❌ 摄像头启动失败")
            return False
        
        print("✅ 摄像头启动成功")
        print("🎮 控制说明:")
        print("  - 按 'q' 键退出")
        print("  - 按 'r' 键切换效果")
        print("  - 按 'i' 键显示信息")
        
        frame_count = 0
        start_time = time.time()
        effect_mode = 0  # 0=正常, 1=灰度, 2=边缘检测
        
        # 主循环
        for frame in cam:
            if frame is None:
                continue
            
            frame_count += 1
            
            # 应用效果
            display_frame = frame.copy()
            effect_name = "正常"
            
            if effect_mode == 1:
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)
                effect_name = "灰度"
            elif effect_mode == 2:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                display_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                effect_name = "边缘检测"
            
            # 计算帧率
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                
                # 添加信息叠加
                info_text = f"FPS: {fps:.1f} | 帧数: {frame_count} | 效果: {effect_name}"
                cv2.putText(display_frame, info_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # 显示图像
            cv2.imshow("AIToolkit Camera 测试", display_frame)
            
            # 处理按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n用户退出")
                break
            elif key == ord('r'):
                effect_mode = (effect_mode + 1) % 3
                effects = ["正常", "灰度", "边缘检测"]
                print(f"切换效果: {effects[effect_mode]}")
            elif key == ord('i'):
                print(f"当前状态 - 帧数: {frame_count}, 效果: {effect_name}")
            
            # 限制最大帧数（防止无限循环）
            if frame_count >= 1000:
                print("达到最大帧数限制，自动退出")
                break
        
        return True
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        return True
    except Exception as e:
        print(f"❌ 显示测试失败: {e}")
        return False
    finally:
        # 确保清理资源
        if cam is not None:
            cam.stop()
            cv2.destroyAllWindows()

def test_camera_info():
    """测试摄像头信息获取"""
    global cam
    
    print("\n📊 摄像头信息测试...")
    
    try:
        if cam is None:
            cam = Camera()
        
        # 获取设备信息
        device_info = cam.get_device_info()
        print(f"设备信息: {device_info}")
        
        # 获取状态
        is_running = cam.is_running()
        print(f"运行状态: {'运行中' if is_running else '已停止'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 信息获取失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 AIToolkit Camera 快速测试")
    print("=" * 40)
    
    # 注册清理函数
    atexit.register(cleanup)
    
    # 测试步骤
    tests = [
        ("摄像头检测", test_camera_detection),
        ("基本显示", test_basic_display),
        ("信息获取", test_camera_info),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 执行测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 通过" if result else "❌ 失败"
            print(f"测试结果: {status}")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 40)
    print("📋 测试总结:")
    
    passed = 0
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("🎉 所有测试通过！摄像头工作正常")
    else:
        print("⚠️  部分测试失败，请检查摄像头设置")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行错误: {e}")
    finally:
        # 最终清理
        cleanup()
        print("\n程序结束") 