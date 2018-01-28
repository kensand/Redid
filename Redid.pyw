#!/usr/bin/env python

import os
import io
import praw
import Tkinter
from PIL import Image, ImageTk
import botCredentials
import requests
import pickle

fg = 'white'
bg = 'black'

historyName = "history.pkl"


def openPickleJar(filename):
    ret = None
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            ret = pickle.load(f)
    return ret

def writePickleJar(filename, pickl):
    with open(filename, 'wb') as f:
        pickle.dump(pickl, f)



history = openPickleJar(historyName)
if history is None:
    history = list()

    
master = Tkinter.Tk()
def exitProg(code=0):
    writePickleJar(historyName, history)
    master.quit()
    exit(code)

def makeWindowScreenSize():
    w, h = master.winfo_screenwidth(), master.winfo_screenheight()
    master.geometry("%dx%d+0+0" % (w, h))
    master.minsize(w, h)

reddit = praw.Reddit(client_id=botCredentials.clientID, client_secret=botCredentials.clientSecret, user_agent='Redid 0.0.1/praw')
poststream = reddit.front.hot()
post = None
im = None
tkpi = None
title = None
label = None


def displayPost(post):
    global title, label, bf, fg
    global master
    if post is None:
        return

    if label is not None:
        label.pack_forget()
        del label
        label = None

    if title is not None:
        title.pack_forget()
        del title
        title = None
    
    name = post.fullname
    if name in history:
        nextFunc()
        return
    
    history.append(name)
    
    title = Tkinter.Label(text=post.title, fg=fg, bg=bg)
    title.pack()
    print(post.url)
    print(post.title)
    url = post.url
    urlend = url[-4:]
    acceptedImages = [".jpg", ".png", ".gif"]
    if urlend in acceptedImages:
        r = requests.get(url)
        print("encoding: ", r.encoding)
        
        im = Image.open(io.BytesIO(r.content))
        print im
        
        tkpi = ImageTk.PhotoImage(im)
        label = Tkinter.Label(image=tkpi, fg=fg, bg=bg)
        label.image=tkpi
        label.pack()
        
        



def nextFunc():
    global poststream
    post = poststream.next()
    displayPost(post)



def maximize():
    master.state("zoomed")


def backgroundColor(widget, color='white'):
    widget.configure(background=color)


backgroundColor(master, 'black')
nextButton= Tkinter.Button(master, text="Next", command=nextFunc)
nextButton.pack()

nextFunc()


master.title("Redid")


maximize()
#master.minsize(master.winfo_width(), master.winfo_height())
Tkinter.mainloop()
exitProg()
