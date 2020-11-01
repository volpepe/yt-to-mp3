from __future__ import unicode_literals

from tkinter import *
import tkinter.filedialog as filedialog

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
subprocess.call("python -m pip install --upgrade pip", shell=True)
subprocess.call("python -m pip install --upgrade youtube_dl", shell=True)
print("OK.")

if len(sys.argv) > 1:
    if sys.argv[1] == 'help':
        print("<application_name>.exe: opens GUI application.")
        print("<application_name>.exe help: displays this guide.")
        #print("<application_name>.exe <yt_video_link>: downloads a whole video.")
        #print("<application_name>.exe audio/video <yt_video_link>: downloads a whole song or video.")
        #print("<application_name>.exe audio/video <yt_video_link> <start_seconds>: downloads a song or video from given time.")
        #print("<application_name>.exe audio/video <yt_video_link> <start_seconds> <end_seconds>: downloads a song or video from start_s to end_s")
    else:
        pass #TODO
else:
    #general application setup
    root = Tk()
    root.title('YT Downloader 2 - By volpepe')
    root.geometry('950x250')

    #this variable will contain the link inserted by the user
    link_text = StringVar()
    folder_text = StringVar()
    st_min = StringVar()
    st_sec = StringVar()
    en_min = StringVar()
    en_sec = StringVar()
    out = StringVar()

    #creating the instruction label
    label = Label(root, text='Incolla qui il link:', font=(12), pady=15)
    label.grid(row=0, column=0, padx=5)

    #creating the input space (entry)
    entry_url = Entry(root, textvariable=link_text, width=70)
    entry_url.grid(row=0, column=1, columnspan=4, sticky=W, padx=20)

    #creating the time selectors
    label = Label(root, text='Minuto di inizio:', font=(12), pady=15)
    label.grid(row=1, column=0, padx=5)
    entry = Entry(root, textvariable=st_min, width=4)
    entry.grid(row=1, column=1, sticky=W, padx=10)
    label = Label(root, text='Secondo di inizio:', font=(12), pady=15)
    label.grid(row=1, column=2, padx=5)
    entry = Entry(root, textvariable=st_sec, width=4)
    entry.grid(row=1, column=3, sticky=W, padx=10)
    label = Label(root, text='Minuto di fine:', font=(12), pady=15)
    label.grid(row=1, column=4, padx=5)
    entry = Entry(root, textvariable=en_min, width=4)
    entry.grid(row=1, column=5, sticky=W, padx=10)
    label = Label(root, text='Secondo di fine:', font=(12), pady=15)
    label.grid(row=1, column=6, padx=5)
    entry = Entry(root, textvariable=en_sec, width=4)
    entry.grid(row=1, column=7, sticky=W, padx=10)

    #creating the output folder label and entry
    label = Label(root, text="Destinazione:", font=(12), pady=15)
    label.grid(row=2, column=0, padx=5)
    entry_folder = Entry(root, textvariable=folder_text, width=70)
    entry_folder.grid(row=2, column=1, columnspan=4, sticky=W, padx=20)

    #initialize folder text
    folder_text.set(os.getcwd())

    #creating the text label
    text = Label(root, textvariable=out, width=80, font=(18))
    text.grid(row=3, column=0, columnspan=8, pady=15, padx=20)
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
        def __init__(self, dl_type): 
            threading.Thread.__init__(self) 
            self.running = False
            self.x = out_show_thread()
            self.type = dl_type
            self.x.start()

        def run(self):
            self.running = True
            start, end = self.check_timings()
            # get title of the final video/audio file
            command_title = 'youtube-dl --get-filename -f "best" {}'.format(entry_url.get())
            #will ignore any non-utf-8 chars in title
            title = subprocess.check_output(command_title, shell=True).decode("utf-8", 'ignore').rstrip()[:-4]
            print("Title: {}".format(title))
            #downloads
            if self.type == 'audio':
                command = 'youtube-dl -x {} --audio-format {} -o "{}%(title)s.%(ext)s" {}'.format(
                    self.add_time_commands(start, end, 'ffmpeg_pre'), audio_format,
                                        os.path.join(folder_text.get(), ''), entry_url.get())
            elif self.type == 'video':
                #1
                command_url = 'youtube-dl -f "best" -g {}'.format(entry_url.get())
                url = subprocess.check_output(command_url, shell=True).decode("utf-8").rstrip()
                print("URL: {}".format(url))
                #2
                command = 'ffmpeg -i "{}" {} -c copy "{}".{}'.format(url, self.add_time_commands(start, end, 'ffmpeg_only'), 
                                                                    os.path.join(folder_text.get(), title), video_format)
            print(command)
            subprocess.call(command, shell=True)
            self.x.stop()
            self.x.join()
            self.running = False

            #clean slate
            text.config(state=NORMAL)
            out.set("Finito!!!")
            text.config(state=DISABLED)

        def check_timings(self):
            start = end = datetime.timedelta(seconds=0)
            #starting minute, starting second, ending minute, ending second
            timings =  list(map(lambda x: int(0 if x == '' else x), [st_min.get(), st_sec.get(), en_min.get(), en_sec.get()]))
            s_start = 60*timings[0] + timings[1]
            s_end = 60*timings[2] + timings[3]
            if s_start > 0:
                start += datetime.timedelta(seconds=s_start)
            if s_end > 0:
                end += datetime.timedelta(seconds=s_end)
            print("Starting time: " + str(start))
            print("Ending time: " + str(end))
            return start, end

        def add_time_commands(self, start, end, style):
            com = ''
            if style == 'ffmpeg_pre' and (start.seconds > 0 or end.seconds > 0):
                com += '--postprocessor-args "'
            if start.seconds > 0:
                com += " {} {} ".format("-ss", str(start))
            if end.seconds > 0:
                com += " {} {} ".format("-to", str(end))
            if style == 'ffmpeg_pre' and (start.seconds > 0 or end.seconds > 0):
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
        entry_url.delete(0, 'end')
        entry_url.insert(0, pyperclip.paste())

    def select_folder():
        folder_text.set(filedialog.askdirectory(initialdir=folder_text.get(), title="Seleziona Cartella di Destinazione").replace('/', os.sep))

    #creating the download button
    dl_button = Button(root, text='Download Audio', command=start_download, bg='brown',fg='white')
    dl_button.grid(row=0, column=5)  

    dl_button = Button(root, text='Download Video', command=start_download_video, bg='brown',fg='white')
    dl_button.grid(row=0, column=6, padx=20)

    #create the paste button
    pt_button = Button(root, text='Incolla', command=paste, bg='brown', fg='white')
    pt_button.grid(row=0, column=7, padx=10)

    #create the choose folder button
    fold_button = Button(root, text="Seleziona...", command=select_folder, bg="brown", fg="white")
    fold_button.grid(row=2, column=5, pady=15, padx=2, sticky=W)

    root.mainloop()