<!--
 * @Author: wangqz
 * @Date: 2026-05-25
 * @LastEditTime: 2026-05-26
 * @Description: content
-->

##  屏幕字幕离线朗读工具

离线屏幕字幕朗读工具，基于 PaddleOCR 实现屏幕局部文字识别，搭配 Piper TTS 完成离线语音播报。
用户手动框选屏幕任意区域后，程序会循环监控该区域画面，当识别到文字内容发生变化时，自动提取文字并转为语音朗读。

> 姑娘喜欢看夏目友人帐但是日语他听不懂,字幕也不认识, 还有玩游戏的时候一些对话她也不认识字, 所以这个项目就诞生了


```bash
# 需要 conda 环境
conda create  -n readscreen python=3.10
conda activate readscreen

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

python main.py

# 框选区域之后 切换视频应用
```


### 平台特殊说明（针对 Mac M1/M2 / Windows / Linux）

- macOS：部分系统 tkinter 可能缺失，终端补装：
- Windows/Linux：Python 安装时勾选 tcl/tk and IDLE 即可自带 tkinter


### 语音 tts 模型
如果需要其他的模型 可以在 https://github.com/OHF-Voice/piper1-gpl 查找