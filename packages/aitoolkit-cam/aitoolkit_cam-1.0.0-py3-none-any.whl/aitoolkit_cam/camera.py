"""
Camera 模块 - 精简版摄像头接口 (专为ARM64+Web流优化)
"""
import threading
import time
import cv2
import numpy as np
import logging
import sys
import queue
import os
from .web_streamer import WebStreamer

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("aitoolkit_cam")

class Camera:
    """
    精简摄像头类 - 专为中学生和ARM64设计
    
    使用方法:
    cam = Camera()
    cam.start()
    for frame in cam:
        cam.show(frame)
    cam.stop()
    """
    
    def __init__(self, source='auto', width=640, height=480, fps=None, max_frames=None, port=9000, en_jupyter=True, auto_stop_frames=500):
        """
        初始化摄像头
        
        参数:
            source: 'auto' 或摄像头索引
            width: 视频宽度
            height: 视频高度  
            fps: 帧率
            max_frames: 最大帧数限制 (None表示无限制)
            port: Web服务端口
            en_jupyter: 启用Jupyter模式
            auto_stop_frames: 无客户端观看时自动停止的帧数
        """
        self.source = self._detect_camera() if source == 'auto' else source
        self.width = width
        self.height = height
        self.fps_setting = fps
        self.max_frames = max_frames
        self.port = port
        self.en_jupyter = en_jupyter
        self.auto_stop_frames = auto_stop_frames
        
        # 状态管理
        self.cap = None
        self.is_running = False
        self.frame_count = 0
        self.web_stream = None
        
        # 智能停止相关
        self._no_client_count = 0  # 无客户端连接的帧数计数
        self._last_client_check = 0
        
        # 线程和队列 - 优化延迟
        self.frame_queue = queue.Queue(maxsize=1)  # 实时流，只缓存1帧
        self._reader_thread = None
        self._stop_event = threading.Event()
        
        logger.info(f"📷 Camera初始化: source={self.source}, size={self.width}x{self.height}, port={self.port}, auto_stop={self.auto_stop_frames}帧")
    
    def _detect_camera(self):
        """极简摄像头检测 - ARM64优化"""
        logger.info("🔍 智能检测摄像头...")
        
        # ARM64: 优先检查设备文件
        if sys.platform.startswith('linux'):
            for i in range(3):  # 只检查前3个
                device_path = f"/dev/video{i}"
                if os.path.exists(device_path):
                    logger.info(f"📹 发现设备: {device_path}")
                    if self._test_device(i):
                        return i
        else:
            # Windows: 直接测试
            for i in range(3):
                if self._test_device(i):
                    return i
        
        logger.warning("⚠️ 未检测到摄像头，使用默认索引0")
        return 0
    
    def _test_device(self, device_id):
        """测试设备是否可用 - 快速检测"""
        try:
            # ARM64: 优先使用V4L2后端
            backend = cv2.CAP_V4L2 if sys.platform.startswith('linux') else cv2.CAP_ANY
            cap = cv2.VideoCapture(device_id, backend)
            
            # 设置快速超时
            if hasattr(cv2, 'CAP_PROP_OPEN_TIMEOUT_MSEC'):
                cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 1000)  # 1秒超时
            
            if cap.isOpened():
                # 不读取帧，只检查是否能打开
                cap.release()
                logger.info(f"✅ 设备 {device_id} 可用")
                return True
            
            cap.release()
            return False
        except Exception as e:
            logger.debug(f"设备 {device_id} 测试失败: {e}")
            return False
    
    def start(self):
        """启动摄像头和Web服务 - 快速启动"""
        if self.is_running:
            logger.warning("摄像头已在运行")
            return self.get_web_url()
        
        logger.info("🚀 启动摄像头...")
        start_time = time.time()
        
        # 初始化摄像头 - 优化后端选择
        if sys.platform.startswith('linux'):
            backend = cv2.CAP_V4L2
        elif sys.platform.startswith('win'):
            backend = cv2.CAP_DSHOW  # Windows用DirectShow更快
        else:
            backend = cv2.CAP_ANY
            
        logger.info(f"📷 使用后端: {backend}, 设备: {self.source}")
        cap_start = time.time()
        
        self.cap = cv2.VideoCapture(self.source, backend)
        cap_time = time.time() - cap_start
        logger.info(f"📷 VideoCapture创建耗时: {cap_time:.2f}秒")
        
        # 快速检查
        if not self.cap.isOpened():
            raise RuntimeError(f"无法打开摄像头 {self.source}")
        
        # 快速配置 - 只设置关键参数
        config_start = time.time()
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 最小缓冲
        
        # 跳过分辨率设置，使用默认值加快启动
        # if self.width and self.height:
        #     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        #     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        # if self.fps_setting:
        #     self.cap.set(cv2.CAP_PROP_FPS, self.fps_setting)
        
        config_time = time.time() - config_start
        logger.info(f"⚙️ 配置耗时: {config_time:.2f}秒")
        
        # 跳过预热帧读取，直接启动
        self.is_running = True
        self._stop_event.clear()
        
        # 启动Web服务
        web_start = time.time()
        self._init_web_stream()
        web_time = time.time() - web_start
        logger.info(f"🌐 Web服务启动耗时: {web_time:.2f}秒")
        
        # 启动读取线程
        thread_start = time.time()
        self._reader_thread = threading.Thread(target=self._read_frames, daemon=True)
        self._reader_thread.start()
        thread_time = time.time() - thread_start
        logger.info(f"🧵 线程启动耗时: {thread_time:.3f}秒")
        
        init_time = time.time() - start_time
        logger.info(f"⚡ 摄像头启动完成，总耗时: {init_time:.2f}秒")
        
        return self.get_web_url()
    
    def _read_frames(self):
        """读取帧的后台线程 - 优化延迟和智能停止"""
        consecutive_read_fails = 0
        
        while self.is_running and not self._stop_event.is_set():
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    consecutive_read_fails = 0
                    
                    # 实时模式：直接替换，不等待
                    try:
                        # 快速清空队列，确保最新帧
                        while not self.frame_queue.empty():
                            try:
                                self.frame_queue.get_nowait()
                            except queue.Empty:
                                break
                        
                        self.frame_queue.put_nowait(frame)  # 非阻塞放入
                        
                        # 更新Web流 - 优化延迟
                        if self.web_stream:
                            self.web_stream.update_frame(frame)
                        
                        # 智能停止检测（每30帧检查一次客户端）
                        if self.frame_count % 30 == 0:
                            self._check_client_connection()
                            
                    except queue.Full:
                        pass  # 队列满了就跳过这一帧，保持实时性
                else:
                    consecutive_read_fails += 1
                    if consecutive_read_fails > 10:
                        logger.warning("连续读取失败，可能摄像头断开")
                        time.sleep(0.1)
                    else:
                        time.sleep(0.001)  # 减少等待时间
            else:
                time.sleep(0.01)  # 摄像头未打开时稍等
    
    def _check_client_connection(self):
        """检查客户端连接状态，实现智能停止"""
        if self.web_stream:
            client_count = self.web_stream.get_client_count()
            
            if client_count == 0:
                self._no_client_count += 30  # 每次检查增加30帧
                
                if self._no_client_count >= self.auto_stop_frames:
                    logger.info(f"🔄 无客户端观看超过{self.auto_stop_frames}帧，自动停止")
                    # 设置停止标志，让线程自然退出，避免递归调用
                    self.is_running = False
                    self._stop_event.set()
                    return
                    
                if self._no_client_count % 150 == 0:  # 每150帧提示一次
                    logger.info(f"💤 无客户端观看，{self.auto_stop_frames - self._no_client_count}帧后自动停止")
            else:
                # 有客户端连接，重置计数
                if self._no_client_count > 0:
                    logger.info(f"👥 检测到{client_count}个客户端连接")
                    self._no_client_count = 0
    
    def _init_web_stream(self):
        """初始化Web流 - 优化启动速度"""
        if not self.web_stream:
            self.web_stream = WebStreamer(host="0.0.0.0", port=self.port)
        
        if not self.web_stream.is_running:
            self.web_stream.start()
            # 异步启动，不等待，让Web服务在后台启动
            time.sleep(0.1)  # 最小等待时间
    
    def read(self, timeout=1.0):
        """读取一帧"""
        if not self.is_running:
            return False, None
        
        try:
            frame = self.frame_queue.get(timeout=timeout)
            return True, frame
        except:
            return False, None
    
    def show(self, frame, mode="web", wait_key=1, window_name="Preview"):
        """
        显示帧
        
        参数:
            frame: 视频帧
            mode: "web" 或 "cv"
            wait_key: OpenCV等待键盘输入时间
            window_name: 窗口名称
        """
        if mode == "web":
            # Web模式：帧已通过Web流显示
            pass
        else:
            # CV模式：使用OpenCV显示
            try:
                cv2.imshow(window_name, frame)
                key = cv2.waitKey(wait_key) & 0xFF
                return key == ord('q') or key == 27  # q键或ESC退出
            except:
                logger.warning("无法显示图像，可能缺少GUI支持")
                return False
    
    def get_web_url(self):
        """获取Web访问地址"""
        if self.web_stream:
            return self.web_stream.get_url()
        else:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return f"http://{local_ip}:{self.port}"
    
    def stop(self):
        """停止摄像头和服务"""
        logger.info("🛑 停止摄像头...")
        self.is_running = False
        self._stop_event.set()
        
        # 停止线程
        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1)
        
        # 释放摄像头
        if self.cap:
            self.cap.release()
            
        # 停止Web服务
        if self.web_stream:
            self.web_stream.stop()
        
        logger.info("✅ 摄像头已停止")
    
    def __iter__(self):
        """迭代器接口"""
        return self
    
    def __next__(self):
        """获取下一帧 - 智能停止机制"""
        # 检查固定帧数限制（如果设置了）
        if self.max_frames and self.frame_count >= self.max_frames:
            logger.info(f"已达到最大帧数限制: {self.max_frames}")
            raise StopIteration
        
        # 检查是否因无客户端而停止
        if not self.is_running:
            raise StopIteration
            
        ret, frame = self.read()
        if ret:
            self.frame_count += 1
            return frame
        else:
            raise StopIteration
    
    def __enter__(self):
        """上下文管理器"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.stop()
    
    def __del__(self):
        """析构函数"""
        self.stop()
    
    # 静态方法 - 保持兼容性
    @staticmethod
    def find_available_cameras(max_test=5):
        """检测可用摄像头"""
        available = []
        for i in range(max_test):
            try:
                backend = cv2.CAP_V4L2 if sys.platform.startswith('linux') else cv2.CAP_ANY
                cap = cv2.VideoCapture(i, backend)
                if cap.isOpened() and cap.read()[0]:
                    available.append(i)
                cap.release()
            except:
                continue
        return available
    
    @staticmethod
    def get_default_camera():
        """获取默认摄像头"""
        available = Camera.find_available_cameras(max_test=3)
        return available[0] if available else None
    
    # 兼容性方法
    def is_running_status(self):
        """检查是否运行中"""
        return self.is_running
    
    def get_fps(self):
        """获取帧率"""
        return self.cap.get(cv2.CAP_PROP_FPS) if self.cap else 0
    
    def set_port(self, port):
        """设置端口"""
        self.port = port 