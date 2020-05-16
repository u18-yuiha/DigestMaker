
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#エラーが出た時などの共通処理

def auth():
    auth_flag = False
    auth_password = auth_entry.get()
    if auth_password == 'student2020VV':
        showInfo('プログラムを起動します')
        auth_flag = True
        auth_root.destroy()
    else:
        showError('パスワードが違います')
    return auth_flag
def showError(msg : str):
    tk = Tk()
    tk.withdraw()
    messagebox.showerror("エラー",msg)
    tk.destroy()

def showInfo(msg : str):
    tk = Tk()
    tk.withdraw()
    messagebox.showinfo("お知らせ",msg)
    tk.destroy()
auth_root = tk.Tk()
auth_root.title('パスワードを入力してください。')
auth_entry = ttk.Entry(auth_root,width = 60)
auth_entry.grid()
auth_button = ttk.Button(auth_root,text = 'OK',command = auth)
auth_button.grid()
auth_root.mainloop()




    

    
