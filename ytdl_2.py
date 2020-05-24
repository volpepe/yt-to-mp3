from __future__ import unicode_literals

from tkinter import *

from io import StringIO
import threading
import time
import pyperclip
import os
import sys
import datetime
import subprocess

########################### FORMATS #############################

audio_format = "mp3" # change to wav if quality suuuux
video_format = "mp4"

#################################################################

#check for yt-dl updates
print("Controllo aggiornamenti...")
subprocess.call("python -m pip install --upgrade pip")
subprocess.call("python -m pip install --upgrade youtube_dl")
print("OK.")

#general application setup
root = Tk()
root.title('YT Downloader 2 - By volpepe')
root.geometry('950x250')

#this variable will contain the link inserted by the user
link_text = StringVar()
st_min = StringVar()
st_sec = StringVar()
en_min = StringVar()
en_sec = StringVar()
out = StringVar()

#creating the instruction label
label = Label(root, text='Incolla qui il link:', font=(12), pady=20)
label.grid(row=0, column=0, padx=5)

#creating the input space (entry)
entry_url = Entry(root, textvariable=link_text, width=70)
entry_url.grid(row=0, column=1, columnspan=4, sticky=W, padx=20)

#creating the time selectors
label = Label(root, text='Minuto di inizio:', font=(12), pady=20)
label.grid(row=1, column=0, padx=5)
entry = Entry(root, textvariable=st_min, width=4)
entry.grid(row=1, column=1, sticky=W, padx=10)
label = Label(root, text='Secondo di inizio:', font=(12), pady=20)
label.grid(row=1, column=2, padx=5)
entry = Entry(root, textvariable=st_sec, width=4)
entry.grid(row=1, column=3, sticky=W, padx=10)
label = Label(root, text='Minuto di fine:', font=(12), pady=20)
label.grid(row=1, column=4, padx=5)
entry = Entry(root, textvariable=en_min, width=4)
entry.grid(row=1, column=5, sticky=W, padx=10)
label = Label(root, text='Secondo di fine:', font=(12), pady=20)
label.grid(row=1, column=6, padx=5)
entry = Entry(root, textvariable=en_sec, width=4)
entry.grid(row=1, column=7, sticky=W, padx=10)

#creating the text label
text = Label(root, textvariable=out, width=80, font=(18))
text.grid(row=2, column=0, columnspan=8, pady=20, padx=20)
text.config(state=DISABLED)

#################### THREADS #######################

class out_show_thread(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 
        self.running = False
    
    def run(self):
        self.running = True
        count=0
        while(self.running):
            text.config(state=NORMAL)
            out.set("Scaricando" + "."*count)
            count = count+1 if count < 5 else 0
            text.config(state=DISABLED)
            time.sleep(0.8)
    
    def stop(self):
        self.running = False

class download_thread(threading.Thread):
    def __init__(self, type): 
        threading.Thread.__init__(self) 
        self.running = False
        self.x = out_show_thread()
        self.type = type
        self.x.start()

    def run(self):
        self.running = True
        start, end = self.check_timings()
        if self.type == 'audio':
            command = "youtube-dl -x {} --audio-format {} {}".format(
                self.add_time_commands(start, end, 'ffmpeg'), audio_format, entry_url.get())
            print(command)
            subprocess.call(command)
        elif self.type == 'video':
        	pass
        	'''
			Still a work in progress, unfortunately.

            command = 'youtube-dl {} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best/bestvideo+bestaudio" --merge-output-format {} {}'.format(
            	self.add_time_commands(start, end, 'ffmpeg'), video_format, entry_url.get())
            print(command)
            title = subprocess.check_output(["youtube-dl", "-f", '"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best/bestvideo+bestaudio"', "--merge-output-format",
                "mp4", entry_url.get(), "--get-filename"])
            print("Title: " + title)
            os.system(command)
            command = 'HandBrakeCLI {} -i "{}" -o "{}_{}_{}.mp4"'.format(self.add_time_commands(start, end, 'handbrake'),
                title, title[:-4], start.seconds, end.seconds)
            os.system(command)
            '''
        self.x.stop()
        self.x.join()
        self.running = False

        #clean slate
        text.config(state=NORMAL)
        out.set("Finito!!!")
        text.config(state=DISABLED)

    def check_timings(self):
        start = end = datetime.timedelta(seconds=0)
        if st_sec.get() != '':
            start += datetime.timedelta(seconds=int(st_sec.get()) + 60*int(st_min.get() if st_min.get() != '' else 0))
        if en_sec.get() != '':
            end += datetime.timedelta(seconds=int(en_sec.get()) + 60*int(en_min.get() if en_min.get() != '' else 0))
        print("Starting time: " + str(start))
        print("Ending time: " + str(end))
        return start, end

    def add_time_commands(self, start, end, style):
        com = ''
        if style == 'ffmpeg' and (start.seconds > 0 or end.seconds > 0):
            com += '--postprocessor-args "'
        if start.seconds > 0:
            com += " {} {} ".format("-ss" if style == 'ffmpeg' else "--start-at", str(start) if style == 'ffmpeg' else "seconds:{}".format(str(start)))
        if end.seconds > 0:
            com += " {} {} ".format("-to" if style == 'ffmpeg' else "--stop-at", str(end) if style == 'ffmpeg' else "seconds:{}".format(str(end)))
        if style == 'ffmpeg' and (start.seconds > 0 or end.seconds > 0):
            com += '"'
        return com

####################################################

def start_download():
    y = download_thread('audio')
    y.start()

def start_download_video():
    y = download_thread('video')
    y.start()

def paste():
    entry_url.insert(0, pyperclip.paste())

#creating the download button
dl_button = Button(root, text='Download Audio', command=start_download, bg='brown',fg='white')
dl_button.grid(row=0, column=5)  

'''
Code for video download is still work in progress

dl_button = Button(root, text='Download Video', command=start_download_video, bg='brown',fg='white')
dl_button.grid(row=0, column=6, padx=20)  
'''

#create the paste button
pt_button = Button(root, text='Incolla', command=paste, bg='brown', fg='white')
pt_button.grid(row=0, column=6, padx=10)  

root.mainloop()