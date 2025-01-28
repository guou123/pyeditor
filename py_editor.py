#!/usr/bin/python
# This Python file uses the following encoding: UTF-8
# 导入所需模块
import tkinter as tk
from traceback import format_exc
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkinter import ttk
from tkinter import simpledialog as sg
from _tkinter import TclError
from threading import Thread as Td
from pyttsx3 import speak
from os import startfile, system, getlogin as user_name
import platform
from time import strftime, localtime, time, sleep
from translate import Translator
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from PIL.Image import open as open_image
from PIL.ImageTk import PhotoImage
# from pyautogui import press
from sys import version, executable
# from win10toast import ToastNotifier
from webbrowser import open as url_open

# 标题
title = 'PyEditor'
__author__ = {'name': '狄锦灏',
              'Email': '3029769392@qq.com',
              'Blog': 'None',
              'QQ': '3029769392',
              'Created': '2023-01-16'}
__version__ = 20.0
__all__ = ['__author__', '__version__']
# 窗口参数
width = 600
height = 600
save_width = width
save_height = height


class Files:  # 定义文件基本参数
    """文件需要的所有参数都在这里"""
    encoding = 'UTF-8'
    initialdir = r'C:\\Users\Administrator\Desktop'
    fine_name = ''
    BEGIN = '1.0'
    END = tk.END

    def __init__(self):
        self.user = None
        self.p = None
        self.init_tf = False

    def init(self):
        self.__init__()
        print(platform.system())
        if platform.system() != 'Windows':
            mb.showwarning('警告', '软件部分功能仅能使用于Windows上')
            exit(1)
        self.init_tf = True
        self.user = ''
        self.p = '20140620'

    def login(self, password, user=user_name()):
        self.user = user
        print(self.user + ':' + password)
        if self.p == password and self.init_tf:
            print('注册成功')
            print('-' * 80)
        elif not self.init_tf:
            print('注册失败')
            print('未初始化')
            exit()
        else:
            print('注册失败')
            exit()


class Tk_Tool:
    QUIT = 'WM_DELETE_WINDOW'


class App(tk.Tk):
    print(tk.TkVersion)


class LoginError(BaseException):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text):
        """在工具提示窗口中显示文本"""
        if self.tip_window or not tip_text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        # 获取小部件的大小
        x = x + self.widget.winfo_rootx() + 25
        # 计算以显示工具提示
        y = y + cy + self.widget.winfo_rooty() + 25
        # 下方和右侧
        self.tip_window = tw = tk.Toplevel(self.widget)
        # 创建新的工具提示窗口
        tw.wm_overrideredirect(True)
        # 删除所有窗口管理器 （WM）
        tw.wm_geometry("+%d+%d" % (x, y))
        # 创建窗口大小

        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID,
                         borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class MenuBar(tk.Menu):
    pass


class Syntax_highlighting:
    def __init__(self, master):
        self.master = master

    @staticmethod
    def master_syntax_highlighting():
        global text_box
        percolator = Percolator(text_box)
        colordelgator = ColorDelegator()
        percolator.insertfilter(colordelgator)
        return


def pop_message(m_title, message):
    toaster = ToastNotifier()
    toaster.show_toast(m_title,
                       message,
                       icon_path="logos/logo.ico",
                       duration=5)
    sleep(0.5)
    messages.append(f'{m_title}:{message}')


def pop_win_message(m_title, message):
    mt = Td(target=pop_message, args=(m_title, message))
    mt.start()


def translate(word):  # 翻译
    translator = Translator(to_lang='chinese')
    translation = translator.translate(str(word))
    return translation


def enter():
    global runtf
    print('-' * len(executable) + '-')
    print(print_colour('30', 'Python ' + version))
    print(print_colour('32', 'Type "help", "copyright", "credits" or "license()" for more information.'))
    print(print_colour('33', copyright))
    print(print_colour('34', executable))
    print(f'进程已结束,运行代码{rv}')
    runtf = False


def print_colour(fg, text, m='0'):
    return_string = f"\033[{m};{fg}m{text}\033[m"
    return return_string


def cleared_text_box():  # 清空
    global text_box
    yn = mb.askyesnocancel('清空', '确定要清空吗?')
    if yn:
        text_box.delete(Files.BEGIN, Files.END)
    else:
        pass


