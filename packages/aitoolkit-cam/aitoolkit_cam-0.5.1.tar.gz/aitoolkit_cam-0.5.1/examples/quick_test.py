import cv2
import argparse
import os
from aitoolkit_base import FaceDetector
import time

# 默认图片路径
DEFAULT_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "face_test.jpg")

def run_on_image(detector, image_path):
    """在静态图片上运行人脸检测"""
    if not os.path.exists(image_path):
        print(f"错误: 图像文件 '{image_path}' 不存在。")
        print(f"请将测试图片放置在 `examples/images/` 目录下，并命名为 `face_test.jpg`，或通过 --input 参数指定路径。")
        return

    image = cv2.imread(image_path)
    
    print("正在检测人脸...")
    results = detector.run(image)
    
    if results:
        print(f"检测到 {len(results)} 张人脸。")
        vis_image = detector.draw(image, results)
        
        cv2.imshow("Face Detection Result", vis_image)
        print("按任意键退出。")
        cv2.waitKey(0)
    else:
        print("未检测到人脸。")
    
    cv2.destroyAllWindows()

def run_on_window(detector):
    """在本地窗口上运行人脸检测"""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("错误：无法打开摄像头。")
        return

    print("启动实时人脸检测... 按 'q' 键退出。")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.run(frame)
        vis_frame = detector.draw(frame, results)
        
        cv2.imshow("Real-time Face Detection", vis_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def run_on_web(detector):
    """使用 aitoolkit-cam 在网页上运行人脸检测"""
    try:
        from aitoolkit_cam import Camera
    except ImportError:
        print("错误: aitoolkit-cam 未安装。请运行 'pip install aitoolkit-cam' 或 'pip install .[cam]'。")
        return

    # 启用web_enabled=True以启动Web服务，设置max_frames=None禁用自动停止
    cam = Camera(web_enabled=True, max_frames=None)
    # 启动摄像头和Web服务，并获取URL
    url = cam.start()
    
    if not url:
        print("错误: 启动摄像头或Web服务失败。请检查日志。")
        return
        
    print(f"摄像头已启动，请在浏览器中访问: {url}")
    print("在Jupyter中，此单元格将持续运行。在终端中，您可以按 Ctrl+C 停止。")

    try:
        last_timestamp = 0  # 记录上次处理的时间戳
        
        for frame in cam:
            # 智能时间戳控制：确保时间戳单调递增
            current_time = time.time_ns() // 1_000_000  # 转换为毫秒
            if current_time <= last_timestamp:
                current_time = last_timestamp + 1  # 至少比上次晚1毫秒
            last_timestamp = current_time
            
            # 对帧进行人脸检测
            results = detector.run(frame)
            # 将结果绘制在帧上
            vis_frame = detector.draw(frame, results)
            
            # 通过cam.show()在网页上显示处理后的帧，并指定 mode='web'
            cam.show(vis_frame, mode='web')
            
            # 轻微延迟，确保不会过快处理帧
            time.sleep(0.01)  # 10ms延迟，确保时间戳间隔
            
    except KeyboardInterrupt:
        print("\n用户中断，正在停止服务...")
    finally:
        cam.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1. 人脸检测 (Face Detection)")
    parser.add_argument(
        '--input', 
        type=str, 
        default='window',
        help="输入源。可以是 'window' (本地窗口), 'web' (网页) 或图像文件路径。"
    )
    args = parser.parse_args()

    # 初始化检测器
    detector = FaceDetector()

    if args.input == 'window':
        run_on_window(detector)
    elif args.input == 'web':
        run_on_web(detector)
    else:
        image_path = args.input if os.path.exists(args.input) else DEFAULT_IMAGE_PATH
        run_on_image(detector, image_path)
    
    detector.close() 