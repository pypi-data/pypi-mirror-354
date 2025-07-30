<div align="center">
  <img src="https://raw.githubusercontent.com/bosscoder-ai/aitoolkit_cam/main/docs/assets/logo.png" alt="AIToolkit Camera Logo" width="150"/>
  <h1>AIToolkit Camera</h1>
  <p><strong>一个为中学生和初学者设计的超简单Python摄像头库</strong></p>
  <p>
    <a href="https://pypi.org/project/aitoolkit-cam/"><img src="https://img.shields.io/pypi/v/aitoolkit-cam.svg" alt="PyPI Version"></a>
    <a href="https://github.com/bosscoder-ai/aitoolkit_cam/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/aitoolkit-cam.svg" alt="License"></a>
    <a href="https://github.com/bosscoder-ai/aitoolkit_cam"><img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version"></a>
  </p>
</div>

---

`aitoolkit-cam` 是一个强大的Python摄像头工具库，它将复杂的摄像头操作封装成极其简洁的接口。无论你是编程新手还是经验丰富的开发者，都可以用最少的代码快速实现本地窗口显示和网页流媒体功能。

## ✨ 核心特性

- **极简API**: 只需几行代码即可启动摄像头并显示视频。
- **Jupyter 模式**: 默认开启安全模式，在Jupyter环境中自动处理资源释放，避免内核崩溃。
- **双显示模式**: 同时支持本地`OpenCV`窗口和`Web`浏览器实时视频流。
- **自动管理**: 使用`with`语句自动完成摄像头的启动和关闭，无需手动管理。
- **智能健壮**: 自动检测可用摄像头，处理各种异常。
- **中文友好**: 完美支持在窗口标题中显示中文。

## 🚀 快速上手

首先，请确保你已经安装了 `aitoolkit-cam` 和 `opencv-python`。

```bash
pip install aitoolkit-cam opencv-python
```

### 本地窗口显示

这是在本地窗口中显示摄像头的最简单方法。代码会在一个名为"实时画面"的窗口中显示视频，直到你按下 'q' 键。

```python
from aitoolkit_cam import Camera

# 使用 'with' 语句自动管理摄像头
try:
    with Camera() as cam:
        print("📹 摄像头已启动, 按 'q' 键退出。")
        # 循环获取并显示每一帧
        for frame in cam:
            # show() 方法会处理显示和按键检测
            if cam.show(frame, window_name="实时画面"):
                break
    print("✅ 演示完成")
except Exception as e:
    print(f"❌ 启动失败: {e}")
```

### Jupyter Notebook / Lab

在Jupyter环境中使用 `aitoolkit-cam` 同样简单。默认的Jupyter模式会自动显示50帧后停止，防止无限运行和资源泄漏。

```python
from aitoolkit_cam import Camera

# 在Jupyter中，这会自动显示50帧然后停止
with Camera() as cam:
    for frame in cam:
        if cam.show(frame, window_name="Jupyter演示"):
            break
```

### 网页流模式

想在浏览器里看视频？只需一个参数即可。

```python
from aitoolkit_cam import Camera
import time

# 启用web模式
with Camera(web_enabled=True) as cam:
    url = cam.get_web_url()
    print(f"🌍 Web服务已启动: {url}")
    print("请在浏览器中打开以上URL。服务将在20秒后自动关闭。")
    
    # 保持程序运行以提供视频流
    time.sleep(20)

print("Web演示结束。")
```

## 📚 文档

- **[快速入门](docs/quick_start.md)**: 最快速的上手指南。
- **[API参考](docs/api_reference.md)**: `Camera`类的详细接口文档。
- **[学生指南](docs/student_guide.md)**: 专为中学生设计的趣味教程。

## 🤝 贡献

我们欢迎任何形式的贡献！无论是提交bug报告、功能请求还是代码PR，请随时通过 [GitHub Issues](https://github.com/bosscoder-ai/aitoolkit_cam/issues) 与我们联系。

## 📄 许可

本项目采用 [MIT 许可](LICENSE)。 