#!/usr/bin/python

import Tkinter
import Image,ImageTk,tkFileDialog,sys,tkMessageBox

import main

class mainWindow(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent=parent
		self.initialize()

	def changePara(self):
		cpara = Tkinter.Toplevel(bg="white")
		cpara.title("Change Parameters")
		cpara.geometry('250x250+0+0')


	def aboutProj(self):
		aproj = Tkinter.Toplevel(bg="white")
		aproj.title("Project Goldeneye")
		aproj.geometry('250x250+0+0')

		message = "Project Members: \nMatt, Joe, Ricky\n\nDetails:\n"
		Tkinter.Label(aproj,text=message,bg="white").pack()

	def loadImage(self):
		imgPath = tkFileDialog.askopenfilename()
		loadImage = ImageTk.PhotoImage(file=imgPath)

		self.background.destroy()
		self.b1.destroy()
		self.b2.destroy()

		self.title("Iris Processing")

		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)

		self.button = Tkinter.Button(self, text="Process Image",command=lambda i=imgPath: self.processImage(i) ,bg="white")
		self.button.grid(row=2,column=0,columnspan=2)

	def paraSubmit(self):
		tkMessageBox.showinfo("Iris Processing", "Test")

	def searchRecord(self):
		tkMessageBox.showinfo("SEARCHING...", "RECORD")

	def processImage(self,path):
		self.newimage.destroy()
		self.title("Iris Processed")
		self.button.destroy()

		loadImage = ImageTk.PhotoImage(main.main(path))
		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)
		
		self.button = Tkinter.Button(self, text="Close",command=self.quit ,bg="white")
		self.button.grid(row=2,column=0,columnspan=2)

	def initialize(self):
		self.grid()

		self.backImage = ImageTk.PhotoImage(file="images/1.gif")
		self.background = Tkinter.Label(self,image=self.backImage,bg="black")
		self.background.grid(row=0,column=0,columnspan=2,rowspan=2)

		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,False)

		menubar=Tkinter.Menu(self)
		filemenu = Tkinter.Menu(menubar,tearoff=0)
		filemenu.add_command(label="Change Parameters",command=self.changePara)
		filemenu.add_separator()
		filemenu.add_command(label="Quit",command=self.quit)

		menubar.add_cascade(label="File",menu=filemenu)

		helpmenu = Tkinter.Menu(menubar,tearoff=0)
		helpmenu.add_command(label="About Project",command=self.aboutProj)
		menubar.add_cascade(label="Help",menu=helpmenu)

		self.config(menu=menubar)

		self.b1 = Tkinter.Button(self, text="Load Image", command=self.loadImage,bg="white")
		self.b1.grid(row=3,column=0)


		self.b2 = Tkinter.Button(self, text="Search for Record", command=self.searchRecord,bg="white")
		self.b2.grid(row=3,column=1)

if __name__ == "__main__":
	root = mainWindow(None)
	root.title("Healthcare Iris Biometric Scanner")
	root.mainloop()

