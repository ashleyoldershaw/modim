import Tkinter, tkFileDialog
from Tkinter import *
import os
from generator import generate_grammar_file


root = Tkinter.Tk()

message = StringVar()
list_of_files = []
save_directory = []

#Buttons callbacks
def askOpenFilenames():
    global list_of_files
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose file(s) to generate the grammar')
    list_of_files = root.tk.splitlist(filez)
    
    if len(list_of_files) == 0:
        print "Warning: No files selected..."

def askSaveDirectory():
    global save_directory
    current_dir = os.path.dirname(__file__)
    save_directory = tkFileDialog.askdirectory(parent=root,initialdir=current_dir,title='Choose directory where to save the generated grammars')
    if len(save_directory ) == 0:
        print "Warning: You did not chose any output folder..."

def generateGrammars():
    global list_of_files
    
    if len(list_of_files) == 0:
        message.set("Warning: No files selected...")
        labelMessage.config(fg = 'red')
        return
    if len(save_directory) == 0:
        message.set("Warning: You did not chose any output folder...")
        labelMessage.config(fg = 'red')
        return

    
    for filename in list_of_files:
        generate_grammar_file(filename, save_directory)

    message.set('Grammar files saved in %s.' %save_directory)
    labelMessage.config(fg = 'green')

#Creating buttons
buttonFilenames = Tkinter.Button(root, text = 'Choose file(s) to generate the grammar', command=askOpenFilenames)
buttonFilenames.pack()

buttonDirectory = Tkinter.Button(root, text = 'Choose save directory', command=askSaveDirectory)
buttonDirectory.pack()

buttonGenerate = Tkinter.Button(root, text = 'Generate grammars', command=generateGrammars)
buttonGenerate.pack()

labelMessage = Tkinter.Label(root, textvariable=message)
labelMessage.pack()

root.mainloop()
