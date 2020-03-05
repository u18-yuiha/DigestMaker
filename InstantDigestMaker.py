
from tkinter import *
from tkinter import messagebox
#エラーが出た時などの共通処理
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




import subprocess
import os
from moviepy import *
from moviepy.editor import *
import sys
import os.path
import pathlib
#from COMPONENT import *
#class versionの作成。
#一応成功した。
class DigestMaker:
    
    def __init__(self,path,output = None,threshold = -33,silence_section = 0.5):
        try:
            self.path = path
            self.output = output
            self.threshold = threshold
            self.silence_section = silence_section
            self.video = VideoFileClip(self.path)
        except OSError:
                showError("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
            
    
    def get_info(self):

        self.info = subprocess.run(["echo 'A'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
        self.info = subprocess.run(["ffmpeg","-vn" ,"-i", self.path, "-af",
                                f"silencedetect=noise={self.threshold}dB:d={self.silence_section}",
                                "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True,
                                text = True)
        
        # "-af", "silencedetect=noise=-33dB:d=0.6"オーディオの設定。ノイズのデシベルと、秒数の指定。
        
        self.info = str(self.info)
        
        return self.info
    def silence_detect(self,info):
        self.info = info
        lines = info.split('\\n')
        
        time_list =[]

        for line in lines:
            if "silencedetect" in line:
                words = line.split(" ")

                for i in range(len(words)):
                    if "silence_start" in words[i]:
                       
                        time_list.append(float(words[i+1].replace('\\r','')))
                    if "silence_end" in words[i]:
                        
                        time_list.append(float(words[i+1].replace('\\r','')))
                #inputが空だった場合、
            """
            if "No such file or directory" in line:
                print(">>動画を読み込めませんでした。パスが間違っている可能性があります。")
                print(">>Could not load video. The path may be wrong.")
                return False
            
            if  "does not contain any stream"in line:
                print(">>動画を読み込めませんでした。動画以外を入力している可能性があります。")
                print(">>Could not load video. You may have entered something other than a video.")
                return False
            """    
        self.starts_ends = list(zip(*[iter(time_list)]*2))
        #print(starts_ends)
        return self.starts_ends



    def using_parts(self,starts_ends):
        
        
        #動画の長さを図る
        duration = self.video.duration

        #５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
        self.merge_list = [[self.starts_ends[i][1],self.starts_ends[i + 1][0]] for i in range(len(self.starts_ends)) if i <= len(starts_ends) - 2]
        #音声の始まりが無音ではなかった場合,最初の部分をつける
        if self.starts_ends[0][0] != 0:
            self.merge_list.insert(0,[0,self.starts_ends[0][1]])
        #音声の終わりが無音ではなかった場合、最後の部分をつける

        if self.starts_ends[-1][1] <= int(duration):
            self.merge_list.insert(-1,[self.starts_ends[-1][1],int(duration)])
        return self.merge_list

    def concatenate_videos(self,merge_list):      
        clips = {}      
        count = 0

        for i in range(len(merge_list)):
            clips[count] = self.video.subclip(self.merge_list[i][0],self.merge_list[i][1])
            count += 1
        
        #listがたのから集合にclipsを入れていく
        videos = [clips[i] for i in range(count)]
        #concatenateで、それらを合体させていく
        result = concatenate(videos)
        #.write_videofileで合体させたものを動画として出力。
        result.write_videofile(self.output,fps = 20,preset = "ultrafast")


def run(path,output,threshold,silence_section):
    movie = DigestMaker(path,output = output,threshold = "-30",silence_section = "0.4")    
    try:
        info = movie.get_info()
    except OSError:
        showError("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
    else:
        pass
    info = movie.get_info()
    #print(movie.silence_detect(info))

    starts_ends = movie.silence_detect(info)
    if type(starts_ends) == bool:
        pass
    elif starts_ends == []:
        showError(">>無音区間の検出ができませんでした。スレッショルドなどの値を見直してみてください。")
        pass      

    else:
        #print(movie.using_parts(starts_ends))
        #print(starts_ends)
        try:
            merge_list = movie.using_parts(starts_ends)
            movie.concatenate_videos(merge_list)
        except OSError:
            showError("出力用のファイルのパスが間違っている可能性があります。")
        else:
            showInfo("動画出力が完了しました。")

import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfd


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_frame()
        self.create_input_label()
        self.create_input_btn()
        self.create_output_lbl()
        self.create_output_btn()
        self.create_thre_lbl()
        self.create_interval_lbl()
        self.create_main_btn()
        self.create_help_btn()
        self.create_entry1()
        self.create_entry2()
        self.create_lb()
        self.create_th_scrollbar()
        self.create_silence_lb()
        self.create_silence_scrollbar()
        self.create_explain_lbl()
        
     #frame
    def create_frame(self):
        self.frame1 = ttk.Frame(root)
        self.frame1['height'] = 300
        self.frame1['width'] = 600
        self.frame1['relief'] = 'ridge'
        self.frame1['borderwidth'] = 10
        self.frame1.grid() 
    #input label
    def create_input_label(self):
        self.input_lbl = tk.Label(root,text = '入力',width = 20,fg='#ff0000')
        self.input_lbl.place(x = 10, y = 100)

        #input 参照
    def create_input_btn(self):
        self.input_btn = tk.Button(root, text = '参照',bg = '#87cefa',command = self.input_open_file)
        self.input_btn.place(x = 550,y = 100)
        #output label
    def create_output_lbl(self):
        self.output_lbl = tk.Label(root,text = '出力',width = 20,fg='#ff0000')
        self.output_lbl.place(x = 10, y = 150)
        #output参照
    def create_output_btn(self):
        self.output_btn = tk.Button(root,text = '参照',bg = '#87cefa',command = self.output_open_file)
        self.output_btn.place(x = 550,y = 150)
        #threshold
    def create_thre_lbl(self):
        self.thre_lbl = tk.Label(root,text = '無音とみなす音量',bg = '#87cefa')
        self.thre_lbl.place(x = 100,y = 180)
        #無音区間
    def create_interval_lbl(self):
        self.interval_lbl = tk.Label(root,text = '無音とみなす区間',bg = '#87cefa')
        self.interval_lbl.place(x = 250,y = 180)
    #実行ボタン
    def create_main_btn(self):
        self.main_btn = tk.Button(root, text = '実行',bg = '#87cefa',width = 20,command = self.Execute)
        self.main_btn.place(x = 400,y = 230)
        #helpボタン
    def create_help_btn(self):
        self.help_btn = tk.Button(root,text = 'ヘルプ')
        self.help_btn.place(x= 550,y = 10)
        #文字入力するところ（入力）
    def create_entry1(self):
        self.entry1 = ttk.Entry(root ,width = 70) 
        self.entry1.place(x = 100,y = 100)
        #文字入力するところ（出力）
    def create_entry2(self):
        self.entry2 = ttk.Entry(root ,width = 70) 
        self.entry2.place(x = 100,y = 150)
    #スレッショルドのスクロールボックス
    def create_lb(self):
        th_listarray = [i for i in range(-45,-10)]
        threshold = tk.StringVar(value = th_listarray)
        self.lb = tk.Listbox(root, listvariable = threshold,width=10,height = 4)
        self.lb.bind('<<ListboxSelect>>',self.th_selected)
        self.lb.configure(selectmode = "single")
        self.lb.place(x = 100,y = 210)
    def create_th_scrollbar(self):
        self.th_scrollbar = ttk.Scrollbar(root,orient = tk.VERTICAL,command =  self.lb.yview)
        self.th_scrollbar.place(x = 80,y = 230)
        #無音区間のスクロールボックス
    def create_silence_lb(self):
        silence_list =  [i / 10 for i in range(1,51)]
        silence_list = tk.StringVar(value = silence_list)
        self.silence_lb = tk.Listbox(root, listvariable = silence_list,width=10,height = 4)
        self.silence_lb.bind('<<ListboxSelect>>', self.silence_selected)
        self.silence_lb.configure(selectmode = "single")
        self.silence_lb.place(x = 250, y = 210)
    def create_silence_scrollbar(self):
        self.silence_scrollbar = ttk.Scrollbar(root,orient = tk.VERTICAL ,command =  self.silence_lb.yview)
        self.silence_scrollbar.place(x = 230,y = 230)
        self.silence_lb['yscrollcommand'] = self.silence_scrollbar.set
        #説明のためのラベル
    def create_explain_lbl(self):
        self.explain_lbl = tk.Label(root,text = "動画を入力して、出力先を決めてください。\nスレッショルドは無音とみなす音量、\n無音区間は無音の部分が何秒続いたらカットするかを決めます")
        self.explain_lbl.place(x = 10, y = 10)
    
 
    #フォルダ検索
    def input_open_file(self):
        input_file = tkfd.askopenfilenames(filetypes = [('mp4','*.mp4'),('MOV','*.MOV')])
        input_file = ''.join(input_file)
        self.entry1.insert('end',input_file)
        self.input_path = self.entry1.get()
        print(self.input_path)
        #print(os.path.isfile(self.input_path))
        return self.input_path
    #ファイルの保存場所を表示。
    def output_open_file(self):
        output_file = tkfd.asksaveasfilename(filetypes= [('mp4','*.mp4')])
        output_file = ''.join(output_file)
        self.entry2.insert('end',output_file)
        self.entry2.insert('end','.mp4')
        self.output_path = self.entry2.get()
        #print(self.output_path)
        #print(os.path.exists(self.output_path))
        return self.output_path

    #スレッショルド（無音閾値）のリストボックスから値をとってくる
    def th_selected(self,th_event):
        #ここをforで回さないと、
        #tkinter.TclError: bad listbox index "": must be active, anchor, end, @x,y, or a numberが出る。
        #（理由不明）
        for item_index in self.lb.curselection() :   #indexを取得
            self.th_item = self.lb.get(item_index)
            #print(self.th_item)
            return self.th_item
    #無音区間のリストボックスから値をとってくる
    def silence_selected(self,silence_event):
            for item_index in self.silence_lb.curselection():    #indexを取得
                self.silence_item = self.silence_lb.get(item_index)
                #print(self.silence_item)
                return self.silence_item
    
    #def change(self,path):
        #self.path =  path.replace("\\","/")
        #return self.path
        
    def dir_for_check(self,path):
        lines = path.split("/")
        rm_file = "/" + lines[-1]
        self.check_dir = path.replace(rm_file,"")
        return self.check_dir

    def inputValidator(self,path):
        self.inputFlag = True
        judge_input = os.path.exists(path)
        if judge_input == False :
            showInfo("入力用のパスが間違っている可能性があります。")
            self.inputFlag = False
        return self.inputFlag

    def outputValidator(self,output):
        self.outputFlag = True
        judge_output = self.dir_for_check(output)
        if  judge_output == False:
            showInfo("出力用のフォルダのパスが間違っている可能性があります。")
            self.outputFlag = False
        return self.outputFlag

    

    def notExistValidator (self,output):
        self.notExistFlag = True
        judge_not_exist_output = os.path.exists(output)
        if  judge_not_exist_output == True:
            showInfo("出力用のファイルのパスが既に存在しています。")
            self.notExistFlag = False
        return self.notExistFlag

    def validator(self,input_path,output_path): 
        self.inputFlag =self.inputValidator(self.input_path)
        self.outputFlag = self.outputValidator(self.output_path)
        self.notExistFlag = self.notExistValidator(self.output_path)
        print(self.inputFlag)
        print(self.outputFlag)
        print(self.notExistFlag)
        self.validatorFlag = False
        if self.inputFlag == self.outputFlag == self.notExistFlag == True:
            self.validatorFlag = True
        #print(self.validatorFlag)
        return self.validatorFlag



    def Execute(self):
        #入力値の検査
        self.input_path = self.entry1.get()
        print(self.input_path)
        self.output_path = self.entry2.get()
        print(self.output_path)
        self.th_item = self.th_selected(self.lb)
        self.silence_item = self.silence_selected(self.silence_lb)
        print(self.th_item)
        print(self.silence_item)
        self.validatorFlag = self.validator(self.input_path,self.output_path)
        if self.validatorFlag == True :
            run(self.input_path,self.output_path,self.th_item ,self.silence_item)
        else:
            showInfo("処理を中止します。")
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DigestMaker")
    app = Application(master=root)
    app.mainloop()