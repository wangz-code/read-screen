import tkinter as tk
from tkinter import messagebox
import sys
class RegionSelector:
    @staticmethod
    def select_region(master):
        """
        全屏半透明选区，松开鼠标立即变为全透明并销毁，消除系统残影
        """
        root = tk.Toplevel(master)
        root.attributes('-topmost', True)
        # 原生TCL调用，修复 Mac 布尔值报错
        root.tk.call("wm", "overrideredirect", root._w, 1)

        # 全屏配置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        root.attributes('-alpha', 0.3)   # 初始半透明
        root.configure(bg='black')

        canvas = tk.Canvas(root, cursor="cross", bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        start_x = start_y = 0
        # 兜底初始化，防止直接点击不拖拽导致变量未赋值
        end_x = end_y = 0
        rect = None

        # 提示标签
        tip = tk.Label(
            root,
            text="1.按住鼠标左键拖拽以框选区域，松开即完成 \n\n2.手动ctrl+tab 切换回视频应用",
            font=("Arial", 25),
            bg="blue",
            fg="white",
            padx=10,
            pady=5,
            justify=tk.LEFT
        )
        tip.place(relx=0.5, rely=0.3, anchor="n")

        def on_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(
                start_x, start_y, start_x, start_y,
                outline='red', width=3, fill=''
            )

        def on_drag(event):
            canvas.coords(rect, start_x, start_y, event.x, event.y)

        def on_release(event):
            nonlocal end_x, end_y
            end_x, end_y = event.x, event.y
            print("event",event)
            # 异步销毁窗口
            root.after(10, root.destroy)

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        master.wait_window(root)
        print("mainloop")
        # 计算选区坐标与尺寸
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)
        width = x2 - x1
        height = y2 - y1

        if width < 50 or height < 20:
            messagebox.showwarning("区域太小", "选定区域过小，请至少 50x20 像素")
            return None

        return {
            "left": x1,
            "top": y1,
            "width": width,
            "height": height
        }