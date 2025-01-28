import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tfg
import tkinter.messagebox as msgbox
from webbrowser import open as open_url

code = ''
a = ''


def aclr(a):
    wt.config(fg='skyblue')


def bclr(b):
    wt.config(fg='blue')


def hyperlinks(master, text, url):
    global wt

    def cd(event):
        open_url(url)
        return event

    wt = tk.Label(master, text=text)
    wt.config(font=("microsoft yahei", 10, "underline"), fg='blue')
    wt.bind('<Button-1>', cd)
    wt.bind('<Enter>', aclr)
    wt.bind('<Leave>', bclr)
    return wt


def set_code():
    global code, path, a
    a = tfg.askopenfilename(title='打开', filetypes=[('PeIns', '.peins')])
    with open(a, encoding='utf-8') as f:
        code = f.read()
    path.configure(text=a)


def install_ins():
    n, p = tuple(code.split('║'))
    with open(f'software_library_is_installed\\{n}.pyw', 'w', encoding='utf-8') as f:
        f.write(p)
    msgbox.showinfo('安装', '安装成功!')


r = tk.Tk()
path = ttk.Label(r, text=a)
ou = hyperlinks(r, '插件包下载\n提取码:wnKr\n注意!Microsoft\n会报错不安全，\n请忽略', 'https://www.123684.com/s/ul18Td-ZTOod?')
open_ins = ttk.Button(r, text='打开插件包', command=set_code)
install_ins_b = ttk.Button(r, text='安装(I)', command=install_ins)
path.grid(row=0, column=1)
open_ins.grid(row=0, column=0)
install_ins_b.grid(row=1, column=1)
ou.grid(row=1, column=0)
r.mainloop()
