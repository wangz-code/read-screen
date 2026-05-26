# src/tts_engine.py
import threading
import queue
import wave
import simpleaudio as sa
from piper import PiperVoice
import os
# 1. 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. 拼接模型完整路径
MODEL_Folder = os.path.join(BASE_DIR, "TTSModal")

MODEL_PATH = MODEL_Folder+"/zh_CN-huayan-medium.onnx"

class TTSEngine:
    """Piper TTS 封装，支持异步播放，非阻塞"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # 单例模式，避免重复加载模型
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.model_path = MODEL_PATH
        print(f"正在加载 Piper 模型: {self.model_path}")
        self.voice = PiperVoice.load(self.model_path)
        self.sample_rate = self.voice.config.sample_rate
        print(f"模型加载完成，采样率: {self.sample_rate}")

        # 异步播放队列
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._worker = threading.Thread(target=self._play_worker, daemon=True)
        self._worker.start()
        self._initialized = True

    def speak(self, text):
        """异步朗读文本，立即返回"""
        if not text or not text.strip():
            return
        self._queue.put(text.strip())

    def _synthesize(self, text):
        """合成音频，返回 PCM 字节数据"""
        audio_bytes = b''.join(chunk.audio_int16_bytes for chunk in self.voice.synthesize(text))
        return audio_bytes

    def _play_worker(self):
        """后台线程：从队列取文本，合成并播放"""
        while not self._stop_event.is_set():
            try:
                text = self._queue.get(timeout=0.5)
                if text is None:
                    continue
                # 合成音频
                audio_data = self._synthesize(text)
                if not audio_data:
                    continue
                # 播放（阻塞直到播放完成）
                play_obj = sa.play_buffer(audio_data, 1, 2, self.sample_rate)
                play_obj.wait_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[TTS错误] {e}")

    def stop(self):
        """停止所有播放并清理资源"""
        self._stop_event.set()
        if self._worker.is_alive():
            self._worker.join(timeout=1.0)


# 为了方便直接调用，提供一个全局实例（懒加载）
_tts_engine = None

def speak(text):
    """全局函数，直接调用朗读"""
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = TTSEngine()
    _tts_engine.speak(text)