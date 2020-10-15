from Modules import Requirments
import tkinter as tk

def createSpotify(root):
    b=tk.Button(root,text="Spotify")
    photo1=tk.PhotoImage(file="images//gaana.png")
    b.config(image=photo1,width="100",height="100",compound = tk.CENTER,text="""Gaana""",command=Requirments.vlc_open)
    b.place(x=40,y=120)
    return b

def createNotepad(root):
    c=tk.Button(root,text="Notepad")
    photo2=tk.PhotoImage(file="images//notepad.png")
    c.config(image=photo2,width="100",height="100",compound = tk.CENTER,text="""Notepad""",command=Requirments.notepad_open)
    c.place(x=160,y=120)
    return c

def createChrome(root):
    e=tk.Button(root)
    photo4=tk.PhotoImage(file="images//chrome.png")
    e.config(image=photo4,text="Chrome",width="100",height="100",compound = tk.CENTER,command=Requirments.chrome_open)
    e.place(x=280,y=120)
    return e

def createMovies(root):
    d=tk.Button(root)
    photo3=tk.PhotoImage(file="images//opened_folder.png")
    d.config(image=photo3,text="Movies",width="100",height="100",compound = tk.CENTER,command=Requirments.movies_open)
    d.place(x=40,y=240)
    return d

def createDesktop(root):
    f=tk.Button(root)
    photo5=tk.PhotoImage(file="images//opened_folder.png")
    f.config(image=photo5,text="Desktop",width="100",height="100",compound = tk.CENTER,command=Requirments.desktop_open)
    f.place(x=160,y=240)
    return f

def createAdd(root):
    g=tk.Button(root)
    photo6=tk.PhotoImage(file="images//plus.png")
    g.config(image=photo6,text="Add",width="100",height="100",compound = tk.CENTER)
    g.place(x=280,y=240)
    return g

