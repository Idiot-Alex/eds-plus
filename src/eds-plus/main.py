import threading
import tkinter as tk
from tkinter import messagebox
from Args import Args
from Eds import Eds
from playwright.sync_api import sync_playwright
from PIL import Image, ImageTk

def app():
  def url_entry_change(e):
    args.url = url_entry.get()

  def user_entry_change(e):
    args.user = user_entry.get()

  def pwd_entry_change(e):
    args.password = pwd_entry.get()

  def msg_entry_change(e):
    args.msg = msg_entry.get("1.0", tk.END)

  def checkbox_headless_change():
    args.headless = False if headless_var.get() == 1 else True

  def wright_eds_worker(eds, args):
    try:
      with sync_playwright() as playwright:
        eds.run(playwright, args)
    except Exception as e:
      print(f"An error occurred: {str(e)}")

  def exec_button_click():
    if (len(user_entry.get()) == 0):
      user_entry.focus_set()
      messagebox.showerror("错误", f"请输入用户名")
      return

    if (len(pwd_entry.get()) == 0):
      pwd_entry.focus_set()
      messagebox.showerror("错误", f"请输入密码")
      return

    exec_button.config(text="正在处理，请稍后", state=tk.DISABLED)
    root.update()

    eds = Eds()
    thread = threading.Thread(target=wright_eds_worker, args=(eds, args), name="thread-wright-eds")
    thread.start()
    thread.join()

    if (eds.code == 200):
      print(f"自动填写日志完成: {eds.msg}")
      messagebox.showinfo("信息", f"自动填写日志完成: {eds.msg}")
    else:
      print(f"自动填写日志失败: {eds.msg}")
      messagebox.showwarning("警告", f"自动填写日志失败: {eds.msg}")

    exec_button.config(text="开始自动填写 EDS 日志", state=tk.NORMAL)

  # main logic
  args = Args()
  root = tk.Tk()
  root.geometry("400x400")
  root.title("自动填写 EDS")

  frame = tk.Frame(root)
  frame.pack()

  url_label = tk.Label(frame, text="请输入 EDS 地址：", anchor=tk.E)
  url_label.grid(row=0, column=0, sticky=tk.NSEW)
  url_entry = tk.Entry(frame, width=30, textvariable=tk.StringVar(value=args.url))
  url_entry.bind("<KeyRelease>", url_entry_change)
  url_entry.grid(row=0, column=1)

  user_label = tk.Label(frame, text="请输入用户名：", anchor=tk.E)
  user_label.grid(row=1, column=0, sticky=tk.NSEW)
  user_entry = tk.Entry(frame, width=30)
  user_entry.bind("<KeyRelease>", user_entry_change)
  user_entry.grid(row=1, column=1)

  pwd_label = tk.Label(frame, text="请输入密码：", anchor=tk.E)
  pwd_label.grid(row=2, column=0, sticky=tk.NSEW)
  pwd_entry = tk.Entry(frame, width=30, show="*")
  pwd_entry.bind("<KeyRelease>", pwd_entry_change)
  pwd_entry.grid(row=2, column=1)

  msg_label = tk.Label(frame, text="请输入 EDS 内容：", anchor=tk.E)
  msg_label.grid(row=3, column=0, sticky=tk.NSEW)
  msg_entry = tk.Text(frame, width=30, height=3)
  msg_entry.insert(tk.END, args.msg)
  msg_entry.bind("<KeyRelease>", msg_entry_change)
  msg_entry.grid(row=3, column=1)

  headless_var = tk.IntVar()
  checkbox_headless = tk.Checkbutton(frame, text="显示执行过程", variable=headless_var, onvalue=1, offvalue=0, command=checkbox_headless_change)
  checkbox_headless.grid(row=4, column=0, columnspan=2)

  exec_button = tk.Button(frame, text="开始自动填写 EDS 日志", command=exec_button_click)
  exec_button.grid(row=5, column=0, columnspan=2)

  img = Image.open("src/eds-plus/assets/hotstrip.jpg")
  img = img.resize((200, 200), Image.Resampling.LANCZOS)
  photo = ImageTk.PhotoImage(img)
  img_label = tk.Label(frame, image=photo)
  img_label.image = photo
  img_label.grid(row=6, column=0, columnspan=2)

  root.mainloop()

if __name__ == "__main__":
  app()