"""
Camera 模块 - 提供简洁的摄像头接口
"""
import threading
import time
import cv2
import asyncio
import numpy as np
import logging
import sys
import queue  # Added for queue.Queue
from .web_streamer import WebStreamer

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 恢复为INFO级别，显示重要信息但不过于冗长
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("aitoolkit_cam")

# Sentinel object to signal the end of the queue
_QUEUE_SENTINEL = object()

class _CameraReaderThread(threading.Thread):
    """
    专用线程，负责从摄像头硬件读取帧并将其放入队列。
    """
    def __init__(self, source, width, height, fps, raw_frame_queue, initialized_event, stop_event, target_fps):
        super().__init__(daemon=True)
        self.name = "_CameraReaderThread"
        self.source = source
        # 确保width和height是整数类型
        self.target_width = int(width) if width is not None else None
        self.target_height = int(height) if height is not None else None
        self.target_fps_setting = fps # FPS setting for camera
        self.raw_frame_queue = raw_frame_queue # Renamed
        self.initialized_event = initialized_event
        self.stop_event = stop_event
        self.cap = None
        
        # Actual FPS for frame reading loop
        self.actual_read_fps = target_fps if target_fps is not None else 30  # Default to 30 if not specified
        self.frame_interval = 1.0 / self.actual_read_fps if self.actual_read_fps > 0 else 0
        
        # 减少队列满警告的频率
        self.queue_full_count = 0

    def run(self):
        try:
            logger.info(f"[{self.name}] Initializing camera source: {self.source}...")
            
            # 根据平台和源类型选择合适的后端
            if isinstance(self.source, int):
                # 摄像头索引
                if sys.platform.startswith('win'):
                    self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
                elif sys.platform.startswith('linux'):
                    # Linux系统优先尝试V4L2后端
                    try:
                        self.cap = cv2.VideoCapture(self.source, cv2.CAP_V4L2)
                        logger.info(f"[{self.name}] Using V4L2 backend for camera {self.source}")
                    except Exception as e:
                        logger.warning(f"[{self.name}] V4L2 backend failed: {e}, trying default backend")
                        self.cap = cv2.VideoCapture(self.source)
                else:
                    self.cap = cv2.VideoCapture(self.source)
            else:
                # 视频文件或其他源
                self.cap = cv2.VideoCapture(self.source)
                logger.info(f"[{self.name}] Opening video file/stream: {self.source}")

            if not self.cap.isOpened():
                logger.error(f"[{self.name}] Failed to open video source: {self.source}")
                if isinstance(self.source, int):
                    logger.error(f"[{self.name}] Camera index {self.source} is not available")
                    if sys.platform.startswith('linux'):
                        logger.error(f"[{self.name}] Linux troubleshooting:")
                        logger.error(f"[{self.name}] - Check if /dev/video{self.source} exists")
                        logger.error(f"[{self.name}] - Try: ls -la /dev/video*")
                        logger.error(f"[{self.name}] - Check user permissions: groups $USER")
                self.initialized_event.set() # Signal completion (even if failed)
                return

            # 配置摄像头参数
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if self.target_width and self.target_height:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_height)
            if self.target_fps_setting is not None:
                self.cap.set(cv2.CAP_PROP_FPS, self.target_fps_setting)

            # Pre-read some frames to ensure camera is stable
            logger.info(f"[{self.name}] Pre-reading frames to stabilize camera...")
            stable_frames = 0
            for attempt in range(10):  # 最多尝试10次
                if not self.cap.isOpened() or self.stop_event.is_set(): 
                    break
                ret, frame = self.cap.read()
                if ret and frame is not None and frame.size > 0:
                    stable_frames += 1
                    if stable_frames >= 3:  # 连续3帧成功就认为稳定
                        break
                time.sleep(0.05)
            
            if stable_frames < 3:
                logger.error(f"[{self.name}] Camera not stable after pre-read (only {stable_frames} valid frames)")
                self.initialized_event.set()
                return

            # 获取实际配置
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps_val = self.cap.get(cv2.CAP_PROP_FPS)
            logger.info(f"[{self.name}] Camera configured: {actual_width}x{actual_height} @ {actual_fps_val}fps (Target read FPS: {self.actual_read_fps})")
            
            self.initialized_event.set() # Signal that initialization is complete
            
            last_frame_read_time = time.time()

            while not self.stop_event.is_set():
                current_time = time.time()
                if self.frame_interval > 0 and (current_time - last_frame_read_time < self.frame_interval):
                    sleep_time = self.frame_interval - (current_time - last_frame_read_time)
                    if sleep_time > 0.001: # Only sleep if meaningful
                        time.sleep(sleep_time * 0.8) # Sleep a bit less to catch up if needed
                    continue # Re-check stop event and time

                ret, frame = self.cap.read()
                last_frame_read_time = time.time()

                if not ret:
                    logger.warning(f"[{self.name}] Failed to read frame from source.")
                    # Wait a bit before retrying or breaking
                    time.sleep(0.1)
                    if not self.cap.isOpened(): # If camera closed itself
                        logger.error(f"[{self.name}] Camera disconnected.")
                        break
                    continue
                
                if frame is None or frame.size == 0:
                    logger.warning(f"[{self.name}] Received empty frame")
                    continue
                
                # 为帧附加捕获时的时间戳
                timestamp_ns = time.time_ns()
                
                try:
                    # 将 (frame, timestamp) 元组放入队列
                    self.raw_frame_queue.put((frame, timestamp_ns), timeout=0.01) # 很短的超时，实时优先
                except queue.Full:
                    # 实时模式：队列满时自动丢弃最旧的帧，保留最新的帧
                    # 这样确保用户总是看到最新的画面，而不是延迟的画面
                    try:
                        self.raw_frame_queue.get_nowait()  # 丢弃最旧的帧
                        self.raw_frame_queue.put_nowait((frame, timestamp_ns))  # 添加最新的帧
                    except (queue.Empty, queue.Full):
                        # 如果操作失败，继续处理下一帧，不要阻塞
                        pass
                except Exception as e:
                    logger.error(f"[{self.name}] Error putting frame to raw_frame_queue: {e}")
                    break

        except Exception as e:
            logger.error(f"[{self.name}] Error in camera reader thread: {e}", exc_info=True)
            self.initialized_event.set() # Ensure main thread is not blocked if init fails here
        finally:
            if self.cap:
                self.cap.release()
            self.raw_frame_queue.put(_QUEUE_SENTINEL) # Signal consumers that reading has stopped
            logger.info(f"[{self.name}] Camera reader thread stopped.")


