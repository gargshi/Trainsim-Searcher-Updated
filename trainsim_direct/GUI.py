def direct_dnld(qf,sts,win):
	fname=qf.get(1.0,"end-1c")
	print("Received input: "+fname)
	sts.config(fg="#0023FF",text="Checking file "+fname)
	if(down_comp(fname)):
		sts.config()
		sts.config(fg="#FF0000",text="File already present in Downloads folder")
	else:
		time.sleep(1)
		url="https://www.trainsim.com/download.php?fn="+fname
		webbrowser.get('chrome').open(url)
		while not down_comp(fname):
			sts.config(text="Download in progress")
			win.lift()
			win.update()

		if(down_comp(fname)):
			sts.config(fg="#00FF23", text="Downloaded")

def down_comp(fname):
	path1="D:/Shivam Garg/Downloads"
	if(os.path.exists(path1+"/"+fname)):
		return True
	return False

def searching_gui(fname,comp,dt,win):
	url="https://www.trainsim.com/download.php?fn="+fname
	#url="https://www.google.com"
	found=True
	try:
		webbrowser.get('chrome').open(url)
	except:
		print(fname+"Some issue with the webserver or file not found")
		found=False
		pass
	comp[fname]='DOWNLOAD IN PROGRESS'
	pop_table(dt, comp,win)	
	while(not down_comp(fname) and found):
		win.lift()
		win.update()
		print(fname+" : Download in progress",end="\r")

	print(url)

def get_data_from_file(file):
	f=open(file,'r')
	con=f.read()
	res=len(con)==0
	con1=con.split('\n')
	f.close()
	if res:
		return []
	return con1

def pop_table(dt,data,win):
	print(data)
	
	dt.column("#0", width=0,  stretch=tkinter.NO)
	dt.column('filename',width=200)
	dt.column('Downloaded?',width=150)
	dt.heading("#0",text="")
	dt.heading('filename',text='FILENAME')
	dt.heading('Downloaded?',text='STATUS?')
	dt.delete(*dt.get_children())
	win.update()
	for i in data:
		dt.insert(parent='', index='end',values=(i,data[i]))
	win.update()

def delete(widget):
   widget.delete("1.0","end")

def check(sts,txt,abc=None):
	if(len(txt.get(1.0,"end-1c"))!=0):
		sts.config(fg="#0023FF",text="When done, click on download")

	else:
		sts.config(fg="#000000",text="STATUS MONITOR")

def start():
	def stay_on_top():
	   win.lift()
	   win.after(2000, stay_on_top)
	win=tkinter.Tk()
	win.geometry("750x350")
	win.title("TRAINSIM FILE SERACHER")
	win['bg'] = '#000000'
	lbl=tkinter.Label(win,text=" INPUT A FILE USING THE Button, then click on the start download button")	
	disp_tbl=ttk.Treeview(win, selectmode ='browse', show='headings')
	vsb= ttk.Scrollbar(win, orient ="vertical", command = disp_tbl.yview)
	disp_tbl.configure(yscroll = vsb.set)
	disp_tbl['columns'] = ('filename','Downloaded?')
	btn=tkinter.Button(win,text="OPEN FILE", width=50, command=lambda:openfdialog(disp_tbl,win))
	btn1=tkinter.Button(win,text="START DOWNLOAD", width=50, command=lambda:start_proc(disp_tbl,win))
	separator = ttk.Separator(win, orient='horizontal')
	emptylbl= tkinter.Label(win,text="or You can enter your file name in the text field below and click on the download button.")
	qf=tkinter.Text(win,width=50, height=1,font=('Consolas',10))
	sts=tkinter.Label(win,text="STATUS MONITOR")
	qf.bind('<KeyRelease>', lambda abc:check(sts,qf,abc))
	srch_dnld=tkinter.Button(win, width=25,text="Download",command=lambda:direct_dnld(qf,sts,win))
	clear_qf_btn=tkinter.Button(win, width=25,text="Clear Field",command=lambda:delete(qf))
	menubar=Menu(win)
	win.config(menu=menubar)
	file_menu=Menu(menubar,tearoff=False)
	file_menu.add_command(label='Open File',command=lambda:openfdialog(disp_tbl, win))
	file_menu.add_command(label='Exit',command=win.destroy)
	menubar.add_cascade(label="File",menu=file_menu)
	# place=[[btn,lbl,0,0]]
	# for i in place:
	# 	for j in range(len(i)):
	# 		if(not isinstance(i[j],int)):
	# 			i[j].grid(row=place.index(i),column=j)
	btn.grid(row=0,column=0, sticky='we')
	btn1.grid(row=0,column=1, sticky='we')
	lbl.grid(row=1,column=0,columnspan=2, sticky='we')
	disp_tbl.grid(row=2, column=0, columnspan=2,sticky='nsew')
	vsb.grid(row=2,column=2,sticky='ns')
	separator.grid(row=3,column=0,sticky='we',columnspan=3)
	emptylbl.grid(row=4,column=0,sticky='nsew',columnspan=2)
	srch_dnld.grid(row=5,column=1,sticky='nsew')
	clear_qf_btn.grid(row=6,column=1,sticky='nsew')
	qf.grid(row=5,column=0,columnspan=1,sticky='nsew')
	sts.grid(row=6,column=0,columnspan=1,sticky='nsew')
	#stay_on_top()
	win.mainloop()

def start_proc(dt,win):
	print("start")
	print(data)
	status(dt, data,win)

def status(dt,data,win):
	comp={}
	for i in data:
		if(not down_comp(i) and '##' not in i):
			searching_gui(i,comp,dt,win)
			comp[i]="COMPLETED"
		else:
			comp[i]="ALREADY DOWNLOADED"
		pop_table(dt, comp,win)


def openfdialog(dt,win):
	ftype=(('text files','*.txt'),('All files','*.*'))
	fname=fd.askopenfilename(title='Open a file',initialdir=os.getcwd(),filetypes=ftype)
	print("File selected :"+fname.replace("\\","/"))
	global data
	comp1={}
	data=get_data_from_file(fname)
	print(data)
	if len(data)!=0:
		for i in data:
			comp1[i]='FOUND FROM FILE'
		pop_table(dt, comp1, win)
	else:
		messagebox.showwarning("No data in file", "It seems that there is no data in the file you selected")


import tkinter
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import time
import webbrowser
import threading
if __name__=="__main__":
	data=[]
	webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))
	start()