#!/usr/bin/python 

from Tkinter import *
import Image,ImageTk,main,tkFileDialog,sys


###########################################
####### Definition buttons CMDs ###########
###########################################
def globalPath(path):
	return path
	
def loadImage():
	imgPath = tkFileDialog.askopenfilename()
	loadImage = ImageTk.PhotoImage(file=imgPath)
	print imgPath,loadImage
	w.loadImage=loadImage
	w.config(image=loadImage)

def saveImage():
	return 0

def compareImage():
	return 0

def autoProcess(path):
	newImage = ImageTk.PhotoImage(main.main(path))
	w.newImage=newImage
	w.config(image=newImage)

def manProcess():
	newImage= ImageTk.PhotoImage(main.main(imgPath))
	w.newImage=newImage
	w.config(image=newimage)


##############################################
######## Creation of the root window #########
##############################################
root = Tk()



if len(sys.argv) == 1:
	w = Label(root, text="Please load an image")
	
elif len(sys.argv) == 2:
	imgPath = sys.argv[1]
	panelImage = ImageTk.PhotoImage(file=imgPath)
	w = Label(root, image=panelImage)
else:
	print "Error: Too many arguments"
 

#############################################
############# Button Creation ###############
#############################################
loadButton = Button(root,text="Load Image",command=loadImage)
saveButton = Button(root,text="Save Image",command=saveImage)
compareButton = Button(root,text="Compare Image",command=compareImage)
autoProcessButton = Button(root,text="Auto-Process Image",command=lambda i=imgPath: autoProcess(i))
manualProcessButton = Button(root,text="Manually Process",command=manProcess)


#############################################
########### Calling Buttons/Image ###########
#############################################
saveButton.pack()
loadButton.pack()
compareButton.pack()

w.pack()

autoProcessButton.pack()
manualProcessButton.pack()

root.mainloop()
