#!/usr/bin/python

from Tkinter import *
import Image,ImageTk,tkFileDialog,sys,tkMessageBox,main

####### Definition buttons CMDs ###########

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


