import time
import tkinter as tk
import tkinter.ttk


def show():
    global lab, progressbarOne
    lab.grid(row=0, column=0)
    lab['text'] = '正在连接打印机'
    for i in range(100):
        # 每次更新加1
        progressbarOne['value'] = i + 1
        # 更新画面
        root.update()
        time.sleep(0.05)
    progressbarOne['value'] = 0
    lab['text'] = '获取文本'
    for i in range(100):
        # 每次更新加1
        progressbarOne['value'] = i + 1
        # 更新画面
        root.update()
        time.sleep(0.03)
    progressbarOne['value'] = 0
    progressbarOne.destroy()
    lab.destroy()
    button.destroy()
    root.destroy()
    from win32api import ShellExecute
    from win32print import GetDefaultPrinter
    ShellExecute(0, 'print', 'reducing.inf', '/d:"%s"' % GetDefaultPrinter(), '.', 0)


root = tk.Tk()
root.geometry('100x90')

progressbarOne = tkinter.ttk.Progressbar(root)
progressbarOne.grid(row=1, column=0)
lab = tk.Label(root)
# 进度值最大值
progressbarOne['maximum'] = 120
# 进度值初始值
progressbarOne['value'] = 0

button = tkinter.ttk.Button(root, text='打印', command=show, width=5)
button.grid(row=2, column=0)

root.mainloop()
