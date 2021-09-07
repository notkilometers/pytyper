from pynput.mouse import Button, Listener, Controller
from keyboard import write
import tkinter as tk
import pickle

macros = [] # init global "macros" & set mouse to controller from pynput
mouse = Controller()

def executeMacro(macro): # moves mouse to location, clicks, types words
    mouse.position = macro.location
    mouse.press(Button.left)
    mouse.release(Button.left)
    write(macro.text)

def addButton(frame, macro): # packs button to frame with label
    frame.newButton = tk.Button(frame, text=macro.label, command=lambda: executeMacro(macro))
    frame.newButton.pack()

def loadMacros():
    return pickle.load(open("macros.p", "rb"))

def saveMacros():
    pickle.dump(macros, open("macros.p", "wb"))
    

def getMousePosition(self):
    self.location = mouse.position
    return False # returns false for to flag that button click is complete to grab location in calling function

def getMousePositionWrapper(self): # wrapper function for getting mouse position
    with Listener(on_click = lambda x, y, button, pressed: getMousePosition(self)) as listener: # the lambda needs 4 args that never get used, blame pynput
        listener.join()
    
    
def saveFields(self): # save fields to list, save list, destroy window
    newMacro = macro(self.location, self.textBox1.get("1.0","end-1c"), self.textBox2.get("1.0","end-1c")) # append to list
    macros.append(newMacro)
    addButton(self.parent, newMacro)
    saveMacros() # saves to pickle
    self.master.destroy() # close window

class macro():
    def __init__(self, location, label, text):
        self.location = location
        self.label = label
        self.text = text

# class for window to add buttons
class addGUI(tk.Frame):
    
    def __init__(self, master=None, parent=None):
        self.super = tk.Frame
        super().__init__(master)
        self.master = master
        self.parent = parent

        # text box vars so I can grab the contents later
        self.textBox1 = tk.Text(self,height=1, width=10)
        self.textBox2 = tk.Text(self, height=2, width=10)
        
        # all of the labels, text boxes, buttons
        fields = [tk.Label(self, text="Enter Desired Label:"), self.textBox1, tk.Label(self, text="Enter Desired Text:"), self.textBox2, tk.Button(self, text="Get Location", command=lambda : getMousePositionWrapper(self)), tk.Button(self, text="Save", command=lambda : saveFields(self))]
    
        # packs buttons onto gui
        for i in fields:
            i.pack()

# class for window housing the actual macro buttons
class macroGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # caller for gui to add macros
        def callAdd():
            frame = tk.Tk()
            appAdd = addGUI(frame, self)
            appAdd.pack()
        
        button = tk.Button(self, text=" + ", command=callAdd)
        button.pack()

        # add pre-existing macros from pickle
        macros = loadMacros()

        for macro in macros:
            addButton(self, macro)

# start program       
if __name__ == "__main__":
    root = tk.Tk()
    app = macroGUI(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
