#!/usr/bin/env python3
"""
SimpleWebStream 模块 - 简单的Web视频流实现
不依赖vidgear，使用Flask实现MJPEG流服务器
"""
import threading
import time
import socket
import queue
import cv2
import numpy as np
import logging
from flask import Flask, Response, render_template_string
import sys

# 配置日志
logger = logging.getLogger("aitoolkit_cam.simple_web_stream")
# 不再设置日志级别，让上层决定

class WebStreamer:
    """
    简单的Web视频流服务器
    使用Flask实现MJPEG流，支持局域网访问
    """
    
    def __init__(self, host="0.0.0.0", port=8000):
        """
        初始化SimpleWebStream
        
        参数:
            host: 服务器主机地址，"0.0.0.0"可从网络访问
            port: 服务器端口号
        """
        self.host = host
        self.port = port
        self.is_running = False
        
        # Flask应用
        self.app = Flask(__name__)
        self.app.logger.setLevel(logging.ERROR)  # 减少Flask日志输出
        
        # 帧队列，用于接收来自Camera的帧
        self.frame_queue = queue.Queue(maxsize=10)
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        
        # 客户端计数
        self.client_count = 0
        self.client_lock = threading.Lock()
        
        # 服务器线程
        self.server_thread = None
        
        # 设置路由
        self._setup_routes()
    
    def _setup_routes(self):
        """设置Flask路由"""
        
        @self.app.route('/')
        def index():
            """主页面"""
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Stream</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            width: 100%;
            text-align: center;
        }
        h1 {
            color: #4CAF50;
            margin-bottom: 30px;
        }
        .video-container {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .video-stream {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        .status {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            margin-left: 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        .info {
            background: #333;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            text-align: left;
        }
        .error {
            background: #d32f2f;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>摄像头实时流 <span class="status" id="status"></span></h1>
        
        <div class="video-container">
            <img src="/video" class="video-stream" alt="视频流" id="videoStream">
        </div>
        
        <div class="info">
            <h3>连接信息</h3>
            <p><strong>服务器地址:</strong> {{ request.host }}</p>
            <p><strong>视频流地址:</strong> {{ request.host_url }}video</p>
            <p><strong>状态:</strong> <span id="statusText">连接中...</span></p>
        </div>
    </div>

    <script>
        const video = document.getElementById('videoStream');
        const status = document.getElementById('status');
        const statusText = document.getElementById('statusText');
        
        video.onload = function() {
            status.style.background = '#4CAF50';
            statusText.textContent = '正常运行';
        };
        
        video.onerror = function() {
            status.style.background = '#f44336';
            statusText.textContent = '连接失败';
            // 尝试重新连接
            setTimeout(() => {
                video.src = '/video?' + new Date().getTime();
            }, 2000);
        };
        
        // 定期检查连接状态
        setInterval(() => {
            if (video.complete && video.naturalWidth === 0) {
                video.src = '/video?' + new Date().getTime();
            }
        }, 5000);
    </script>
</body>
</html>
            """
            return render_template_string(html_template)
        
        @self.app.route('/video')
        def video_feed():
            """视频流端点"""
            return Response(
                self._generate_frames(),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )
        
        @self.app.route('/status')
        def status():
            """状态检查端点"""
            return {
                'status': 'running' if self.is_running else 'stopped',
                'has_frame': self.latest_frame is not None,
                'queue_size': self.frame_queue.qsize(),
                'clients': self.get_client_count()
            }
    
    def _generate_frames(self):
        """生成视频帧的生成器"""
        # 增加客户端计数
        with self.client_lock:
            self.client_count += 1
        logger.info(f"新客户端连接，当前客户端数量: {self.client_count}")

        try:
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, 80]
            
            while self.is_running:
                frame = None
                try:
                    # 使用超时来避免永久阻塞，并能响应 is_running 的变化
                    frame = self.frame_queue.get(timeout=1.0)
                except queue.Empty:
                    # 如果队列长时间为空，也检查一下是否应该继续运行
                    if not self.is_running:
                        break
                    # 发送上一帧或占位符
                    with self.frame_lock:
                        frame = self.latest_frame
                        
                if frame is None:
                    frame = self._create_placeholder_frame()

                if frame is None:
                    continue

                # 更新最新帧
                with self.frame_lock:
                    self.latest_frame = frame
                
                try:
                    success, buffer = cv2.imencode('.jpg', frame, encode_params)
                    if not success:
                        logger.warning("帧编码失败")
                        continue
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                    
                except (GeneratorExit, ConnectionResetError, BrokenPipeError):
                    # 这是客户端断开连接的明确信号
                    logger.info("客户端断开连接 (GeneratorExit/ConnectionError)")
                    break
                except Exception as e:
                    logger.error(f"发送帧时发生未知错误: {e}")
                    break
        finally:
            with self.client_lock:
                self.client_count -= 1
            logger.info(f"一个客户端已断开，剩余客户端数量: {self.client_count}")

    def get_client_count(self):
        """获取当前连接的客户端数量"""
        with self.client_lock:
            return self.client_count
    
    def _create_placeholder_frame(self, width=640, height=480):
        """创建占位帧"""
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 添加文字
        text = "Waiting for camera..."
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        
        # 居中显示
        x = (width - text_size[0]) // 2
        y = (height + text_size[1]) // 2
        
        cv2.putText(frame, text, (x, y), font, 1, (255, 255, 255), 2)
        
        # 添加时间戳
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, height - 20), font, 0.5, (128, 128, 128), 1)
        
        return frame
    
    def update_frame(self, frame):
        """更新帧数据"""
        if frame is None:
            return
            
        try:
            # 非阻塞方式放入队列
            if not self.frame_queue.full():
                self.frame_queue.put(frame, block=False)
            else:
                # 队列满时，丢弃旧帧，保留新帧
                try:
                    self.frame_queue.get_nowait()
                    self.frame_queue.put(frame, block=False)
                except queue.Empty:
                    pass
        except Exception as e:
            logger.debug(f"更新帧时出错: {e}")
        
        self.latest_frame = frame
        
        # 优化：如果队列是空的，就直接放入
        if self.frame_queue.empty():
            try:
                self.frame_queue.put_nowait(frame)
            except queue.Full:
                pass # 忽略，下一帧会更新
    
    def _find_available_port(self, start_port=9000, max_attempts=50):
        """查找可用端口，优先重用指定端口"""
        # 首先尝试使用指定的端口（如果可用）
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.5)
            sock.bind(('0.0.0.0', start_port))
            sock.close()
            logger.info(f"端口 {start_port} 可用，将重用此端口")
            return start_port
        except OSError:
            logger.debug(f"端口 {start_port} 不可用，查找其他端口")
        except Exception as e:
            logger.debug(f"检测端口 {start_port} 时出错: {e}")
        
        # 如果指定端口不可用，才查找其他端口
        # 如果原始端口小于9000，从9000开始查找
        if start_port < 9000:
            start_port = 9000
            
        for offset in range(max_attempts):
            test_port = start_port + offset
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(0.5)
                sock.bind(('0.0.0.0', test_port))
                sock.close()
                logger.info(f"找到可用端口: {test_port}")
                return test_port
            except OSError:
                continue
            except Exception as e:
                logger.debug(f"检测端口 {test_port} 时出错: {e}")
                continue
        
        logger.warning(f"未找到可用端口，使用原始端口 {start_port}")
        return start_port
    
    def _get_local_ip(self):
        """获取本机局域网IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "localhost"
    
    def start(self):
        """启动Web服务器"""
        if self.is_running:
            return self.get_url()
        
        # 查找可用端口
        original_port = self.port
        self.port = self._find_available_port(self.port)
        if self.port != original_port:
            logger.info(f"端口从 {original_port} 更改为 {self.port}")
        
        self.is_running = True
        
        # 启动Flask服务器线程
        def run_server():
            try:
                # 禁用Flask的启动信息
                import logging as flask_logging
                flask_log = flask_logging.getLogger('werkzeug')
                flask_log.setLevel(flask_logging.ERROR)
                
                self.app.run(
                    host=self.host,
                    port=self.port,
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                logger.error(f"Flask服务器启动失败: {e}")
                self.is_running = False
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # 等待服务器启动并绑定端口
        time.sleep(1)
        
        # 尝试连接以确认服务器已就绪
        if not self._test_connection():
            logger.error("无法连接到内部Web服务器，启动失败")
            self.stop()
            return None
            
        logger.info(f"Web服务已在 {self.get_url()} 启动")
        return self.get_url()
    
    def _test_connection(self):
        """测试服务器连接"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.host if self.host != "0.0.0.0" else "127.0.0.1", self.port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_url(self):
        """获取访问URL"""
        if self.host == "0.0.0.0":
            # 返回局域网IP
            local_ip = self._get_local_ip()
            return f"http://{local_ip}:{self.port}/"
        else:
            return f"http://{self.host}:{self.port}/"
    
    def stop(self):
        """停止Flask服务器"""
        if not self.is_running:
            return
            
        logger.info("正在停止Web服务...")
        self.is_running = False
        
        # 等待服务器线程结束
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=3.0)
            if self.server_thread.is_alive():
                logger.debug("Web服务线程未能及时停止")
        
        logger.info("Web服务已停止")

if __name__ == '__main__':
    """用于独立测试的简单示例"""
    
    # 初始化
    web_stream = WebStreamer(host="0.0.0.0", port=9000)
    web_stream.add_shutdown_route()
    url = web_stream.start()
    
    if not url:
        print("❌ 启动失败")
        exit()
        
    print(f"✅ Web流服务已启动: {url}")
    print("🎬 开始模拟摄像头帧...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 无法打开摄像头")
        web_stream.stop()
        exit()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            web_stream.update_frame(frame)
            time.sleep(0.03)  # 模拟~30fps
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
    finally:
        cap.release()
        web_stream.stop()
        print("✅ 服务已停止") 