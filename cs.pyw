# This Python file uses the following encoding: UTF-8
import subprocess
from tkinter import Tk, Text, INSERT, DISABLED, Scrollbar


def run_ping_command():
    # 配置STARTUPINFO以隐藏CMD窗口
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    # 使用subprocess.Popen而不是subprocess.run，因为我们需要传递startupinfo
    # 但是，为了简化，我们仍然可以捕获输出，只是需要稍微不同的方法
    process = subprocess.Popen(
        ['ping', 'baidu.com'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # 等待进程完成并获取输出
    stdout, stderr = process.communicate()

    # 检查是否有错误输出
    if stderr:
        return f"Error occurred:\n{stderr}"
    else:
        return stdout


def main():
    root = Tk()
    root.title('Ping Result')

    text_area = Text(root, wrap='word')
    scrollbar = Scrollbar(root, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    text_area.pack(expand=1, fill='both')

    output = run_ping_command()
    text_area.insert(INSERT, output)
    text_area.config(state=DISABLED)

    root.mainloop()


if __name__ == "__main__":
    main()