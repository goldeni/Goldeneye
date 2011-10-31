#!/usr/bin/python

#test
import Tkinter
import Image,ImageTk,tkFileDialog,sys,tkMessageBox,cv
import main
from Tkinter import *

class mainWindow(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent=parent
		self.initialize()

	def changePara(self):
		cpara = Tkinter.Toplevel()
		cpara.title("Advanced Configuration Options")
		cpara.geometry('400x140+0+0')

		#### Use arrays ####
		L1 = Tkinter.Label(cpara, text="Hamming Distance:")
		L1.grid(sticky=E)
		E1 = Tkinter.Entry(cpara, bd=2)
		E1.grid(row=0, column=1)
		D1 = Tkinter.Label(cpara, text="(0.45)")
		D1.grid(row=0, column=3)

		L2 = Tkinter.Label(cpara, text="Median Filter Radius:")
		L2.grid(sticky=E)
		E2 = Tkinter.Entry(cpara, bd=2)
		E2.grid(row=1, column=1)
		D2 = Tkinter.Label(cpara, text="(???)")
                D2.grid(row=1, column=3)

		L3 = Tkinter.Label(cpara, text="Hough Transform Option:")
		L3.grid(sticky=E)
		E3 = Tkinter.Entry(cpara, bd=2)
		E3.grid(row=2, column=1)
		D3 = Tkinter.Label(cpara, text="(???)")
                D3.grid(row=2, column=3)

		L4 = Tkinter.Label(cpara, text="Unspecified Parameter:")
		L4.grid(sticky=E)
		E4 = Tkinter.Entry(cpara, bd=2)
		E4.grid(row=3, column=1)
		D4 = Tkinter.Label(cpara, text="(???)")
                D4.grid(row=3, column=3)

        	button = Tkinter.Button(cpara, text="Submit", command=self.paraSubmit,bg="white")
       		button.grid(row=6, column=1, pady=10)

	def queryDatabase(self):
		query = Tkinter.Toplevel()
		query.title("Patient Information")
		query.geometry('250x180+0+0')

		QL1 = Tkinter.Label(query, text="First Name:")
		QL1.grid(sticky=E)
		QE1 = Tkinter.Entry(query, bd=2)
		QE1.grid(row=0, column=1)

		QL2 = Tkinter.Label(query, text="Last Name:")
                QL2.grid(sticky=E)
                QE2 = Tkinter.Entry(query, bd=2)
                QE2.grid(row=1, column=1)

		QL3 = Tkinter.Label(query, text="SSN:")
                QL3.grid(sticky=E)
                QE3 = Tkinter.Entry(query, bd=2)
                QE3.grid(row=2, column=1)

		self.btype = StringVar(query)
		self.btype.set("A")
		
		QL4 = Tkinter.Label(query, text="Blood type:")
		QL4.grid(sticky=E)
		QE4 = Tkinter.OptionMenu(query, self.btype, "A", "B", "AB", "O")
                QE4.config(bg="white")
		QE4.grid(row=3, column=1, sticky=W)

		self.gender = StringVar(query)
		self.gender.set("Male")		

		QL5 = Tkinter.Label(query, text="Gender:")
                QL5.grid(sticky=E)
                QE5 = Tkinter.OptionMenu(query, self.gender, "Male", "Female")
		QE5.config(bg="white")
                QE5.grid(row=4, column=1, sticky=W)

		button = Tkinter.Button(query, text="Query", command=self.passFunction,bg="white")
       		button.grid(row=8, column=1, pady=10)

	def passFunction(self):
                func = Tkinter.Toplevel()
                func.title("Patient Record")
                func.geometry('400x400+0+0')
		
		#query.destroy()

	def aboutProj(self):
		aproj = Tkinter.Toplevel(bg="white")
		aproj.title("Project Goldeneye")
		aproj.geometry('250x250+0+0')

		message = "Project Members: \nMatt, Joe, Ricky\n\nDetails:\n"
		Tkinter.Label(aproj,text=message,bg="white").pack()

	def loadImage(self):
		while 1:
			try:
				imgPath = tkFileDialog.askopenfilename()
				loadImage = ImageTk.PhotoImage(file=imgPath)
			except IOError:
				fileString = " is not a valid PIL image file."
				tkMessageBox.showwarning("Not an image",
							 imgPath + fileString)
			else:
				break

		self.background.destroy()
		self.b1.destroy()
		self.b2.destroy()

		self.title("Iris Processing")

		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)

		self.button = Tkinter.Button(self, text="Process Image",command=lambda i=imgPath: self.processImage(i) ,bg="white")
		self.button.grid(row=2,column=0,columnspan=2,sticky=Tkinter.S+Tkinter.N)

	def paraSubmit(self):
		tkMessageBox.showinfo("Iris Processing", "Test")

	def processImage(self,path):
		self.newimage.destroy()
		self.title("Iris Processed")
		self.button.destroy()

		newImageObject = main.main(path)
		newImage = newImageObject.thresholdedImage
		centerx = newImageObject.xPoint
		centery = newImageObject.yPoint
		radius = newImageObject.rPoint

		loadImage = ImageTk.PhotoImage(newImage)
		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.pack()
		#self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)

		pupilCenter = Tkinter.Label(self, text="Center: " + str(centerx) + "," + str(centery),bg="white")
		pupilCenter.pack()
		#pupilCenter.grid(row=2,column=0,columnspan=2)

		pupilRadius = Tkinter.Label(self, text="Radius: " + str(radius),bg="white")
		pupilRadius.pack()
		#pupilCenter.grid(row=3,column=0,columnspan=2)	

		self.button = Tkinter.Button(self, text="Close",command=self.quit ,bg="white")
		self.button.pack()
		#self.button.grid(row=4,column=0,columnspan=2)

	def initialize(self):
		self.grid()

		self.backImage = ImageTk.PhotoImage(file="images/1.gif")
		self.background = Tkinter.Label(self,image=self.backImage,bg="black")
		self.background.grid(row=0,column=0,columnspan=2,rowspan=2)

		self.grid_columnconfigure(0,weight=1)
		#self.resizable(True,False)

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
		self.b1.grid(row=3,column=0, sticky=Tkinter.W+Tkinter.E)

		self.b2 = Tkinter.Button(self, text="Search for Record", command=self.queryDatabase,bg="white")
		self.b2.grid(row=3,column=1, sticky=Tkinter.W+Tkinter.E)


if __name__ == "__main__":
	root = mainWindow(None)
	root.title("Goldeneye Iris Scanner")
	root.geometry('+0+0')
	root.mainloop()

