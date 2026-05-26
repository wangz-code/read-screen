import time
import threading
import subprocess
import numpy as np
import cv2
from ocr_engine import OCREngine
from tts_engine import TTSEngine
from region_selector import RegionSelector
import sounddevice as sd
from piper import PiperVoice
import re
from difflib import SequenceMatcher


def keep_chinese(text: str) -> str:
    """只保留中文字符，过滤字母、数字、符号、空格"""
    # 正则匹配所有中文
    pattern = re.compile(r'[^\u4e00-\u9fff]')
    # 非中文全部替换为空
    return pattern.sub('', text)

def is_similar(text1, text2, threshold=0.5):
    """判断两个文本的相似度是否超过阈值"""
    if not text1 or not text2:
        return False
    return SequenceMatcher(None, text1, text2).ratio() > threshold


class ScreenReader:
    def __init__(self):
        self.ocr = OCREngine()
        self.tts = TTSEngine()
        self.running = False
        self.last_text = ""
        self.region = {}

    def start(self,rootTk):
        region = RegionSelector.select_region(rootTk)
        print("region:",region)
        if region is None:
            self.start()
            return 

        self.region = region
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        return True

    def _monitor_loop(self):
        while self.running:
            try:
                ocr_text = self.ocr.screen_ocr(self.region)
                text = keep_chinese(ocr_text)
                print("text: ", text)
                # 文字变更才播报
                if text and not is_similar(text, self.last_text, threshold=0.5):
                    self.tts.speak(text)
                    self.last_text = text
                time.sleep(0.41)
            except Exception as e:
                print(f"监控异常: {e}")
                time.sleep(1)

    def stop(self):
        self.running = False

