import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox as mx
import ctypes

# 告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


def install():
    global z
    d = z.get()
    f = os.popen('pip install ' + d)
    b = f.readlines()
    c = ''
    for q in b:
        c = c + q
    mx.showinfo('y', c+'\n安装成功')


def install_():
    os.system(r'.\install_config\install.bat')
    mx.showinfo('y', '安装成功')


root = tk.Tk()
a = ttk.Button(root, text='安装', command=install)
x = ttk.Button(root, text='一键补齐运行库', command=install_)
z = ttk.Entry()
z.pack()
a.pack()
x.pack()
root.mainloop()