def run_fine():  # 运行文件
    global rjsq
    global rv
    text = text_box.get(Files.BEGIN, Files.END)
    print(f'{rjsq}'.center(10, '-'))
    rjsq += 1
    rv += 1
    try:
        exec(text)
    except BaseException as e:
        ec = str(type(e)).replace("class", "").replace("<", "").replace(
            ">", "").replace("'", "")
        raise_error(f'错误信息:{ec}:{e},\n{format_exc()}\n错误类型:{ec}')


def save():  # 保存
    global root
    if file_path == '' or file_path is None:
        save_as()
    else:
        with open(file_path, 'r+') as f:
            f.truncate()
            f.write(text_box.get(Files.BEGIN, Files.END))


def open_():  # 打开
    global file_path
    global file_text
    global root
    global text_box
    global et
    file_path = filedialog.askopenfilename(title='选择文件', initialdir=Files.initialdir)
    if file_path is not None:
        try:
            with open(file=file_path, mode='r+', encoding=Files.encoding) as file:
                file_text = file.read()
        except FileNotFoundError:
            file_path = None
        except BaseException as e:
            raise_error('你打开的文件是不支持的格式,已损坏或无权限')
            file_path = None
            et = e
        finally:
            text_box.delete(Files.BEGIN, Files.END)
            text_box.insert(tk.INSERT, file_text)
    try:
        root.title(file_path + ' - ' + title)
    except TypeError:
        pass


def save_as():  # 另存为
    global filename
    newfilename = filedialog.asksaveasfilename(
        title='保存', initialdir=Files.initialdir, initialfile='%s' % Files.fine_name,
        filetypes=[('py', '.py'), ('pyw',
                                   '.pyw'), ('TXT', '.txt')])

    if newfilename:
        fp = open(newfilename, 'w')
        fp.write(text_box.get(Files.BEGIN, Files.END))
        fp.close()
        filename = newfilename

        textChanged.set(0)


def load_fine():  # 下载
    global filename
    if not filename:
        save_as()

    elif textChanged.get():
        fp = open(filename, 'w')
        fp.write(text_box.get(Files.BEGIN, Files.END))
        fp.close()
        textChanged.set(0)


def oa():  # 完成新建
    global new_fine_name_
    global new_fine_type_
    global file_path
    new_fine_name_ = new_fine_name_entry.get()
    new_fine_type_ = new_fine_type_entry.get()
    root.title(new_fine_name_ + '.' + new_fine_type_ + '-' + title)
    file_path = new_fine_name_ + '.' + new_fine_type_


def add_fine():  # 新建
    global root
    global new_fine_name_entry
    global new_fine_type_entry
    yn = mb.askyesnocancel('新建', '不要之前的了吗?')
    if yn:
        text_box.delete(Files.BEGIN, Files.END)
    else:
        pass
    new_fine_name_and_type_top = tk.Toplevel()
    new_fine_name_and_type_top.title('新建')
    new_fine_name_and_type_top.iconbitmap('logos/new_file.ico')
    y = tk.LabelFrame(new_fine_name_and_type_top, labelanchor='w', text='名称')
    new_fine_name_entry = ttk.Entry(y)
    z = tk.LabelFrame(new_fine_name_and_type_top, labelanchor='w', text='类型')
    new_fine_type_entry = ttk.Entry(z)
    oab = ttk.Button(new_fine_name_and_type_top, text='ok', command=oa)
    y.pack()
    new_fine_name_entry.pack()
    z.pack()
    new_fine_type_entry.pack()
    oab.pack()


def open_fine_in_window():  # 打开文件在explorer里
    filenames = filedialog.askopenfilename(title='打开', initialdir=Files.initialdir,
                                           initialfile='%s' % Files.fine_name)
    startfile(filenames)


def ld():  # 朗读
    ld_threading = Td(target=speak, args=(text_box.get(Files.BEGIN, Files.END), ))
    ld_threading.start()


