import tkinter as tk
import VIEW
import VIEW.Main as vMain
#import AuthID

class Application(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        root.title("DigstMaker")
        self.pack
        Main = vMain.Create(root)
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
        Main.create_th_measure_button(self.frame)
        self.grid_column(3)
        self.grid_row(4)
    
    def grid_column(self,column_index):
        for i in range(column_index + 1):
            self.frame.grid_columnconfigure(i,weight = 1)

    def grid_row(self,row_index):
        for i in range(row_index + 1):
            self.frame.grid_rowconfigure(i,weight = 1)
    


def main():
    app = Application(tk.Tk())
    app.mainloop()
if __name__ == "__main__":
    main()

    
