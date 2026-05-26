from paddleocr import PaddleOCR
print("--- 启动纯 CPU 运行模式 ---")

# 初始化 PaddleOCR 时指定 device="cpu" 即可
# 3.x 版本中已弃用 use_angle_cls=False，请使用 use_textline_orientation=False 
ocr = PaddleOCR(enable_mkldnn=False, device="cpu", lang="ch", use_textline_orientation=False)

# 读取当前目录下的 t.png 图片并开始识别
img_path = 't.png'
results = ocr.ocr(img_path)

# 提取并打印输出识别出来的纯文本
print("\n--- 识别结果 ---")
if results and results[0]:
    for line in results[0]:
        # line 结构为: [[坐标], (文本内容, 置信度)]
        text = line[1][0]
        confidence = line[1][1]
        print(f"文本: {text} (置信度: {confidence:.2f})")
else:
    print("未在图片中检测到任何文字。")
