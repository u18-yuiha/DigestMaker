import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfd
from PIL import Image, ImageTk
import sys
import COMPONENT.BasicErrorComponent as BEC
import LOGIC.DigestMaker as DM

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
    th_entry.delete(0,tk.END)
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
            ('mp4','*.mp4'),('webm','*.webm')]
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



        
class Help():
    def __init__ (self,root):
        self.window = None
        self.root = root
    
    def create_dialog (self):
        self.window = tk.Toplevel(self.root)
        self.window.title("ヘルプ")
        self.window.geometry("600x400") # 画面サイズを1000 x 1000 とする 
        # 画像を指定    
        self.img = Image.open(resource_path('helpImage.png'))
        
        w = self.img.width # 横幅を取得                                        
        h = self.img.height # 縦幅を取得                                                  
        self.img = self.img.resize(( int(w * (600/w)), int(h * (500/w)) ))
        self.img = ImageTk.PhotoImage(self.img)
        # canvasサイズも画面サイズと同じにして描画                                      
        canvas = tk.Canvas(self.window,width=600, height=200)
        canvas.grid(row = 0,sticky = tk.NW)
        # -------------------------------------                                         
        # キャンバスに画像を表示する                                                    
        canvas.create_image(0, 0, image=self.img, anchor=tk.NW)

        help_label = tk.Label(self.window,text = "➀ 参照ボタン（入力用）を押して、カットしたい動画を選択します。")
        help_label.grid(row = 1,sticky = tk.NW)
        help_label2 = tk.Label(self.window,text = "➁ 参照ボタン（出力用）を押して、出力先のフォルダとファイル名を入力します。")
        help_label2.grid(row = 2,sticky = tk.NW)
        help_label3 = tk.Label(self.window,text= "➂ スレッショルド計測ボタンを押します。お勧めのスレッショルド値が自動で入力されます。")
        help_label3.grid(row = 3,sticky = tk.NW)
        help_label4 = tk.Label(self.window,text= "➃ 無音区間入力欄に、スレッショルド以下の音量が何秒続いたらカットするかを入力します。（半角英数）")
        help_label4.grid(row = 4,sticky = tk.NW)
        help_label4_ex = tk.Label(self.window,text = "(0.2~0.4：よく見るカット編集、0.5～1.0:一人語りだと自然。1.0~:二人以上の会話、会議などに）")
        help_label4_ex.grid(row = 5,sticky = tk.NW)
        help_label5 = tk.Label(self.window,text = "➄ 実行ボタンを押します。しばらく反応がない状態になりますが裏でプログラムが働いています。そのままお待ちください。")
        help_label5.grid(row = 6,sticky = tk.NW)
        help_label5_ex = tk.Label(self.window,text = "起動したときに一緒に出てくる黒い画面を見ると、処理の進捗が見れます。")
        help_label5_ex.grid(row = 7,sticky = tk.NW)
        help_label6 = tk.Label(self.window,text = "さらに詳しい操作方法の解説はこちら",pady = 5,relief = "groove")
        help_label6.grid(row = 8,sticky = tk.NW)
        help_label6_ex = tk.Text(self.window)
        help_label6_ex.insert('end',"https://youtu.be/wZ9KjdwX-9Q")
        help_label6_ex.grid(row = 9,sticky = tk.NW)   
        self.window.lift()

    def __call__(self,root):
        if self.window == None:
            self.create_dialog()
            return
        try:
            self.window.lift()
        except tk.TclError:
        #window was closed, create a new one.
            self.create_dialog()
        


if __name__ == "__main__":
    import tkinter
    import tkinter.filedialog
