from tkinter import ttk
from tkinter import *
import time
from mutagen.mp3 import MP3
import os
import tkinter.messagebox
from tkinter import filedialog
import threading
from pygame import mixer
mixer.init()                                            #initializing the mixer

root = Tk()

statusbar = ttk.Label(root, text="Welcome",relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)                                    #creating the menubar in the root window
root.config(menu=menubar,bg='grey')

submenu = Menu(menubar, tearoff=0)                      #submenu is inside Menubar

def browse_files():
        global filenames                                #Declaring it as a global variable allows it to be used in other functions too.
        filenames = filedialog.askopenfilename()        #file is selected from the computer and stored in 'filenames' variable.
        addtolist(filenames)

Playlist = []                                           #initializing an empty playlist array.

def addtolist(f):
        f = os.path.basename(f)                         #f is the name of the song extracted from the entire path of the song
        index = 0                                       #first song is given the index 0
        playlistbox.insert(index,f)                     #the first song is entered into playlist box
        Playlist.insert(index,filenames)
        index+=1                                        #after the first song is entered the index is increased

menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open",command=browse_files)
submenu.add_command(label="Exit", command=root.destroy)

def aboutUs():
        tkinter.messagebox.showinfo("About Music Player","This Music Player has been developed as a project for the EE551 course in Fall 2019 by Neel Haria.")

submenu = Menu(menubar, tearoff=0)                      #submenu is inside Menubar
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About", command=aboutUs)

root.title("Music Player")
root.iconbitmap('Icons\Mic.ico')

leftframe = Frame(root)                                 #Dividing the root window into two frames LEFT and RIGHT
leftframe.pack(side=LEFT,padx=20)                       #side=LEFT pushes the frame to the left

rightframe = Frame(root)                                #Dividing the root window into two frames LEFT and RIGHT
rightframe.pack()

topframe = Frame(rightframe)                            #Top part of the right frame
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length = --:--',relief=GROOVE)
lengthlabel.pack()

currentlabel = ttk.Label(topframe, text='Current Time = --:--',relief=GROOVE)
currentlabel.pack()

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe, text="Add",command=browse_files)
addbtn.pack(side=LEFT)

def delSong():                                          #Function for removing song from the list box.
        selected_song = playlistbox.curselection()      #Used to select
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song)               #removing from array
        Playlist.pop(selected_song)


delbtn =ttk.Button(leftframe, text="Remove",command=delSong)
delbtn.pack(side=LEFT)

def showDetails(play_song):                             #Function to show collect and display total length and runtime of the audio

        data_file = os.path.splitext(play_song)         #Collects the path of the selected song in the form of a list.

        if data_file[1] == ".mp3":                      #Checks if the selected song has an mp3 extension.
                audio = MP3(play_song)
                totallength = audio.info.length         #Collects the total length of the audio.
                #print(totallength)
        else:
                a = mixer.Sound(play_song)              #if the song is of other type such as WAV, it plays the audio.
                totallength = a.get_length()

        mins, secs = divmod(totallength,60)             #Divmod function is used to obtain minutes and seconds from total length
        mins = round(mins)                              #Minutes are rounded off to the nearest value.
        secs = round(secs)
        format_time = '{:2d}:{:2d}.'.format(mins,secs)
        lengthlabel['text'] = "Total Length" + '-' + format_time

        t1 =threading.Thread(target=start_count, args=(totallength,))
        t1.start()

def start_count(t):                                     #Function to implement timer for Music being played.
        while t and mixer.music.get_busy():             #Checks if Stop button is pressed, resets the time.
                if paused:
                        continue
                else:
                        mins, secs = divmod(t, 60)
                        mins = round(mins)
                        secs = round(secs)
                        format_time = '{:02d}:{:02d}'.format(mins, secs)
                        currentlabel['text'] = "Current Length" + '-' + format_time
                        time.sleep(1)                   #One second delay when a song is switced from one to another, starts a new thread.
                        t = t - 1                          #Timer works in reverse.


