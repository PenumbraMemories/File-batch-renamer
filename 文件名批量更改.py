import os
import tkinter as tk
from tkinter import filedialog, messagebox, END
from tkinter import ttk
import sys

def exit_program():
    """退出整个程序"""
    sys.exit()

def rename_selected_files():
    """重命名选中的文件"""
    selected_files = [file_listbox.get(i) for i in file_listbox.curselection()]
    old_string = old_string_entry.get()
    new_string = new_string_entry.get()
    delete_string = delete_string_entry.get()

    if not old_string or not new_string:
        messagebox.showwarning("警告", "请输入要替换的字符串和新字符串。")
        return

    for filename in selected_files:
        old_file_path = os.path.join(folder_path, filename)
        new_filename = filename.replace(old_string, new_string)
        new_filename = new_filename.replace(delete_string, "")
        new_file_path = os.path.join(folder_path, new_filename)
        try:
            os.rename(old_file_path, new_file_path)
        except Exception as e:
            messagebox.showerror("错误", f"重命名文件 {filename} 时出错：{e}")
        else:
            print(f"将文件名 {filename} 替换为 {new_filename}")

    messagebox.showinfo("完成", "文件重命名完成。")

def select_folder_and_show_files():
    """选择文件夹并显示文件"""
    global folder_path
    folder_path = filedialog.askdirectory(title="选择文件夹")
    if not folder_path:
        return

    file_listbox.delete(0, END)
    file_types_set.clear()  # 清空文件类型集合
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_listbox.insert(END, filename)
            # 提取文件扩展名并添加到集合
            file_extension = os.path.splitext(filename)[1]
            if file_extension:
                file_types_set.add(file_extension)

    # 更新文件类型按钮
    update_file_type_buttons()

def show_instructions():
    """显示工具使用说明"""
    instructions = (
        "文件批量改名工具使用说明：\n\n"
        "1. 点击“选择文件夹”按钮，选择需要批量改名的文件所在的文件夹。\n"
        "2. 在输入框中输入要替换的字符串、新的字符串以及要删除的字符。\n"
        "3. 选中需要改名的文件，点击“重命名选中的文件”按钮。\n"
        "4. 工具会自动批量修改文件名。\n\n"
        "注意：\n"
        "- 请确保输入的字符串正确无误。\n"
        "- 如果遇到问题，请检查文件权限或联系开发者2195786717@qq.com。"
    )
    messagebox.showinfo("使用说明", instructions)

def update_file_type_buttons():
    """根据文件类型动态生成按钮"""
    for widget in file_type_frame.winfo_children():
        widget.destroy()  # 清空之前的按钮

    selected_file_types.clear()  # 清空选中的文件类型
    for file_type in sorted(file_types_set):
        btn = ttk.Button(file_type_frame, text=file_type, command=lambda ft=file_type: toggle_file_type_selection(ft))
        btn.pack(pady=2)

    # 更新文件列表框背景色
    update_file_colors()

def toggle_file_type_selection(file_type):
    """切换文件类型的选中状态"""
    if file_type in selected_file_types:
        selected_file_types.remove(file_type)
    else:
        selected_file_types.add(file_type)

    # 更新文件列表框背景色
    update_file_colors()

def update_file_colors():
    """根据选中的文件类型更新文件列表框中的背景颜色"""
    for idx, filename in enumerate(file_listbox.get(0, END)):
        file_extension = os.path.splitext(filename)[1]
        if file_extension in selected_file_types:
            file_listbox.itemconfig(idx, background="lightblue")  # 设置选中的文件背景为浅蓝色
        else:
            file_listbox.itemconfig(idx, background="white")  # 恢复未选中的文件背景为白色

# 初始化全选状态变量
is_all_selected = False

def toggle_select_all_files():
    """切换全选和取消全选状态"""
    global is_all_selected
    if is_all_selected:
        # 取消全选
        file_listbox.selection_clear(0, END)  # 取消所有选中
        for idx in range(file_listbox.size()):
            file_listbox.itemconfig(idx, background="white")  # 恢复背景色为白色
        is_all_selected = False
    else:
        # 全选
        file_listbox.select_set(0, END)  # 选中所有文件
        for idx in range(file_listbox.size()):
            file_listbox.itemconfig(idx, background="lightblue")  # 设置背景色为浅蓝色
        is_all_selected = True

def change_theme(event):
    """更改界面主题"""
    selected_theme = theme_combobox.get()
    style.theme_use(selected_theme)
    # 重新应用字体样式，确保字体大小保持一致
    style.configure("TLabel", font=("Georgia", 12), background="white")
    style.configure("TButton", font=("Georgia", 12), background="white")
    style.configure("TEntry", font=("Georgia", 12), fieldbackground="white")

# 创建主窗口
root = tk.Tk()
root.title("音符文件批量改名工具")
root.geometry("800x450")  # 调整窗口宽度以容纳文件类型按钮
root.configure(bg="white")  # 设置窗口背景颜色

# 使用 ttk.Style 设置样式
style = ttk.Style()
style.theme_use("alt")  # 默认主题为 "alt"

style.configure("TLabel", font=("Georgia", 12), background="white")
style.configure("TButton", font=("Georgia", 12), background="white")
style.configure("TEntry", font=("Georgia", 12), fieldbackground="white")

# 创建并放置标签和输入框
tk.Label(root, text="要替换的字符串：", font=("Georgia", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
old_string_entry = ttk.Entry(root)
old_string_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(root, text="新的字符串：", font=("Georgia", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
new_string_entry = ttk.Entry(root)
new_string_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

tk.Label(root, text="要删除的字符：", font=("Georgia", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
delete_string_entry = ttk.Entry(root)
delete_string_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# 创建文件列表框
file_listbox = tk.Listbox(root, selectmode='multiple', width=50, height=15)
file_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# 创建文件类型按钮区域
file_type_frame = tk.Frame(root, bg="white", width=200)
file_type_frame.grid(row=4, column=2, padx=10, pady=5, sticky="nsew")

# 创建全选按钮
select_all_button = ttk.Button(root, text="全选", command=toggle_select_all_files)
select_all_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

# 创建并放置按钮
select_folder_button = ttk.Button(root, text="选择文件夹", command=select_folder_and_show_files)
select_folder_button.grid(row=3, column=0, pady=10)

rename_button = ttk.Button(root, text="重命名选中的文件", command=rename_selected_files)
rename_button.grid(row=3, column=1, pady=10)

# 添加说明按钮
instructions_button = ttk.Button(root, text="说明", command=show_instructions)
instructions_button.grid(row=6, column=0, columnspan=2, pady=10)

# 添加主题选择下拉框
ttk.Label(root, text="选择界面主题：").grid(row=7, column=0, padx=10, pady=5, sticky="w")
theme_combobox = ttk.Combobox(root, values=style.theme_names(), state="readonly")
theme_combobox.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
theme_combobox.set("alt")  # 设置默认主题为 "alt"
theme_combobox.bind("<<ComboboxSelected>>", change_theme)

# 调整窗口布局
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

# 初始化文件类型集合和变量
file_types_set = set()
selected_file_types = set()

# 运行主循环
root.mainloop()