def quit_window():  # 关闭窗口
    global quit_yesno
    if file_path:
        quit_yesno = mb.askyesnocancel('关闭', f'要保存你对{file_path}的更改吗?\n(下次开启可选择文件->还原,找回)')
    else:
        quit_yesno = mb.askyesnocancel('关闭', '要保存吗?\n(下次开启可选择文件->还原,找回)')
    if quit_yesno is True:
        save()
        with open('reducing.re', 'r+') as f:
            f.truncate()
            f.write(text_box.get(Files.BEGIN, Files.END))
        enter()
        root.quit()
        exit()
    elif quit_yesno is False:
        with open('reducing.inf', 'r+') as f:
            f.truncate()
            f.write(text_box.get(Files.BEGIN, Files.END))
        enter()
        root.quit()
        exit()
    else:
        pass


def python_help():
    url_open('https://docs.python.org/3.8/')


def callback1():  # 剪切
    global root
    text_box.event_generate('<<Cut>>')


def callback2():  # 复制
    global root
    text_box.event_generate('<<Copy>>')


def callback3():  # 粘贴
    global root
    text_box.event_generate('<<Paste>>')


def popup(event):  # 显示菜单
    pop_menu.post(event.x_root, event.y_root)  # post在指定的位置显示弹出菜单


def image():  # 加载图片
    file_name = filedialog.askopenfilename()
    photo = PhotoImage(open_image(file_name))
    text_box.image_create(tk.INSERT, image=photo)
    text_box.insert(tk.INSERT, '\n')


def printes():
    startfile('print.pyw')


def printf():  # 打印
    my_td = Td(target=printes)
    my_td.start()


def callback():  # 撤销
    text_box.edit_undo()


def select_all():  # 全选
    pass


def get_time():  # 获取时间
    msgs = strftime('%Y年%m月%d日 %H时%M分', localtime(time()))
    text_box.insert(tk.INSERT, msgs)


def abouts():
    startfile('about.pyw')


def about():  # 信息
    my_td = Td(target=abouts)
    my_td.start()


def helpes():
    startfile('help.pyw')


def helps():  # 帮助
    my_td = Td(target=helpes)
    my_td.start()


def ok_font():  # 确定字体
    global font_name, text_box
    font = font_name
    text_box['font'] = font


def wi_font():  # 设置字体
    global font_menu, font_name
    wi_top = tk.Toplevel()
    wi_top.title('字体')
    wi_top.iconbitmap('logos/wi_font.ico')
    font_menu = ttk.Combobox(wi_top, state='readonly', textvariable=font_name)
    ob = ttk.Button(wi_top, text='ok', command=ok_font)
    font_menu['value'] = list_
    font_menu.pack()
    ob.pack()


def command():  # 用于无效指令
    mb.showerror('无', '无状态栏')


def search():  # 搜索
    global start
    text_to_search = sg.askstring(title='搜索', prompt='搜索什么?')
    try:
        start = text_box.search(text_to_search, 0.0, Files.END)
    except TclError:
        pass
    finally:
        if start:  # 查找到时，返回yes
            mb.showinfo(title='发现', message='发现信息')
        else:
            mb.showinfo(title='未发现', message='未发现信息')


def go_to():  # 转到
    global row_entry, column_entry
    go_to_top = tk.Toplevel()
    go_to_top.iconbitmap('logos/go_to.ico')
    go_to_top.title('转到')
    row_frame = ttk.LabelFrame(go_to_top, labelanchor='w', text='行')
    row_entry = ttk.Entry(row_frame)
    column_frame = ttk.LabelFrame(go_to_top, labelanchor='w', text='列')
    column_entry = ttk.Entry(column_frame)
    ob = ttk.Button(go_to_top, text='ok', command=og)
    row_frame.pack()
    row_entry.pack()
    column_frame.pack()
    column_entry.pack()
    ob.pack()


def og():  # 完成转到
    global row_entry, column_entry
    row_ = int(row_entry.get())
    col_ = int(column_entry.get())
    k = '%d.%d' % (row_ + 1, col_ + 1)
    text_box.see(k)


def replacement():  # 替换
    global row_entry_
    global column_entry_
    global a
    replacement_top = tk.Toplevel()
    replacement_top.iconbitmap('logos/replacement.ico')
    replacement_top.title('替换')
    row_frame = ttk.LabelFrame(replacement_top, labelanchor='w', text='行')
    row_entry_ = ttk.Entry(row_frame)
    column_frame = ttk.LabelFrame(replacement_top, labelanchor='w', text='列')
    column_entry_ = ttk.Entry(column_frame)
    a = ttk.Entry(replacement_top)
    ob = ttk.Button(replacement_top, text='ok', command=ore)
    row_frame.pack()
    row_entry_.pack()
    column_frame.pack()
    column_entry_.pack()
    a.pack()
    ob.pack()


