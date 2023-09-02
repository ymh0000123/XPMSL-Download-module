import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import requests
import os

version= "V1.0"

# 函数，用于执行下载操作
def download_file(status_label):
    selected_file = file_listbox.get(tk.ACTIVE)
    if not selected_file:
        return

    # 获取选定文件的URL
    file_url = file_info_dict[selected_file]

    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_name = os.path.basename(file_url)
            # 获取当前工作目录
            current_directory = os.getcwd()
            # 创建目标文件夹（如果不存在）
            target_folder = os.path.join(current_directory, "Download")
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            status_label.config(text=f"文件 {file_name} 已成功下载到 {file_path}")

            # 下载成功时显示弹窗提示
            messagebox.showinfo("下载成功", f"文件 {file_name} 已成功下载到 {file_path}")
        else:
            status_label.config(text=f"下载失败，HTTP状态码: {response.status_code}")
    except Exception as e:
        status_label.config(text=f"下载发生错误: {str(e)}")

# 函数，用于解析文件列表
def parse_file_list(file_content):
    file_info_dict = {}
    lines = file_content.split("\n")
    for line in lines:
        if line.strip():  # 忽略空行
            parts = line.split("](")
            if len(parts) == 2:
                file_name = parts[0].strip("[").strip()
                file_url = parts[1].strip(")").strip()
                file_info_dict[file_name] = file_url
    return file_info_dict

# 创建主窗口
root = tk.Tk()
root.title("下载模块")

# 设置窗口大小
root.geometry("439x455")

# 创建一个Frame用于容纳文件列表框和滚动条
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# 创建滚动条
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 创建文件列表框，并设置可见行数
file_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
file_listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=file_listbox.yview)
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("关于")

    about_label = ttk.Label(about_window, text="Xiaofeishu Python Minecraft Server Launcher(XPMSL) 下载模块 "+version+"\n作者: 没用的小废鼠\n程序免费开源,但是要遵守 GPL-3.0 license")
    about_label.pack(padx=20, pady=20)
# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_bar.add_cascade(label="关于", command=open_about_window)

# 获取文件列表内容
url = "https://github.moeyy.xyz/https://raw.githubusercontent.com/ymh0000123/XPMSL/main/announcement/list.txt"
response = requests.get(url)

if response.status_code == 200:
    file_content = response.text
    file_info_dict = parse_file_list(file_content)
    # 将文件名添加到列表框中
    for file_name in file_info_dict.keys():
        file_listbox.insert(tk.END, file_name)
else:
    messagebox.showerror("错误", f"无法获取文件列表，HTTP状态码: {response.status_code}")

# 创建下载按钮，并传递status_label作为参数
download_button = tk.Button(root, text="下载文件", command=lambda: download_file(status_label))
download_button.pack()

# 创建状态标签
status_label = tk.Label(root, text="")
status_label.pack()

# 运行GUI应用
root.mainloop()
