from Tkinter import *
import tkMessageBox

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)
   
def submit():
	tkMessageBox.showinfo("Hello", "Submitted Successfully")

root = Tk()
var = IntVar()
CheckVar1 = IntVar()
CheckVar2 = IntVar()

B2 = Button(root, text ="Open", command = submit)
B2.pack()

R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Option 2", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="Option 3", variable=var, value=3,
                  command=sel)
R3.pack( anchor = W)

C1 = Checkbutton(root, text = "Music", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C2 = Checkbutton(root, text = "Video", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
B = Button(root, text ="Submit", command = submit)

label = Label(root)
label.pack()
C1.pack()
C2.pack()
B.pack()
root.mainloop()
