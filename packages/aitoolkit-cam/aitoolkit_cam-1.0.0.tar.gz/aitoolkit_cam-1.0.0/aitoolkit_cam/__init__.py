"""
AIToolkit Camera - 精简摄像头库 (专为ARM64+Web流优化)
=====================================================

专为中学生设计的极简摄像头库，专注于核心功能：
1. 零配置摄像头检测（ARM64优化）
2. 网页实时流（局域网访问）
3. 简单的for循环API
4. 资源自动管理

快速示例:
```python
from aitoolkit_cam import Camera

# 一行创建摄像头
cam = Camera()

# 一行启动Web服务
url = cam.start()
print(f"浏览器访问: {url}")

# 简单的for循环
with cam:
    for frame in cam:
        cam.show(frame)  # 自动显示到Web
```

专为ARM64设备（树莓派、香橙派等）和Armbian系统优化
"""

# 版本信息
__version__ = '0.5.0'
__author__ = "aitoolkit_cam"

# 导入核心类
from .camera import Camera
from .web_streamer import WebStreamer

# 精简的公共接口
__all__ = [
    'Camera',
    'WebStreamer', 
    'cv_show',
    '__version__',
    '__author__'
]

# 兼容性函数
def cv_show(frame, window_name="Preview", wait_key=1):
    """兼容性函数：显示图像"""
    import cv2
    try:
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(wait_key) & 0xFF
        return key == ord('q') or key == 27
    except:
        print("无法显示图像，可能缺少GUI支持")
        return False 