def ore():  # 完成替换
    global row_entry_, column_entry_, text_box, a, content, col, row
    try:
        row = int(row_entry_.get())
        col = int(column_entry.get())
        content = a.get()
    except ValueError:
        pass
    finally:
        text_box.insert(tk.INSERT, content)


def word_wrap():  # 自动换行
    if word_wrap_var.get() == 1:
        text_box['wrap'] = tk.WORD
    else:
        text_box['wrap'] = tk.NONE


def update():  # 刷新
    global root
    root.update()


def raise_error(text):  # 抛出异常
    mb.showerror('错误', text)


def reducing():  # 还原
    global text_box
    yn = mb.askyesnocancel('还原', '不要之前的了吗?')
    if yn:
        with open('reducing.inf', 'r+') as f:
            text = f.read()
            text_box.insert(1.0, text)
            f.truncate()
    else:
        pass


# 窗口尺寸调整处理函数
def window_resize(event):
    global save_width
    global save_height
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    if event.type == '22':
        if new_width == 1 and new_height == 1:
            return
        if save_width != new_width or save_height != new_height:
            text_box.config(width=new_width - 40, height=new_height - 60)
        save_width = new_width
        save_height = new_height


def syntax_highlighting():  # 语法高亮
    global root
    sh = Syntax_highlighting(root)
    sh.master_syntax_highlighting()


def oh():  # 完成设置字号任务
    global hyphen, sp
    hyphen = sp.get()
    text_box['font'] = ('Microsoft yahei', hyphen)


def wi_hyphen():  # 设置字号
    global sp
    global text_box
    wi_hyphen_top = tk.Toplevel()
    wi_hyphen_top.iconbitmap('logos/wi_font.ico')
    wi_hyphen_top.title('字号')
    sp = ttk.Spinbox(wi_hyphen_top, from_=5, to=30, command=oh, state='readonly')
    sp.set(hyphen)
    sp.pack()


def f_eleven(event):
    global root
    root.wm_state('zoomed')
    return event


def enter_terminal():
    system('start cmd.exe cmd /k cmd')


def enter_interactive_environment():
    system('start cmd.exe cmd /k python')


def enter_shell():
    system('start powershell.exe')


def idle():
    system('idle')


def enter_python_idle():
    my = Td(target=idle)
    my.start()


def times():
    startfile('time.pyw')


def look_time():
    ld_threading = Td(target=times)
    ld_threading.start()


def pri():
    startfile('cs.pyw')


def prosecutorial_network():
    my_td = Td(target=pri)
    my_td.start()


def esc():
    root.deiconify()


def main():
    global root
    global runtf
    papers.init()
    papers.login(user=user_name(), password='20140620')
    runtf = True
    pack_bj()
    root.mainloop()


def pack_bj():
    fm.pack()
    frm.pack()
    text_box.pack(fill=tk.BOTH, expand=True)


def new_win():
    startfile('new_win.pyw')


def new_kzt_win():
    startfile('py_editor1.py')


def create_tooltip(widget, text):
    tooltip = ToolTip(widget)

    def enters(event):
        tooltip.show_tip(text)
        return event

    def leave(event):
        tooltip.hide_tip()
        return event

    widget.bind('<Enter>', enters)
    widget.bind('<Leave>', leave)


