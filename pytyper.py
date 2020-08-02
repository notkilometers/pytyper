# initializing
import tkinter as tk 
from pynput.mouse import Button, Controller, Listener 
from ast import literal_eval as make_tuple
import keyboard
import traceback
import time
import os
import pickle

path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'pytyper.txt')
fpath = path
mouse = Controller()
global list
list = []

# class for holding info
class inf:
    def __init__(self, loca, lab, tex):
        self.loca = loca
        self.lab = lab
        self.tex = tex

    @classmethod
    def fromArray(cls, arr):
        return cls(arr[0], arr[1], arr[2])
    
def pickles_out(): # file upload
    with open(fpath, "w+") as f:
        for obj in list:
            h1 = obj.loca
            h2 = obj.lab
            h3 = obj.tex
            print("WRITING:", h1, h2, h3)
            f.write(str(h1) + os.linesep)
            f.write(str(h2) + os.linesep)
            f.write(str(h3) + os.linesep)
            
def pickles_in(self): # file download
    h = {}
    k = 0
    global list
    list = []

    with open(fpath, "r+") as f:
        for line in f:
            data = line.strip()
            if not data: continue
            if k == 0:
                h[k] = make_tuple(data)
            elif k == 2:
                h[k] = line
            else:
                h[k] = data

            k = (k + 1) % 3

            if k == 0:
                list.append(inf.fromArray(h))
                h = {}

# class for main window
class mainW(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.butA = {}
 
        self.master = master
        self.master.title = ("PyTyper")

        def outpAdv(obj): # output function
            mouse.position = obj.loca
            mouse.press(Button.left)
            mouse.release(Button.left)
            keyboard.write(obj.tex)

        def wrapCB(fn, params): # button func
            return lambda: fn(*params)

        def listtopage(self, list): # adds new buttons to page
            for i, obj in enumerate(list):
                self.butA[i] = tk.Button(self, text=obj.lab, command=wrapCB(outpAdv, [obj]))
                self.butA[i].pack()
            list.clear()

        def delButtons(self):
            for i in self.butA:
                self.butA[i].destroy()
            self.butA = {}
    
        def refr(): # refresh & add buttons
            delButtons(self)
            pickles_in(self)
            listtopage(self, list)

        self.refresh = tk.Button(self, text="Refresh", command=refr)
        self.refresh.pack()

        def addsw(): # add new button
            new = tk.Tk()
            appB = addB(new)
            appB.pack()
        
        self.button = tk.Button(self, text=" + ", command= addsw)
        self.button.pack()

# class for adding new buttons
class addB( tk.Frame):
    def __init__(self, master=None):
        self.butA = {}   
        def getinf(): # get info
            t0 = t
            t1=self.t1.get("1.0","end-1c")
            t2=self.t2.get("1.0","end-1c")
            pickles_in(self)
            list.append( inf(t0, t1, t2))
            pickles_out()
            list.clear()
            self.master.destroy()

        super().__init__(master)

        self.master = master
        self.master.title = ("Add New Button")

        self.l1 = tk.Label(self, text="Enter Desired Label:")
        self.l1.pack()
        self.t1 = tk.Text(self,height=1, width=10)
        self.t1.pack()
        self.l2 = tk.Label(self, text="Enter Desired Text:")
        self.l2.pack()
        self.t2 = tk.Text(self, height=2, width=10)
        self.t2.pack()

        def on_click(x, y, button, pressed): # grab locaiton when mouse is clicked
            global t
            t = mouse.position
            print(t)
            return False

        def start_mList(): # mouse listener
            with Listener(on_click=on_click) as mList:
                mList.join()
    
        def loc(): # starter function
            start_mList()
            
        self.b1 = tk.Button(self, text="Get Location", command=loc)
        self.b1.pack()
        self.b2 = tk.Button(self, text="Save", command=getinf)
        self.b2.pack()

root = tk.Tk()
root.resizable()
app = mainW(root)
app.pack(fill='both', expand=True)
pickles_out()
root.mainloop()
