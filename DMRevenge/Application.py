import tkinter as tk
import VIEW
import VIEW.Main as vMain

class Application(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
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




def main():
    app = Application(tk.Tk())
    app.mainloop()
if __name__ == "__main__":
    main()
    
