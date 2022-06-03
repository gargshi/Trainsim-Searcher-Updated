def searching(fname,comp):
	url="https://www.trainsim.com/download.php?fn="+fname
	#url="https://www.google.com"
	found=True
	try:
		webbrowser.get('chrome').open(url)
	except:
		print(fname+"Some issue with the webserver or file not found")
		found=False
		pass
	while(not down_comp(fname) and found):
		#os.system('cls')
		#time.sleep(1)
		display(comp)
		print(fname+" : Download in progress",end="\r")
		
		time.sleep(1)
	print(url)

def searching_gui(fname,comp):
	url="https://www.trainsim.com/download.php?fn="+fname
	#url="https://www.google.com"
	found=True
	try:
		webbrowser.get('chrome').open(url)
	except:
		print(fname+"Some issue with the webserver or file not found")
		found=False
		pass
	while(not down_comp(fname) and found):
		#os.system('cls')
		#time.sleep(1)
		display(comp)
		print(fname+" : Download in progress",end="\r")
		
		time.sleep(1)
	print(url)
def down_comp(fname):
	path1="D:/Shivam Garg/Downloads"
	if(os.path.exists(path1+"/"+fname)):
		return True
	return False

def display(comp):
	os.system('cls')
	for x in comp:		
		print("COMPLETED : "+x)

def reg():
	webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))

def get_data_from_file(file):
	print("core module called from outside")
	f=open(file,'r')
	con=f.read().split('\n')
	f.close()	
	return con

import os
import webbrowser
import time
import requests
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))
if __name__=='__main__':
	name='chrome'
	comp=[]
	webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))
	file="C:/d-content/openrails_dlc/trainsim_direct/req.txt"
	con=get_data_from_file(file)
	for i in con:
		if(not down_comp(i) and '##' not in i):
			searching(i,comp)
		comp.append(i)
		#get_completed(comp)

	os.system('pause')