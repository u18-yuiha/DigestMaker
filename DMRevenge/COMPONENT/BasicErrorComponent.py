
from tkinter import messagebox

def show_info(msg :str):
    messagebox.showinfo("お知らせ",msg)

def show_error(msg :str):
    messagebox.showerror("エラー",msg)