# 创建主窗口
root = App(useTk=True, className='')
root.title(title)
hyphen = 10
et = ''
root.iconbitmap('logos/logo.ico')
g_screenwidth = root.winfo_screenwidth()
g_screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (g_screenwidth - width) / 2, (g_screenheight - height) / 2)
root.geometry(alignstr)
# 需要的参数
list_ = ['Microsoft yahei', 'Helvetica', 'Arial', 'TkFixedFont', '黑体']
messages = []
runtf = False
my_sp = ttk.Spinbox()
row_entry = ttk.Entry()
column_entry = ttk.Entry()
row_entry_ = ttk.Entry()
column_entry_ = ttk.Entry()
a = ttk.Entry()
new_fine_name_ = ''
new_fine_type_ = ''
new_fine_name_entry = ttk.Entry()
new_fine_type_entry = ttk.Entry()
mf = tk.Frame(root)
col = 0
row = 0
content = ''
start = ''
file_path = ''
file_text = ''
rjsq = 1
textChanged = tk.IntVar(value=0)
word_wrap_var = tk.IntVar(value=1)
rv = 0
filename = ''
font_menu = ''
sp = tk.Spinbox()
frm = tk.Frame(root)
fm = tk.Frame(root, width=22)
quit_yesno = ''
text_box = st.ScrolledText(frm, wrap=tk.WORD, undo=True, bd='0px', font=('Microsoft yahei', hyphen), cursor='xterm',)
# labztl = tk.Label(frm, text='人生苦短,我用python')
texts = text_box.get(Files.BEGIN, Files.END)
font_name = tk.StringVar()
xhx = [u'F̲', u'E̲', u'O̲', u'V̲', u'W̲', u'I̲', u'H̲']
papers = Files()  # 实例化文件
keywords = ['and', 'as', 'assert', 'break', 'class', 'continue'
                                                     'def', 'del', 'elif', 'else', 'except', 'finally',
            'for', 'from', 'False', 'global', 'if', 'import'
                                                    'in', 'is', 'lambda', 'nonlocal', 'not', 'None'
                                                                                             'or', 'pass', 'raise',
            'return', 'try', 'True'
                             'while', 'with', 'yield']
builtins = ["abs", "all", "any", "basestring", "bool",
            "callable", "chr", "classmethod", "cmp", "compile",
            "complex", "delattr", "dict", "dir", "divmod",
            "enumerate", "eval", "execfile", "exit", "file",
            "filter", "float", "frozenset", "getattr", "globals",
            "hasattr", "hex", "id", "int", "isinstance",
            "issubclass", "iter", "len", "list", "locals", "map",
            "max", "min", "object", "oct", "open", "ord", "pow",
            "property", "range", "reduce", "repr", "reversed",
            "round", "set", "setattr", "slice", "sorted",
            "staticmethod", "str", "sum", "super", "tuple", "type",
            "vars", "zip"]
constants = ["False", "True", "None", "NotImplemented",
             "Ellipsis"]
root_menu = MenuBar(root)
file_menu = tk.Menu(root_menu, tearoff=False)
# 添加下拉内容

file_menu.add_command(label="打开", command=open_, accelerator='Shift+O')
file_menu.add_command(label="保存", command=save, accelerator='Shift+S')
file_menu.add_command(label="新建", command=add_fine, accelerator='Shift+N')
# file_menu.add_command(label="新建窗口", command=new_win, accelerator='Shift+N+W')
new_win_menu = tk.Menu(file_menu, tearoff=False)
new_win_menu.add_command(label='新建窗口', command=new_win, accelerator='Shift+N+W')
new_win_menu.add_command(label='新建带控制台的窗口', command=new_kzt_win, accelerator='Shift+N+K')
file_menu.add_cascade(label="新建窗口", menu=new_win_menu)
file_menu.add_command(label="另存为", command=save_as, accelerator='Shift+L')
file_menu.add_command(label='默认打开', command=open_fine_in_window, accelerator='Shift+M')
file_menu.add_separator()
file_menu.add_command(label="运行", command=run_fine, accelerator='Shift+F10')
file_menu.add_command(label="打印", command=printf, accelerator='Shift+P')
file_menu.add_separator()
file_menu.add_command(label="退出", command=quit_window, accelerator='X')
file_menu.add_command(label='刷新', command=update, accelerator='F5')
file_menu.add_command(label='还原', command=reducing, accelerator='R')
root_menu.add_cascade(label=f"文件({xhx[0]})", menu=file_menu)
# 创建编辑菜单
editmenu = tk.Menu(root_menu, tearoff=False)

