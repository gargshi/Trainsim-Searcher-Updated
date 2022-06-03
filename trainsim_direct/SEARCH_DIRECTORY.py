import tkinter as tk
import tkinter.font as tkFont
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
import os

class App:
    q_dir=''
    lb=''
    default_folder=''
    lstdr=[]

    def __init__(self, root):
        #load config file
        self.chk_for_config_file()
        fo=open('config.txt','r')
        cfg=fo.read().split('\n')
        for i in cfg:
            if('DEFAULT_FOLDER' in i):
                self.default_folder=i.split('<=>')[1]

        fo.close()
        print("SETTINGS LOADED")
        print("default_folder = "+self.default_folder)

        #setting title
        root.title("SEARCH DIRECTORY")
        #setting window size
        width=564
        height=502
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        menubar=Menu(root)
        root.config(menu=menubar)
        file_menu=Menu(menubar,tearoff=False)
        file_menu.add_command(label='Open File',command=self.sel_file_dir_for_pop)
        file_menu.add_command(label='Exit',command=root.destroy)
        setting_menu=Menu(menubar,tearoff=False)
        setting_menu.add_command(label='Preferences',command=lambda:self.display_settings_window(root))
        option_menu=Menu(menubar,tearoff=False)
        option_menu.add_command(label='Open Trainsim Searcher',command=lambda:self.open_program(root))
        menubar.add_cascade(label="File",menu=file_menu)
        menubar.add_cascade(label="Settings",menu=setting_menu)
        menubar.add_cascade(label="Options", menu=option_menu)

        GLabel_324=tk.Label(root)
        ft = tkFont.Font(family='Consolas',size=20)
        GLabel_324["font"] = ft
        GLabel_324["fg"] = "#333333"
        GLabel_324["justify"] = "center"
        GLabel_324["text"] = "Search Directory"
        GLabel_324.place(x=100,y=10,width=378,height=97)

        GLineEdit_133=tk.Entry(root)
        GLineEdit_133["borderwidth"] = "1px"
        ft = tkFont.Font(family='Consolas',size=10)
        GLineEdit_133["font"] = ft
        GLineEdit_133["fg"] = "#333333"
        GLineEdit_133["justify"] = "center"
        GLineEdit_133["text"] = "Entry"
        GLineEdit_133.place(x=50,y=160,width=319,height=30)
        GLineEdit_133.bind('<KeyRelease>', lambda abc:self.check(GLineEdit_133,abc))

        GButton_379=tk.Button(root)
        GButton_379["bg"] = "#efefef"
        ft = tkFont.Font(family='Consolas',size=10)
        GButton_379["font"] = ft
        GButton_379["fg"] = "#000000"
        GButton_379["justify"] = "center"
        GButton_379["text"] = "SEARCH"
        GButton_379["relief"] = "raised"
        GButton_379.place(x=430,y=160,width=82,height=30)
        GButton_379["command"] = lambda:self.GButton_379_command(GLineEdit_133.get())

        GListBox_818=tk.Listbox(root)
        GListBox_818["borderwidth"] = "1px"
        ft = tkFont.Font(family='Consolas',size=10)
        GListBox_818["font"] = ft
        GListBox_818["fg"] = "#333333"
        GListBox_818["justify"] = "center"
        GListBox_818.place(x=50,y=210,width=463,height=251)
        GListBox_818["selectmode"] = "browse"
        GListBox_818.bind("<<ListboxSelect>>",lambda abc:self.fetch(GListBox_818,abc))
        self.lb=GListBox_818
        if(self.default_folder!=''):
            self.get_file_list(self.default_folder)

    def display_settings_window(self,root):
        setting_child=tk.Toplevel(root)
        setting_child.geometry("564x502")
        setting_child.title("Settings")
        setting_child.transient(root)
        setting_child.grab_set()
        #root.wait_window(setting_child)

        GLabel_3241=tk.Label(setting_child)
        ft = tkFont.Font(family='Helvetica',size=20)
        GLabel_3241["font"] = ft
        GLabel_3241["fg"] = "#333333"
        GLabel_3241["justify"] = "center"
        GLabel_3241["text"] = "Settings"
        GLabel_3241.place(x=100,y=10,width=378,height=97)

        GLineEdit_134=tk.Label(setting_child)
        GLineEdit_134["borderwidth"] = "1px"
        ft = tkFont.Font(family='Consolas',size=10)
        GLineEdit_134["font"] = ft
        GLineEdit_134["fg"] = "#333333"
        GLineEdit_134["justify"] = "left"
        GLineEdit_134["text"] = "--Enter default directory here through the button--" if self.default_folder == '' else self.default_folder
        GLineEdit_134.place(x=50,y=160,width=349,height=30)

        GButton_379=tk.Button(setting_child)
        GButton_379["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Consolas',size=10)
        GButton_379["font"] = ft
        GButton_379["fg"] = "#000000"
        GButton_379["justify"] = "center"
        GButton_379["text"] = "Change"
        GButton_379["relief"] = "raised"
        GButton_379.place(x=420,y=160,width=95,height=30)
        GButton_379["command"] = lambda:self.pop_sett_fd_entry(GLineEdit_134,setting_child)

        GButton_380=tk.Button(setting_child)
        GButton_380["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Consolas',size=10)
        GButton_380["font"] = ft
        GButton_380["fg"] = "#000000"
        GButton_380["justify"] = "center"
        GButton_380["text"] = "Save"
        GButton_380["relief"] = "raised"
        GButton_380.place(x=420,y=200,width=95,height=30)
        GButton_380["command"] = self.save_settings

        GLabel_805=tk.Label(setting_child)
        ft = tkFont.Font(family='MS Sans Serif',size=10)
        GLabel_805["font"] = ft
        GLabel_805["fg"] = "#333333"
        GLabel_805["justify"] = "center"
        GLabel_805["text"] = "Default Directory :"
        GLabel_805.place(x=50,y=120,width=114,height=30)

    def chk_for_config_file(self):
        if(not os.path.exists('config.txt')):
            print("config file not present, creating")
            f=open('config.txt','w')
            f.write("DEFAULT_FOLDER<=>")
            f.close()

    def save_settings(self):
        f=open('config.txt','w')
        data="DEFAULT_FOLDER<=>"+self.default_folder
        f.write(data)
        f.close()
        messagebox.showinfo("Done","Settngs Saved")

    def open_program(self,path):
        messagebox.showwarning("Warning","Functionality to be defined in future releases")
        #pass

    def fetch(self,widget,abc=None):
        select=widget.get(widget.curselection()[0])
        print(select)

    def select_directory(self):
        print("Select Directory method activated")
        direct=filedialog.askdirectory()
        self.q_dir=direct
        print(direct,self.q_dir)
    
    def pop_sett_fd_entry(self,widget,settwin):
        self.select_directory()
        self.default_folder=self.q_dir
        widget.config(text=self.q_dir)
        settwin.update()

    def sel_file_dir_for_pop(self):
        self.select_directory()
        self.get_file_list(self.q_dir)

    def get_file_list(self,pth):
        lst=os.listdir(pth)
        print(lst)
        self.lstdr=lst
        self.pop_list(lst)

    def pop_list(self,con):
        list_items = tk.StringVar(value=con)
        self.lb.config(listvariable=list_items)
        
    def GButton_379_command(self,txt):
        print(txt)

    def display(self,str):
        ls=self.lstdr
        if(str==''):
            self.pop_list(ls)
        upd=[i for i in ls if str.lower() in i.lower()]
        self.pop_list(upd)

    def check(self,txt,abc=None):
        x=txt.get()
        self.display(x)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()