def playMusic():                                        #Function to Play Music on pressing the play button.
        global paused
        if paused:                                      #Checks if Paused button is/was pressed.
                mixer.music.unpause()                   #Unpauses the player if paused.
                statusbar['text'] = "Unpaused"
                paused = FALSE                          #Pause becomes true after player unpauses the player.
        else:
                try:
                        stopMusic()
                        time.sleep(1)
                        selectedSong = playlistbox.curselection()
                        selectedSong = int(selectedSong[0])
                        playthissong = Playlist[selectedSong]
                        mixer.music.load(playthissong)
                        mixer.music.play()
                        statusbar['text'] = "Playing Now" + "-" + os.path.basename(playthissong)
                        showDetails(playthissong)
                except:
                        tkinter.messagebox.showerror("Warning!", "Please Select a song!")

def stopMusic():
        try:
                mixer.music.stop()
                statusbar['text'] = "Music Stopped"

        except:
                tkinter.messagebox.showinfo("No File Selected.", "Select a New File!")

paused = FALSE
def pauseMusic():
        global paused
        paused = True
        mixer.music.pause()
        statusbar['text'] = "Paused"

def rewindMusic():                                          #Function to Rewind Music.
        playMusic()                                         #Linking to the playMusic Function
        statusbar['text'] = "Music Rewinded"                #Updates the status bar

mute = FALSE                                                #Setting up the inital condition of mute to FALSE.
def muteMusic():
        global mute
        if mute:
                mixer.music.set_volume(0.11)
                volbtn.configure(image=volphoto)
                scale.set(11)
                mute = FALSE
        else:                                               #mute the music
                mixer.music.set_volume(0)
                volbtn.configure(image=mutephoto)
                scale.set(0)
                mute = TRUE

def setvol(val):
        volume = float(val)/100                          #TypeCasting string into integer value
        mixer.music.set_volume(volume)                   #set_volume takes Value from 0 to 1 only


middleframe = Frame(rightframe)                          #Defining the top part of the right frame
middleframe.pack( padx=50,pady=50)

bottomframe = Frame(rightframe)                          #Defining the bottom part of the right frame
bottomframe.pack(padx=10)

scale = ttk.Scale(bottomframe,from_= 0,to_= 100,orient = HORIZONTAL, command=setvol )           #Defining the Volume bar on User interface.
scale.set(11)                                                                                   #Setting the default value of the volume to a certain value, 11 here.
mixer.music.set_volume(0.11)                                                                    #since the range is 0 to 1 for volume.
scale.grid(row=0,column=1,padx=10,pady=10)                                                      #defining position according to the grid system.

rewindphoto = PhotoImage(file='Icons/back.png')                                                       #Using Rewind Icon to use it as a button.
rewindbtn = ttk.Button(bottomframe, image=rewindphoto, command=rewindMusic)                     #Linking the rewind button to the rewindMusic function
rewindbtn.grid(row=0,column=0)                                                                  #defining position according to the grid system.


playphoto = PhotoImage(file='Icons\play.png')                                                         #Using Play Icon to use it as a button.
playbtn = ttk.Button(middleframe, image=playphoto, command=playMusic)                           #Linking the play button to the playMusic function
playbtn.grid(row=0,column=1,padx=10)                                                            #defining position according to the grid system.

stopphoto = PhotoImage(file='Icons\stop.png')
stopbtn =ttk.Button(middleframe, image=stopphoto, command=stopMusic)
stopbtn.grid(row=0,column=0,padx=10)

pausephoto = PhotoImage(file='Icons\icon.png')
pausebtn = ttk.Button(middleframe, image=pausephoto, command=pauseMusic)
pausebtn.grid(row=0,column=2,padx=10)

mutephoto = PhotoImage(file ='Icons\mute.png')
volphoto = PhotoImage(file='Icons/volume.png')
volbtn = ttk.Button(bottomframe, image=volphoto, command=muteMusic)
volbtn.grid(row=0,column=4)


def onClosing():
        stopMusic()
        root.destroy()

root.protocol("WM_DELETE_WINDOW",onClosing)
root.mainloop()
