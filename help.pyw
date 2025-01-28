# This Python file uses the following encoding: UTF-8
from tkinter import Tk, Label
from PIL import ImageTk, Image
root = Tk()
root.title('帮助')
title = Label(root, text='帮助', font=('Microsoft yahei', 20, 'bold'))
image = Image.open('help.png')
msg = ImageTk.PhotoImage(image)
msg1 = Label(root, image=msg)
msg2 = Label(root, text='A.菜单栏,所有的功能都在这')
msg3 = Label(root, text='B.编辑框,任意编辑内容')
title.pack()
msg1.pack()
msg2.pack()
msg3.pack()
root.mainloop()