# 创建编辑下拉内容
editmenu.add_command(label="插入图片", command=image, accelerator='Ctrl+W')
editmenu.add_separator()
editmenu.add_command(label="全选", command=select_all, accelerator='Ctrl+A', state=tk.DISABLED)
editmenu.add_command(label="撤销", command=callback, accelerator='Ctrl+Z')
editmenu.add_command(label="剪切", command=callback1, accelerator='Ctrl+X')
editmenu.add_command(label="复制", command=callback2, accelerator='Ctrl+C')
editmenu.add_command(label="粘贴", command=callback3, accelerator='Ctrl+V')
editmenu.add_command(label="全选", command=select_all, accelerator='Ctrl+A')
editmenu.add_command(label='朗读', command=ld, accelerator='无')

editmenu.add_separator()
editmenu.add_command(label="查找", command=search, accelerator='Ctrl+S')
editmenu.add_command(label="插入", command=replacement, accelerator='Ctrl+I')
editmenu.add_command(label="转到", command=go_to, accelerator='Ctrl+G')
editmenu.add_separator()
editmenu.add_command(label="时间/日期", command=get_time, accelerator='Ctrl+T')

root_menu.add_cascade(label=f"编辑({xhx[1]})", menu=editmenu)

# 创建格式菜单
format_menu = tk.Menu(root_menu, tearoff=False)
format_menu.add_checkbutton(label="自动换行", command=word_wrap, accelerator='Ctrl+W', variable=word_wrap_var)
format_menu.add_command(label="字体", command=wi_font, accelerator='Ctrl+F')
format_menu.add_command(label="字号", command=wi_hyphen, accelerator='Ctrl+K')
root_menu.add_cascade(label=f"格式({xhx[2]})", menu=format_menu)

# 查看菜单
view_menu = tk.Menu(root_menu, tearoff=False)

view_menu.add_command(label="查看状态栏", command=command, accelerator='Ctrl+L')
view_menu.add_command(label="查看时间", command=look_time, accelerator='无')
root_menu.add_cascade(label=f"查看({xhx[3]})", menu=view_menu)
# 系统菜单
windows_menu = tk.Menu(root_menu, tearoff=False)

windows_menu.add_command(label='终端', command=enter_terminal, accelerator='cmd')
windows_menu.add_command(label='Shell', command=enter_shell, accelerator='无')
windows_menu.add_separator()
windows_menu.add_command(label='python交互环境', command=enter_interactive_environment, accelerator='无')
windows_menu.add_command(label='python idle', command=enter_python_idle, accelerator='无')
root_menu.add_cascade(label=f'系统({xhx[4]})', menu=windows_menu)
#  网络菜单
I_menu = tk.Menu(root_menu, tearoff=False)
I_menu.add_command(label='检查网络', command=prosecutorial_network)
root_menu.add_cascade(label=f'网络({xhx[5]})', menu=I_menu)

# 创建帮助菜单
help_menu = tk.Menu(root_menu, tearoff=False)

help_menu.add_command(label="查看帮助", command=helps, accelerator='Ctrl+H')
help_menu.add_command(label="python帮助手册", command=python_help, accelerator='Ctrl+H')
help_menu.add_separator()
help_menu.add_command(label="关于编辑器", command=about, accelerator='Ctrl+O')
root_menu.add_cascade(label=f"帮助({xhx[6]})", menu=help_menu)

pop_menu = tk.Menu(root, tearoff=False)

pop_menu.add_command(label='剪切(T)', command=callback1, accelerator='✂')
pop_menu.add_command(label='复制(C)', command=callback2, accelerator='📄')
pop_menu.add_command(label='粘贴(P)', command=callback3, accelerator='📋')
pop_menu.add_command(label='运行(R)', command=run_fine, accelerator='▶')
pop_menu.add_command(label='朗读(A)', command=ld, accelerator='😮')
pop_menu.add_command(label='保存(S)', command=save, accelerator='💾')
pop_menu.add_command(label='刷新(E)', command=update, accelerator='🔄')
# 语法高亮
syntax_highlighting()
# 定义窗口布局
root.config(menu=root_menu)
# 事件绑定
text_box.bind('<Button-3>', popup)
root.bind('<Configure>', window_resize)
root.bind('<F11>', f_eleven)
root.bind('<Control-KeyPress-Z>', callback)
root.protocol(Tk_Tool.QUIT, quit_window)
# 开启主循环
if __name__ == '__main__':
    main()
