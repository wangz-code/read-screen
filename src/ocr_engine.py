import numpy as np
import mss
import cv2
from paddleocr import PaddleOCR

class OCREngine:
    def __init__(self):
        print("正在初始化 PaddleOCR（首次加载会下载模型，请稍等）...")
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        print("OCR 引擎就绪")

    def screen_ocr(self,region: dict) -> str:
        with mss.MSS() as sct:
            grab_img = sct.grab(region)
            img_arr = np.array(grab_img)
            
            # 通道预处理
            img_bgr = img_arr[:, :, :3]
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            img_enhanced = cv2.convertScaleAbs(img_gray, alpha=1.8, beta=10)
            img_rgb = cv2.cvtColor(img_enhanced, cv2.COLOR_GRAY2RGB)

            results = self.ocr.predict(img_rgb)
            text_list = []
            for item in results:
                if "rec_texts" in item:
                    text_list.extend(item["rec_texts"])
            return "".join(text_list)

