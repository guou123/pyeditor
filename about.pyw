# This Python file uses the following encoding: utf-8
from tkinter import Tk, Label
root = Tk()
root.title('信息')
title = Label(root, text='信息', font=('Microsoft yahei', 20, 'bold'))
msg1 = Label(root, text='开发者:狄锦灏')
msg2 = Label(root, text='电话:15722523345')
b = Label(root, text='版本:正式发布版 v3')
title.pack()
msg1.pack()
msg2.pack()
b.pack()
root.mainloop()
