from tkinter import *

class Editor:
        
    def telaPrincipal():
        root = Tk() 
        root.geometry("800x800")
        root.title("Editor de Texto")
        root.minsize(height=250, width=350)
        root.maxsize(height=1080, width=1920) 
        
        scrollbar = Scrollbar(root) 
        scrollbar.pack(side=RIGHT, fill=Y) 
        
        text_info = Text(root, yscrollcommand=scrollbar.set) 
        text_info.pack(fill=BOTH) 
        scrollbar.config(command=text_info.yview) 
        
        root.mainloop()