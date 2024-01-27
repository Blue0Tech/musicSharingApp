import socket
from threading import Thread
from tkinter import *
from tkinter import ttk,filedialog
from playsound import playsound
import pygame
from pygame import mixer
import os
import time
import ftplib
from ftplib import FTP
import ntpath
from pathlib import Path

PORT = 8050
IP = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
song_counter = 0
listbox = None
infoLabel = None
selected_song = None

def setup():
    global SERVER
    global PORT
    global IP

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP,PORT))

    musicWindow()

def play():
    global selected_song
    global infoLabel
    
    selected_song = listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('C:\\Users\\pruth\\Music\\mymusic\\'+selected_song)
    mixer.music.play()
    if(selected_song!=''):
        infoLabel.configure(text='Now playing: '+selected_song)
    else:
        infoLabel.configure(text='')

def stop():
    global selected_song
    
    pygame
    mixer.music.stop()
    infoLabel.configure(text='')

def resume():
    global selected_song

    pygame
    mixer.music.unpause()

def pause():
    global selected_song
    
    pygame
    mixer.music.pause()

def musicWindow():
    global listbox
    global infoLabel
    global song_counter

    window = Tk()
    window.title('Music Window')
    window.geometry('300x350')
    window.configure(bg='LightSkyBlue')

    selectLabel = Label(window,text='Select Song',bg='LightSkyBlue',font=('Calibri',8))
    selectLabel.place(x=2,y=1)

    listbox = Listbox(window,height=10,width=39,activestyle='dotbox',bg='LightSkyBlue',borderwidth=2,font=('Calibri',10))
    listbox.place(x=10,y=18)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command=listbox.yview)

    playButton = Button(window,text='Play',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=play)
    playButton.place(x=30,y=200)

    stopButton = Button(window,text='Stop',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=stop)
    stopButton.place(x=200,y=200)

    uploadButton = Button(window,text='Upload',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=browseFiles)
    uploadButton.place(x=30,y=300)

    downloadButton = Button(window,text='Download',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=download)
    downloadButton.place(x=200,y=300)

    resumeButton = Button(window,text='Resume',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=resume)
    resumeButton.place(x=200,y=250)
    
    pauseButton = Button(window,text='Pause',width=10,bd=1,bg='SkyBlue',font=('Calibri',10),command=pause)
    pauseButton.place(x=30,y=250)

    infoLabel = Label(window,text='',fg='blue',font=('Calibri',8))
    infoLabel.place(x=4,y=330)

    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter,filename)
        song_counter += 1

    window.mainloop()

def browseFiles():
    global song_counter
    try:
        filename = filedialog.askopenfilename()
        host = '127.0.0.1'
        user = 'ftp'
        pswd = 'ftp'
        fname = ntpath.basename(filename)

        ftp_server = FTP(host,user,pswd)
        ftp_server.encoding = 'utf-8'
        ftp_server.cwd('shared_files')
        with open(filename,'rb') as f:
            ftp_server.storbinary(f'STOR {fname}',f)
        
        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter,fname)
        song_counter += 1

    except FileNotFoundError:
        print('Cancel button pressed')

def download():
    global selected_song
    song_to_download = listbox.get(ANCHOR)
    infoLabel.configure(text="Downloading " + song_to_download)
    HOSTNAME = '127.0.0.1'
    USERNAME = 'ftp'
    PASSWORD = 'ftp'
    home = str(Path.home())
    download_path = home+'/Downloads'
    ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding = 'utf-8'
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path,song_to_download)
    file = open(local_filename,'wb')
    ftp_server.retrbinary('RETR '+song_to_download,file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text='Download Complete')
    time.sleep(1)
    if(selected_song != '' and selected_song != None):
        infoLabel.configure(text="Now playing: "+selected_song)
    else:
        infoLabel.configure(text='')

setup_thread = Thread(target=setup)
setup_thread.start()