#!/usr/bin/python

import Tkinter
import Image,ImageTk,tkFileDialog,sys,tkMessageBox

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

		newimage = Tkinter.Label(self, image=loadImage)
		newimage.loadImage=loadImage
		newimage.grid(row=0,column=0,rowspan=2,columnspan=2)

		button = Tkinter.Button(self, text="Process Image",command=self.processImage,bg="white")
		button.grid(row=2,column=0,columnspan=2)

	def paraSubmit(self):
		tkMessageBox.showinfo("Iris Processing", "Test")

	def searchRecord(self):
		tkMessageBox.showinfo("SEARCHING...", "RECORD")

	def processImage(self,path):
		tkMessageBox.showinfo("Iris Processing", "Test")

	def initialize(self):
		self.grid()

		self.backImage = ImageTk.PhotoImage(file="images/1.gif")
		self.background = Tkinter.Label(self,image=self.backImage,bg="black")
		self.background.grid(row=0,column=0,columnspan=2,rowspan=2)

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


#########################
if False:
	def globalPath(path):
		return path

	def loadImage():
		imgPath = tkFileDialog.askopenfilename()
		loadImage = ImageTk.PhotoImage(file=imgPath)
		print imgPath,loadImage

		w.destroy()

		limage = Toplevel()
		limage.title("Iris Processing")
		limage.geometry('250x250+0+0')

		newimage = Label(limage, image=loadImage)
		newimage.loadImage=loadImage
		newimage.pack()

		button = Button(limage, text="Process Image",command=processImage,bg="white")
		button.pack(side = BOTTOM)

	def processImage():
		tkMessageBox.showinfo("Iris Processing", "Test")

	def changePara():
		cpara = Toplevel(bg="white")
		cpara.title("Change Parameters")
		cpara.geometry('250x250+0+0')

		L1 = Label(cpara, text="Hamming Distance:",bg="white")
		L1.pack()
		E1 = Entry(cpara, bd=2)
		E1.pack()

		L2 = Label(cpara, text="Parameter 2:",bg="white")
		L2.pack()
		E2 = Entry(cpara, bd=2)
		E2.pack()

		L3 = Label(cpara, text="Parameter 3:",bg="white")
		L3.pack()
		E3 = Entry(cpara, bd=2)
		E3.pack()

		L2 = Label(cpara, text="Parameter 4:",bg="white")
		L2.pack()
		E2 = Entry(cpara, bd=2)
		E2.pack()

		button = Button(cpara, text="Submit", command=paraSubmit)
		button.pack(side = BOTTOM)

	def paraSubmit():
		tkMessageBox.showinfo("Iris Processing", "Test")

	def searchRecord():
		tkMessageBox.showinfo("SEARCHING...", "RECORD")

	def aboutProj():
		aproj = Toplevel(bg="white")
		aproj.title("Project Goldeneye")
		aproj.geometry('250x250+0+0')

		message = "Project Members: \nMatt, Joe, Ricky\n\nDetails:\n"
		Label(aproj,text=message,bg="white").pack(side = TOP)

	######## Creation of the root window #########

	root = Tk()
	root.title("Healthcare Iris Biometric Scanner")

	Background = PhotoImage(file="images/1.gif")
	root.geometry("220x220+0+0")
	panel1 = Label(root,image=Background,bg="black").pack()

	######## Menu Creation #######################

	menubar=Menu(root)
	filemenu = Menu(menubar,tearoff=0)
	filemenu.add_command(label="Change Parameters",command=changePara)
	filemenu.add_separator()
	filemenu.add_command(label="Quit",command=root.quit)

	menubar.add_cascade(label="File",menu=filemenu)

	helpmenu = Menu(menubar,tearoff=0)
	helpmenu.add_command(label="About Project",command=aboutProj)
	menubar.add_cascade(label="Help",menu=helpmenu)

	root.config(menu=menubar)

	######## Button Creation #####################

	b1 = Button(root, text="Load Image", command=loadImage,bg="white")
	b1.pack(side = LEFT)

	b2 = Button(root, text="Search for Record", command=searchRecord,bg="white")
	b2.pack(side = RIGHT)

	##############################################

	if len(sys.argv) == 1:
		w = Label(root, text=" ")

	elif len(sys.argv) == 2:
		imgPath = sys.argv[1]
		panelImage = ImageTk.PhotoImage(file=imgPath)
		w = Label(root, image=panelImage)
	else:
		print "Error: Too many arguments"

	w.pack()

	root.mainloop()