class Camera:
    """摄像头类，实现迭代器接口和显示功能"""

    def __init__(self, source='auto', width=640, height=480, fps=None, web_enabled=False, port=9000, max_frames=300, en_jupyter=True):
        """
        初始化摄像头
        
        参数:
            source: 视频源，可以是：
                   - 'auto': 自动使用系统默认摄像头 (索引 0)，不再扫描。
                   - int: 摄像头索引 (0, 1, 2, ...)
                   - str: 视频文件路径
            width: 输出视频帧宽度
            height: 输出视频帧高度
            fps: 摄像头目标帧率 (用于摄像头设置和读取控制)
            web_enabled: 是否启用网页流服务
            port: 网页服务端口号
            max_frames: 最大显示帧数，达到后自动停止 (默认为 300)。
            en_jupyter: 是否启用Jupyter模式 (主要用于自动资源清理)
        """
        self.max_frames = max_frames
        
        # 处理source参数
        if source == 'auto':
            logger.info("自动检测模式: 默认使用摄像头索引 0，不再进行扫描以避免闪烁。")
            self.source = 0
        elif isinstance(source, str) and source.isdigit():
            # 如果传入的是数字字符串，转换为整数
            self.source = int(source)
        else:
            self.source = source
            
        # 基本参数
        self.width = width
        self.height = height
        self.fps_setting = fps # FPS to request from camera
        
        # Jupyter和帧数控制
        self.en_jupyter = en_jupyter
        self.frame_count = 0  # 已显示帧数计数器
        self._auto_stop_triggered = False  # 自动停止标志
        
        # Web流相关
        self.web_enabled = web_enabled
        self.port = port
        self.web_stream = None
        
        # 状态变量
        self.is_running = False
        self._camera_reader_thread = None
        self._reader_stop_event = threading.Event()
        self._reader_initialized_event = threading.Event() # Signals when _CameraReaderThread has initialized cap
        
        # Frame queue - 默认使用实时低延迟设计，只缓存少量帧
        self.raw_frame_queue = queue.Queue(maxsize=3) # 只缓存3帧，确保低延迟
        
        # 资源保护 (used for critical sections in Camera class, less for frame data itself now)
        self._lock = threading.RLock() 
        
        # If web_enabled, prepare SimpleWebStream instance
        if self.web_enabled:
            self._init_web_stream_instance()

        # For Notebook mode
        self._notebook_mode_thread = None
        self._notebook_mode_stop_event = threading.Event()
        
        if self.en_jupyter:
            logger.info(f"Camera初始化完成 (Jupyter模式): source={self.source}, size={self.width}x{self.height}, fps={self.fps_setting}, max_frames={self.max_frames}")
        else:
            logger.info(f"Camera初始化完成: source={self.source}, size={self.width}x{self.height}, fps={self.fps_setting}")

    def _register_jupyter_cleanup(self):
        """注册Jupyter环境的自动清理"""
        import atexit
        
        if not hasattr(self, '_jupyter_cleanup_registered'):
            atexit.register(lambda: self.stop() if hasattr(self, 'is_running') and self.is_running else None)
            self._jupyter_cleanup_registered = True
            logger.info("Jupyter自动清理已注册")

    def show(self, frame, mode="cv2", wait_key=1, window_name="预览"):
        """
        显示图像并处理按键 (类似于 cv2.imshow)
        
        参数:
            frame: 要显示的图像帧
            mode: 显示模式，"cv2"表示本地显示，"web"表示发送到网页流
            wait_key: cv2.waitKey的等待时间(毫秒)，仅cv2模式有效
            window_name: 窗口名称，支持中文显示
        
        返回:
            cv2模式下，如果按下'q'或'ESC'则返回True，表示应退出循环；
            web模式下或无按键时返回False。
        """
        if frame is None:
            return False
        
        display_frame = frame
        if len(frame.shape) == 2: # Grayscale
            display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        
        if mode == "web":
            # Web模式：发送到网页流
            if self.web_stream and self.web_stream.is_running:
                self.web_stream.update_frame(display_frame)
            return False
        else:
            # cv2模式：本地显示（需要GUI支持）
            try:
                # --- 修复Windows下中文窗口标题乱码 ---
                display_window_name = window_name
                if sys.platform.startswith('win'):
                    try:
                        display_window_name = display_window_name.encode('gbk').decode('latin1', 'ignore')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        logger.debug(f"窗口标题 '{window_name}' 无法编码为GBK，可能在Windows上显示为乱码。")

                cv2.imshow(display_window_name, display_frame)
                key = cv2.waitKey(wait_key) & 0xFF
                if key == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    return True
                return False
            except cv2.error as e:
                logger.warning(f"cv2.imshow failed (no GUI support): {e}")
                logger.info("Tip: Use mode='web' for web display instead")
                return True

    def _init_web_stream_instance(self):
        # Dynamically import to avoid dependency if not used
        from .web_streamer import WebStreamer
        self.web_stream = WebStreamer(
            host="0.0.0.0",
            port=self.port
        )

    def read(self, timeout=2.0):
        """
        读取一帧（OpenCV兼容接口）。
        此方法不处理帧数限制，仅用于按需获取单帧。
        
        参数:
            timeout: 从队列获取帧的最长等待时间（秒）。
        返回:
            (ret, frame) 元组，ret表示是否成功，frame为读取的帧(或带时间戳的元组)或None。
            在新版本中，为了支持时间戳，成功时返回 (True, (frame, timestamp_ns))
        """
        if not self.is_running and self.raw_frame_queue.empty():
            return False, None
        
        # 等待摄像头初始化完成
        if not self._reader_initialized_event.is_set():
            if not self._reader_initialized_event.wait(timeout=0.5): # Give it a moment
                logger.debug("Read called before camera fully initialized.")
                return False, None

        try:
            # 现在获取的是 (frame, timestamp) 元组
            frame_data = self.raw_frame_queue.get(block=True, timeout=timeout)
            if frame_data is _QUEUE_SENTINEL:
                self.raw_frame_queue.put(_QUEUE_SENTINEL) # Put back for others
                return False, None
            return True, frame_data
        except queue.Empty:
            return False, None

    def start(self):
        """
        启动摄像头和/或Web服务。
        在Web模式下，此方法会返回可访问的URL。
        """
        with self._lock:
            if self.is_running:
                logger.info("摄像头已经在运行中")
                if self.web_enabled:
                    return self.get_web_url()
                return # 在非web模式下，已经运行时不返回任何东西
            
            self.is_running = True # Set state early
            self._reader_stop_event.clear()
            self._reader_initialized_event.clear()

            # Clear any old items from queue, including potential sentinels
            while not self.raw_frame_queue.empty():
                try:
                    self.raw_frame_queue.get_nowait()
                except queue.Empty:
                    break
            
            logger.info("Starting _CameraReaderThread...")
            self._camera_reader_thread = _CameraReaderThread(
                source=self.source,
                width=self.width,
                height=self.height,
                fps=self.fps_setting, # FPS for camera config
                raw_frame_queue=self.raw_frame_queue,
                initialized_event=self._reader_initialized_event,
                stop_event=self._reader_stop_event,
                target_fps=self.fps_setting # FPS for reader loop control
            )
            self._camera_reader_thread.start()
        
        # Wait briefly for reader to signal initialization attempt (success or failure)
        # This helps make get_web_url more robust if called immediately
        self._reader_initialized_event.wait(timeout=5.0) # Max 5s for camera to open
        if not self._reader_initialized_event.is_set():
            logger.warning("Camera reader thread did not signal initialization within timeout.")

        # Web模式下的启动和URL返回
        if self.web_enabled:
            logger.info("Starting Web service...")
            if not self.web_stream:
                self._init_web_stream_instance()
            
            url = self._start_web_stream() # _start_web_stream 现在会返回URL
            
            # 智能关闭：如果启用web且无帧数限制，则启动闲置监控
            if not self.max_frames:
                logger.info("启动网页流闲置监控 (无帧数限制模式)")
                self._start_web_idle_monitor()
        
            logger.info("Camera start() method finished.")
            return url # 返回获取到的URL
        else:
            logger.info("Camera start() method finished for non-web mode.")
            return None # 非Web模式下返回None
    
    def _start_web_stream(self):
        """启动Web流服务并返回URL"""
        try:
            if not self.web_stream:
                logger.warning("Web stream instance not found, cannot start.")
                return None

            logger.info("Starting SimpleWebStream...")
            url = self.web_stream.start()
            if url:
                logger.info(f"Web stream service started: {url}")
                return url
            else:
                logger.error("Failed to start web stream service")
                return None
                
        except Exception as e:
            logger.error(f"Failed to start Web stream service: {e}", exc_info=True)
            return None
    
    def _start_web_idle_monitor(self, idle_timeout=30.0):
        """启动一个线程，用于在网页流空闲时自动关闭"""
        
        def monitor_loop():
            logger.info("启动网页流空闲监控线程...")
            
            while self.is_running and self.web_stream:
                time.sleep(5.0) # 每5秒检查一次
                
                if not self.is_running:
                    break
                    
                client_count = self.web_stream.get_client_count()
                if client_count == 0:
                    logger.info(f"检测到无客户端连接，将在 {idle_timeout} 秒后关闭...")
                    
                    # 等待一段时间，再次确认是否没有客户端
                    time.sleep(idle_timeout)
                    
                    if not self.is_running:
                        break
            
                    # 再次检查，防止在等待期间有新连接
                    if self.web_stream.get_client_count() == 0:
                        logger.info("确认无客户端连接，自动停止摄像头...")
                        self.stop()
                        break
                    else:
                        logger.info("在等待期间有新客户端连接，取消关闭。")
            
            logger.info("网页流空闲监控线程已停止。")

        # 启动监控线程
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop(self):
        """停止摄像头并释放资源"""
        with self._lock:
            if not self.is_running and not (self._notebook_mode_thread and self._notebook_mode_thread.is_alive()):
                logger.info("Camera and Notebook mode already stopped.")
                return
            
            if self.en_jupyter and self.frame_count > 0:
                logger.info(f"摄像头停止: 共显示了 {self.frame_count} 帧{f'(限制: {self.max_frames})' if self.max_frames else ''}")
            else:
                logger.info("Stopping camera and any active modes (Notebook, etc.)...")
            
            # --- Notebook mode cleanup ---
            if self._notebook_mode_thread and self._notebook_mode_thread.is_alive():
                logger.info("Stopping active Notebook mode thread...")
                self._notebook_mode_stop_event.set()
                self._notebook_mode_thread.join(timeout=1.0) # Shorter timeout, main stop will continue
                if self._notebook_mode_thread.is_alive():
                    logger.warning("Notebook mode thread did not join quickly during main stop.")
            self._notebook_mode_thread = None # Ensure it's cleared

            self.is_running = False # Signal all loops to stop

            # 立即清空队列，防止线程卡在队列操作上
            logger.info("Immediately clearing raw_frame_queue to unblock threads...")
            cleared_count = 0
            while not self.raw_frame_queue.empty():
                try:
                    self.raw_frame_queue.get_nowait()
                    cleared_count += 1
                except queue.Empty:
                    break
            if cleared_count > 0:
                logger.info(f"Cleared {cleared_count} frames from queue")

            # Stop Web流服务 first
            if self.web_stream and self.web_stream.is_running:
                try:
                    logger.info("Stopping Web stream service...")
                    self.web_stream.stop()
                    logger.info("Web stream service stopped.")
                    # 减少等待时间，防止卡住
                    time.sleep(0.2)
                except Exception as e:
                    logger.error(f"Error stopping Web stream service: {e}")

            # Stop camera reader thread - 更强制的停止
            if self._camera_reader_thread and self._camera_reader_thread.is_alive():
                logger.info("Signaling _CameraReaderThread to stop...")
                self._reader_stop_event.set()
                
                # 添加哨兵，强制唤醒可能阻塞的线程
                try:
                    self.raw_frame_queue.put(_QUEUE_SENTINEL, timeout=0.5)
                except queue.Full:
                    logger.debug("Could not add sentinel to full queue during stop")
                
                # Wait for the reader thread to finish - 增加超时时间
                self._camera_reader_thread.join(timeout=3.0)
                if self._camera_reader_thread.is_alive():
                    logger.debug("_CameraReaderThread did not stop in time, continuing anyway.")
            self._camera_reader_thread = None
            
            # Final queue cleanup - 再次清理
            logger.debug("Final queue cleanup...")
            while not self.raw_frame_queue.empty():
                try:
                    item = self.raw_frame_queue.get_nowait()
                    if item is _QUEUE_SENTINEL:
                        logger.debug("Found sentinel in raw_frame_queue during stop cleanup.")
                except queue.Empty:
                    break
            
            self._reader_initialized_event.clear()
            
            # 强制垃圾回收，释放OpenCV资源
            import gc
            gc.collect()
            
        if self.en_jupyter:
            logger.info("摄像头已安全停止并释放资源")
        else:
            logger.info("Camera stopped successfully.")
        
    def get_web_url(self):
        """获取网页流服务的访问URL"""
        if not self.web_enabled:
            logger.info("Web service is not enabled.")
            return None
            
        if not self.web_stream:
            logger.warning("Web_stream instance not initialized in get_web_url.")
            if self.is_running:
                self._init_web_stream_instance()
                self._start_web_stream()
            else:
                return None

        if not self.web_stream or not self.web_stream.is_running:
            logger.warning("Web stream is not running or URL not yet available.")
            return None
            
        return self.web_stream.get_url()
    
    def __iter__(self):
        """返回迭代器自身"""
        if not self.is_running:
            logger.info("Iterator accessed before explicit start(), attempting to start camera...")
            self.start()
        return self
    
    def __next__(self):
        """获取下一帧 for iteration"""
        # 检查帧数限制 (这是Jupyter模式安全的核心)
        if self.max_frames and self.frame_count >= self.max_frames:
            logger.info(f"已达到最大帧数限制 ({self.max_frames})，停止迭代。")
            raise StopIteration
        
        if not self.is_running and self.raw_frame_queue.empty():
            logger.debug("__next__: Not running and raw_frame_queue empty, raising StopIteration.")
            raise StopIteration
        
        # Wait for initialization, but with a timeout to prevent indefinite block if init fails
        if not self._reader_initialized_event.is_set():
            initialized = self._reader_initialized_event.wait(timeout=1.0) # Wait up to 1s
            if not initialized and self.raw_frame_queue.empty():
                 logger.warning("__next__: Camera not initialized after 1s, and raw_frame_queue empty. StopIteration.")
                 if not self.is_running: # If start() failed to keep it running
                    raise StopIteration
        
        try:
            # Blocking get, but _CameraReaderThread puts a sentinel on stop.
            frame_data = self.raw_frame_queue.get(block=True, timeout=2.0) # Timeout to prevent permanent block
            if frame_data is _QUEUE_SENTINEL:
                logger.info("__next__: Sentinel received from raw_frame_queue, raising StopIteration.")
                raise StopIteration
            
            # 迭代器仍然只返回frame，保持API兼容性
            frame, _ = frame_data
            
            # 只有在成功获取帧时才计数
            self.frame_count += 1
            return frame
        except queue.Empty:
            logger.warning("__next__: raw_frame_queue empty after timeout. Raising StopIteration as camera might be stuck or stopped.")
            self.is_running = False # Ensure loop terminates
            raise StopIteration
        except Exception as e:
            logger.error(f"__next__: Error getting frame from raw_frame_queue: {e}")
            self.is_running = False # Ensure loop terminates
            raise StopIteration
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.is_running:
            self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
        
    def __del__(self):
        """析构函数，确保资源释放"""
        try:
            # 检查属性是否存在，避免初始化失败时的AttributeError
            if hasattr(self, 'is_running') and (self.is_running or 
                (hasattr(self, '_camera_reader_thread') and self._camera_reader_thread and self._camera_reader_thread.is_alive())):
                logger.debug(f"Camera __del__ called on a potentially running instance. Attempting to stop.")
                self.stop()
        except Exception as e:
            # 静默处理析构函数中的错误，避免影响程序退出
            logger.debug(f"Error in Camera.__del__: {e}")

    def set_port(self, port):
        """设置Web服务端口，如果服务已启动会重启服务使用新端口"""
        with self._lock:
            old_port = self.port
            if old_port == port:
                logger.info(f"Port already set to {port}.")
                return self.port
            
            self.port = port
            logger.info(f"Web service port changed from {old_port} to {port}.")

            if self.web_enabled:
                if self.web_stream and self.web_stream.is_running:
                    logger.info("Restarting Web service to apply new port...")
                    self.web_stream.stop()
                    
                    # Create a new instance
                    self._init_web_stream_instance()
                    if self.is_running:
                         self._start_web_stream()
                    else:
                        logger.info("Camera is not running, web service will start with new port on next Camera.start()")
                elif self.web_stream:
                    self.web_stream.port = port 
                    logger.info(f"Web service instance port updated to {port}. Will be used on next start.")
                else:
                    logger.info(f"Port set to {port}, but web service is not enabled.")
            else:
                logger.info(f"Port set to {port}, but web service is not enabled.")
        return self.port 

    def start_notebook_mode(self, width=None, height=None, fps=None, port=None, loop_interval=0.02):
        """
        启动适合Jupyter Notebook的模式
        自动获取帧并更新Web流

        Args:
            width (int, optional): Override camera width.
            height (int, optional): Override camera height.
            fps (int, optional): Override camera FPS.
            port (int, optional): Override web service port.
            loop_interval (float, optional): Interval in seconds for the frame fetching loop. Defaults to 0.02.

        Returns:
            str: The URL to access the web stream, or None if failed.
        """
        with self._lock:
            if self._notebook_mode_thread and self._notebook_mode_thread.is_alive():
                logger.info("Notebook mode is already running.")
                return self.get_web_url()

            self.web_enabled = True # Notebook mode implies web is enabled

            # Apply overrides if provided
            if width is not None: self.width = width
            if height is not None: self.height = height
            if fps is not None: self.fps_setting = fps
            if port is not None:
                self.set_port(port) 
            
            # Ensure web stream instance uses the potentially updated port
            if self.web_stream is None or (port is not None and self.web_stream.port != port):
                self._init_web_stream_instance()

            logger.info("Starting camera for Notebook mode...")
            if not self.start():
                logger.error("Failed to start camera in Notebook mode.")
                return None
            
            # Ensure web service is actually started by self.start()
            if not self.web_stream or not self.web_stream.is_running:
                logger.info("Notebook mode: Ensuring web stream is started...")
                self._start_web_stream()
                if not self.web_stream or not self.web_stream.is_running:
                    logger.error("Notebook mode: Failed to start web stream service.")
                    self.stop()
                    return None

            # Wait a brief moment for the URL to become available
            url = None
            for _ in range(10): # Try for up to 1 second
                url = self.get_web_url()
                if url:
                    break
                time.sleep(0.1)
            
            if not url:
                 logger.warning("Notebook mode: Web URL not available after timeout. Service might be slow to start.")
            
            return url

    def stop_notebook_mode(self):
        """
        停止notebook模式并停止摄像头
        """
        logger.info("Stopping Notebook mode...")
        self.stop()
        logger.info("Notebook mode stopped successfully.")
        
    @staticmethod
    def get_camera_count():
        """
        获取可用摄像头数量
        
        返回:
            int: 可用摄像头数量
        """
        return len(Camera.find_available_cameras())
    
    def get_device_info(self):
        """
        获取摄像头设备信息
        
        返回:
            str: 设备信息字符串
        """
        return f"Camera {self.source} ({self.width}x{self.height})"
    
    def get_fps(self):
        """
        获取实际帧率
        
        返回:
            float: 实际帧率
        """
        return self.fps_setting if self.fps_setting else 30.0
    
    def is_running(self):
        """
        检查摄像头是否正在运行
        
        返回:
            bool: 是否正在运行
        """
        return self.is_running

    def _start_web_idle_monitor(self, idle_timeout=30.0):
        """启动一个线程，用于在网页流空闲时自动关闭"""
        
        def monitor_loop():
            logger.info("启动网页流空闲监控线程...")
            
            while self.is_running and self.web_stream:
                time.sleep(5.0) # 每5秒检查一次
                
                if not self.is_running:
                    break

                client_count = self.web_stream.get_client_count()
                if client_count == 0:
                    logger.info(f"检测到无客户端连接，将在 {idle_timeout} 秒后关闭...")
                    
                    # 等待一段时间，再次确认是否没有客户端
                    time.sleep(idle_timeout)
                    
                    if not self.is_running:
                        break

                    # 再次检查，防止在等待期间有新连接
                    if self.web_stream.get_client_count() == 0:
                        logger.info("确认无客户端连接，自动停止摄像头...")
                        self.stop()
                        break
                    else:
                        logger.info("在等待期间有新客户端连接，取消关闭。")
            
            logger.info("网页流空闲监控线程已停止。")

        # 启动监控线程
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        