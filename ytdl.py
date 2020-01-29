from __future__ import unicode_literals

from tkinter import *
import youtube_dl
from functools import partial
from io import StringIO
import threading
import time
import pyperclip
import os

#selecting best audio quality available
#downloader will try to convert the downloaded video into mp3 format
ydl_opts_audio = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

ytdl_opts_video = {
    'format': 'bestvideo/best',
    'extension': 'mp4'
}

#check for yt-dl updates
print("Controllo aggiornamenti...")
os.system("python -m pip install --upgrade youtube_dl --user")

#general application setup
root = Tk()
root.title('YT Downloader - By volpepe')
root.geometry('900x500')

#this variable will contain the link inserted by the user
link_text = StringVar()
out = StringIO()

sys.stdout = out

#creating the instruction label
label = Label(root, text='Incolla qui il link:', font=(12), pady=20)
label.grid(row=0, column=0, padx=5)

#creating the input space (entry)
entry = Entry(root, textvariable=link_text, width=70)
entry.grid(row=0, column=1, sticky=W, padx=20)

#creating the text label
text = Text(root)
text.grid(row=1, column=0, columnspan=3, pady=20, padx=20)
text.config(state=DISABLED)

#creating the scrollbar
scrollbar = Scrollbar(root)
scrollbar.grid(row=1, column=3)

#setting the scrollbar to the text
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command = text.yview)

#################### THREADS #######################

class out_show_thread(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 
        self.running = False
    
    def run(self):
        self.running = True
        while(self.running):
            time.sleep(0.2)
            text.config(state=NORMAL)
            text.delete(1.0, END)
            text.insert(1.0, out.getvalue())
            text.config(state=DISABLED)
    
    def stop(self):
        self.running = False

class download_thread(threading.Thread):
    def __init__(self, ytdl_opts): 
        threading.Thread.__init__(self) 
        self.ytdl_opts = ytdl_opts
        self.running = False
        self.x = out_show_thread()
        self.x.start()

    def run(self):
        self.running = True
        with youtube_dl.YoutubeDL(self.ytdl_opts) as ydl:
            ydl.download([link_text.get()])
        self.x.stop()
        self.x.join()
        self.running = False

        #clean slate
        text.config(state=NORMAL)
        text.delete(1.0, END)
        text.insert(1.0, "Finito!!!!")
        text.config(state=DISABLED)
        out.truncate(0)
        out.seek(0)

####################################################

def start_download():
    y = download_thread(ydl_opts_audio)
    y.start()

def start_download_video():
    y = download_thread(ytdl_opts_video)
    y.start()

def paste():
    entry.insert(0, pyperclip.paste())

#creating the download button
dl_button = Button(root, text='Download Audio', command=start_download, bg='brown',fg='white')
dl_button.grid(row=0, column=2)  

dl_button = Button(root, text='Download Video', command=start_download_video, bg='brown',fg='white')
dl_button.grid(row=0, column=3, padx=20)  

#create the paste button
pt_button = Button(root, text='Incolla', command=paste, bg='brown', fg='white')
pt_button.grid(row=0, column=4, padx=10)  

root.mainloop()