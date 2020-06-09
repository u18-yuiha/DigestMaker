import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfd
from PIL import Image, ImageTk

import COMPONENT.BasicErrorComponent as BEC
import LOGIC.DigestMaker as DM

def input_validator(input_path):
    input_flag = True
    if os.path.exists(input_path) == False:
        BEC.show_error("入力用のパスが間違っている可能性があります。")
        input_flag = False
    return input_flag

def output_validator(output_path):
    lines = output_path.split("/")
    rm_file = "/" + lines[-1]
    check_dir = output_path.replace(rm_file,"")
    output_flag = True
    if os.path.isdir(check_dir) == False:
        BEC.show_error("出力用のフォルダのパスが間違っている可能性があります。")
        output_flag = False
    return output_flag

def th_validator(threshold):
    th_flag = True
    try:
        threshold = int(threshold)
    except ValueError:
        BEC.show_error("-45~-10までの整数を入力してください（半角英数)")
        th_flag = False
    
    else: 
        if threshold < -100 or -10 < threshold:
            BEC.show_error("-100~-10までの整数を入力してください（半角英数)")
            th_flag = False
    
    finally:
        return th_flag

def silence_validator(silence):
    silence_flag = True
    try:
        silence = float(silence)
    except ValueError:
        BEC.show_error("0.1~3.0までの、小数点第一位までを入力してください（半角英数）")
        silence_flag = False
    else:
        silence_list = [i / 10 for i in range(1,30,1)]
        if not silence in silence_list:
            BEC.show_error("0.1~3.0までの、小数点第一位までを入力してください（半角英数）")
            silence_flag = False
    
    finally:
        return silence_flag

def measure_threshold(input_entry,th_entry):
    input_path = input_entry.get()
    input_flag = input_validator(input_path)
    if input_flag == True:
        mean_volume = DM.mean_volume_detect(input_path)
        BEC.show_info(f"この動画の平均音量は約{mean_volume}dbです。\nスレッショルドは{mean_volume - 4}をお勧めします。")
        th_entry.insert('end', mean_volume - 4)
    


class Input_path:
    def __init__ (self,input_entry):
        self.input_entry = input_entry

    def __call__ (self,input_entry):
        self.input_entry.delete(0,tk.END)
        input_file = tkfd.askopenfilenames(filetypes = [
            ('mp4','*.mp4'),('MOV','*.MOV'),('webm','*.webm'),('flv','*.flv'),('AMV','*.AMV')])
        input_file = ''.join(input_file)
        self.input_entry.insert('end',input_file)

class Output_path:
    def __init__ (self,output_entry):
        self.output_entry = output_entry

    def __call__ (self,output_entry):
        self.output_entry.delete(0,tk.END)
        f_type =  [
            ('mp4','*.mp4'),('MOV','*.MOV'),('webm','*.webm'),('flv','*.flv'),('AMV','*.AMV')]
        output_file = tkfd.asksaveasfilename(filetypes= f_type,defaultextension = 'mp4' )
        output_file = str(output_file)
        self.output_entry.insert('end',output_file)

class Execute:
    def __init__ (self,input_entry,output_entry,th_entry,silence_entry):
        self.input_entry = input_entry
        self.output_entry = output_entry
        self.th_entry = th_entry
        self.silence_entry = silence_entry

    #def __call__(self,input_entry,output_entry,th_entry,silence_entry):
        
        self.input_path = self.input_entry.get()
        self.output_path = self.output_entry.get()
        self.threshold = self.th_entry.get()
        self.silence = self.silence_entry.get()

        self.input_flag = input_validator(self.input_path)
        self.output_flag = output_validator(self.output_path)
        self.th_flag = th_validator(self.threshold)
        self.silence_flag = silence_validator(self.silence)

        if self.input_flag == self.output_flag == self.th_flag == self.silence_flag == True:
            DM.run(self.input_path,self.output_path,self.threshold,self.silence)
        else:
            BEC.show_info("処理を中止します。")

def show_help():
    pass
    
   


if __name__ == "__main__":
    import tkinter
    import tkinter.filedialog

    class Application(tkinter.Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.master.title('tkinter dialog trial')
            self.pack()
            self.create_widgets()

        def create_widgets(self):
            self.dialog_button = tkinter.Button(self, text='Save File As ...', command=file_open, width=120)
            self.dialog_button.pack(anchor=tkinter.NW)

            self.text_1 = tkinter.StringVar()
            self.type_label = tkinter.Label(self, textvariable=self.text_1)
            self.type_label.pack(anchor=tkinter.W)
            self.text_2 = tkinter.StringVar()
            self.content_label = tkinter.Label(self, textvariable=self.text_2)
            self.content_label.pack(anchor=tkinter.W)

    def file_open():
        f_type = [('Text', '*.txt'), ('Markdown', '*.md'),('mp4','*.mp4')]
        ini_dir = 'C:\\temp'
        #defaultextensionでファイル端子も表現できる。
        ret = tkinter.filedialog.asksaveasfilename(defaultextension='txt' , filetypes=f_type , initialdir=ini_dir, title='file dialog test')
        app.text_1.set('Type : ' + str(type(ret)))
        app.text_2.set('Content : ' + str(ret))

    root = tkinter.Tk()
    app = Application(master=root)
    app.mainloop()
    silence_list = ([i / 10 for i in range(1,31,1)])
    a = 2.03
    if not a in silence_list:
        print("error")
    else:
        print("ok") 
