import tkinter as tk
import CONTROLLER.DigestMakerExecutor as DME

class Create:
    def __init__(self,root):
        self.root = root
    def create_frame(self,root):
        self.basic_frame = tk.Frame(root)
       
        #self.basic_frame['height'] = 300
        #self.basic_frame['width'] = 600
        self.basic_frame['relief'] = 'ridge'
        self.basic_frame['borderwidth'] = 5
        self.basic_frame.pack(expand = 1)
        return self.basic_frame

    def create_input_label(self,basic_frame):
        self.input_label = tk.Label(self.basic_frame,text = '入力',fg = '#ff0000')
        self.input_label.grid(row = 1,column = 0)
    
    def create_output_label(self,basic_frame):
        self.output_label = tk.Label(self.basic_frame,text = "出力",fg = '#ff0000')
        self.output_label.grid(row = 2,column = 0)

    def create_th_label(self,basic_frame):
        self.th_label = tk.Label(self.basic_frame,text = "スレッショルド",fg = '#ff0000',bg = '#87cefa')
        self.th_label.grid(row = 3,column = 1)
    
    def create_silence_label(self,basic_frame):
        self.silence_label = tk.Label(self.basic_frame,text = "無音区間",fg = '#ff0000',bg = '#87cefa')
        self.silence_label.grid(row = 3,column = 2)
    
    def create_explain_label(self,basic_frame):
        self.explain_label = tk.Label(self.basic_frame,
                                        text ="動画を入力して、出力先を決めてください。\nスレッショルドは無音とみなす音量、\n無音区間は無音の部分が何秒続いたらカットするかを決めます"
                                         )
        self.explain_label.grid(row = 0,column = 0,columnspan = 3)

    def create_input_entry(self,basic_frame):
        self.input_entry = tk.Entry(self.basic_frame)
        self.input_entry.grid(row = 1,column = 1,columnspan = 2,sticky = tk.W + tk.E)

    def create_output_entry(self,basic_frame):
        self.output_entry = tk.Entry(self.basic_frame)
        self.output_entry.grid(row = 2,column = 1,columnspan = 2,sticky = tk.W + tk.E)
    
    def create_th_entry(self,basic_frame):
        self.th_entry = tk.Entry(self.basic_frame)
        self.th_entry.grid(row = 4,column = 1,sticky = tk.N)

    def create_silence_entry(self,basic_frame):
        self.silence_entry = tk.Entry(self.basic_frame)
        self.silence_entry.grid(row = 4,column = 2,sticky = tk.N)

    def create_help_button(self,basic_frame):
        self.help_button = tk.Button(self.basic_frame)
        self.help_button['text'] = "ヘルプ"
        self.help_button.bind("<Button-1>",DME.show_help())
        self.help_button.grid(row = 0,column = 3,padx = 10)

    def create_input_button(self,basic_frame):
        self.input_button = tk.Button(self.basic_frame)
        self.input_button['text'] = "参照"
        self.input_button.bind("<Button-1>",DME.Input_path(self.input_entry))
        self.input_button.grid(row = 1,column = 3,pady = 5)

    def create_output_button(self,basic_frame):
        self.output_button = tk.Button(self.basic_frame)
        self.output_button['text'] = "参照"
        self.output_button.bind("<Button-1>",DME.Output_path(self.output_entry))
        self.output_button.grid(row = 2,column = 3)

    def create_execute_button(self,basic_frame):
        self.execute_button = tk.Button(self.basic_frame)
        self.execute_button['text'] = "実行"
        #self.entry_list = [self.input_entry,self.output_entry,self.th_entry,self.silence_entry]
        self.execute_button['command'] = lambda input_entry = self.input_entry ,output_entry = self.output_entry,th_entry = self.th_entry ,silence_entry = self.silence_entry   :DME.Execute(input_entry,output_entry,th_entry,silence_entry)
        self.execute_button.grid(row = 4,column = 3)

    def create_th_measure_button(self,basic_frame):
        self.th_measure_button = tk.Button(self.basic_frame)
        self.th_measure_button['text'] = "スレッショルド計測"
        self.th_measure_button['command'] = lambda input_entry = self.input_entry , th_entry = self.th_entry :DME.measure_threshold(input_entry,th_entry)
        self.th_measure_button.grid(row = 4,column = 0)

if __name__ == "__main__":
    
    class Application(tk.Frame):
        def __init__(self,root):
            super().__init__(root)
            self.pack(expand = 1)
            Main = Create(root)
            self.frame = Main.create_frame(root)
            Main.create_input_label(self.frame)
            Main.create_output_label(self.frame)
            Main.create_th_label(self.frame)
            Main.create_silence_label(self.frame)
            Main.create_explain_label(self.frame)
            Main.create_input_entry(self.frame)
            Main.create_output_entry(self.frame)
            Main.create_th_entry(self.frame)
            Main.create_silence_entry(self.frame)
            Main.create_help_button(self.frame)
            Main.create_input_button(self.frame)
            Main.create_output_button(self.frame)
            Main.create_execute_button(self.frame)

    root = Application(tk.Tk())
    root.mainloop()
    

