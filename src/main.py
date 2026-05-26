import tkinter as tk
from tkinter import ttk
from read import ScreenReader
import sys
reader = ScreenReader()
class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("屏幕读取工具")
        self.root.geometry("470x150")
        self.root.configure(bg="#f8f8f8")
        self.root.resizable(False, False)  # 固定窗口大小

        # 自定义按钮样式（圆角+悬浮效果）
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 正常状态
        self.style.configure(
            "Custom.TButton",
            background="#ffffff",
            foreground="#e65c5c",
            font=("Arial", 24, "bold"),
            borderwidth=0,
            padding=(25, 15)
        )
        # 悬浮状态
        self.style.map(
            "Custom.TButton",
            background=[("active", "#fff0f0")],
            foreground=[("active", "#d64545")]
        )

        # 绘制选区按钮
        self.btn_select = ttk.Button(
            self.root,
            text="绘制选区",
            style="Custom.TButton",
            command=self.on_select_region
        )
        self.btn_select.place(relx=0.28, rely=0.5, anchor="center")

        # 退出程序按钮
        self.btn_exit = ttk.Button(
            self.root,
            text="退出程序",
            style="Custom.TButton",
            command=self.on_exit
        )
        self.btn_exit.place(relx=0.72, rely=0.5, anchor="center")

        # 顶部标题
        title_label = tk.Label(
            self.root,
            text="屏幕读取工具",
            font=("Arial", 18),
            bg="#f8f8f8",
            fg="#333333"
        )
        title_label.place(relx=0.5, rely=0.15, anchor="center")

    def on_select_region(self):
        regionArea = reader.start(self.root)

    def on_exit(self):
        print("退出程序")
        reader.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
