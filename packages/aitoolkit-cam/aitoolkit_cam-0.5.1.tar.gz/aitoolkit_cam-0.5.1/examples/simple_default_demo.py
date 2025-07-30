import argparse
from aitoolkit_cam import Camera

def run_cv2_mode():
    """在本地OpenCV窗口中运行摄像头。"""
    print("🚀 启动本地窗口模式...")
    try:
        # 使用'with'语句可以确保摄像头资源被自动释放
        with Camera() as cam:
            print("✅ 摄像头已启动。在弹出的窗口中按 'q' 键即可退出。")
            
            # cam对象本身就是迭代器，可以轻松获取每一帧
            for frame in cam:
                # show方法会显示帧并检查'q'键是否被按下
                # 如果按下'q'，show返回True，循环中断
                if cam.show(frame, window_name="本地窗口预览 (按q退出)"):
                    break
        
        print("👋 本地窗口模式已关闭。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        print("💡 请检查摄像头是否连接且未被其他程序占用。")

def run_web_mode():
    """在网页浏览器中运行摄像头视频流。"""
    print("🚀 启动网页流模式...")
    try:
        # 启用web模式，设置max_frames=None允许持续运行，Jupyter/headless环境下的理想选择
        with Camera(web_enabled=True, max_frames=None) as cam:
            # start()会启动服务器并返回URL
            url = cam.start()
            print(f"✅ Web服务已启动!")
            print(f"👉 请在浏览器中打开此URL: {url}")
            print(f"ℹ️  按 Ctrl+C 停止服务。")
            print(f"ℹ️  或者，如果关闭浏览器标签页超过30秒，服务也会自动停止。")
            
            # 遍历摄像头的每一帧并推送到Web流
            for frame in cam:
                # 手动将每一帧推送到Web流，这是显示视频的正确方式
                cam.show(frame, mode='web')
                
        print("👋 网页流模式已结束。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="aitoolkit-cam 示例程序。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助文本格式
    )
    parser.add_argument(
        'mode', 
        type=str, 
        choices=['cv2', 'web'],
        help="""运行模式:
  cv2: 在本地OpenCV窗口中显示实时视频。
  web: 通过网页浏览器提供实时视频流。"""
    )
    args = parser.parse_args()

    if args.mode == 'cv2':
        run_cv2_mode()
    elif args.mode == 'web':
        run_web_mode() 