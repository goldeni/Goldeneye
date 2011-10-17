#!/usr/bin/python

<<<<<<< HEAD
from Tkinter import *
import Image,ImageTk,tkFileDialog,sys,tkMessageBox,cv
=======
import Tkinter
import Image,ImageTk,tkFileDialog,sys,tkMessageBox
>>>>>>> exp
import main

####### Definition buttons CMDs ###########

class mainWindow(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent=parent
		self.initialize()

	def changePara(self):
		cpara = Tkinter.Toplevel(bg="white")
		cpara.title("Change Parameters")
		cpara.geometry('250x250+0+0')

<<<<<<< HEAD
        #limage = Toplevel()
        #limage.title("Iris Processing")
        #limage.geometry('400x400+0+0')

	############################################
	#Test code here
	b1.destroy()
	b2.destroy()
	newimage = Label(root, image=loadImage)
	newimage.loadImage=loadImage
	newimage.grid(row=0,column=0,columnspan=2,rowspan=2)
	root.title("Iris Processing")
	root.geometry('400x400+0+0')
	############################################

	#newimage = Label(limage, image=loadImage)
	#newimage.loadImage=loadImage
	#newimage.pack()

        button = Button(root, text="Process Image",command=lambda i=imgPath: processImage(i),bg="white")
	button.grid(row=2,column=0,columnspan=2)

	# This is a really bad practice... but it works so whatever
	def processImage(imagePath):
		newimage.destroy()
		preImage = main.main(imagePath)
		processedImage = ImageTk.PhotoImage(preImage)
		newnewimage = Label(root, image=processedImage)
		newnewimage.processedImage=processedImage
		newnewimage.grid(row=0,column=0,columnspan=2,rowspan=2)
=======
		L1 = Tkinter.Label(cpara, text="Hamming Distance:",bg="white")
		L1.pack()
		E1 = Tkinter.Entry(cpara, bd=2)
		E1.pack()

		L2 = Tkinter.Label(cpara, text="Parameter 2:",bg="white")
		L2.pack()
		E2 = Tkinter.Entry(cpara, bd=2)
		E2.pack()

		L3 = Tkinter.Label(cpara, text="Parameter 3:",bg="white")
		L3.pack()
		E3 = Tkinter.Entry(cpara, bd=2)
		E3.pack()

		L2 = Tkinter.Label(cpara, text="Parameter 4:",bg="white")
		L2.pack()
		E2 = Tkinter.Entry(cpara, bd=2)
		E2.pack()

		button = Tkinter.Button(cpara, text="Submit", command=self.paraSubmit)
		button.pack(side = BOTTOM)
>>>>>>> exp

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

	def initialize(self):
		self.grid()

<<<<<<< HEAD
Background = PhotoImage(file="images/1.gif")
root.geometry("220x220+0+0")
#panel1 = Label(root,image=Background,bg="black").pack()
=======
		self.backImage = ImageTk.PhotoImage(file="images/1.gif")
		self.background = Tkinter.Label(self,image=self.backImage,bg="black")
		self.background.grid(row=0,column=0,columnspan=2,rowspan=2)
>>>>>>> exp

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

<<<<<<< HEAD
b1 = Button(root, text="Load Image", command=loadImage,bg="white")
b1.grid(row=0,column=0)

b2 = Button(root, text="Search for Record", command=searchRecord,bg="white")
b2.grid(row=0,column=1)

##############################################

if len(sys.argv) == 1:
        w = Label(root, text=" ")

elif len(sys.argv) == 2:
        imgPath = sys.argv[1]
        panelImage = ImageTk.PhotoImage(file=imgPath)
        w = Label(root, image=panelImage)
else:
        print "Error: Too many arguments"

w.grid(row=0,column=0)

root.mainloop()
=======
		self.b2 = Tkinter.Button(self, text="Search for Record", command=self.searchRecord,bg="white")
		self.b2.grid(row=3,column=1)

>>>>>>> exp

if __name__ == "__main__":
	root = mainWindow(None)
	root.title("Healthcare Iris Biometric Scanner")
	root.mainloop()

