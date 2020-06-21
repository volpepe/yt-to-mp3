# yt-to-mp3
A simple YouTube-to-mp3 downloader written for my dad to use in a single day. It's nothing special, but it's a working project I might as well showcase on my github page. It downloads a YouTube video given a link and tries to convert it in MP3. To do that, additional libraries are required to be on PATH (ffmpeg, I think. I found the answer on Stack Overflow). It's also my very first time using Tkinter.

---------------------------------------------

29/01/2020: Added video downloading & automatic youtube-dl updates (requires pip). Accidentally translated the application in Italian.  

---------------------------------------------

24/05/2020: Greatly messed up things during the last few months, had to rewrite the app from scratch: that's what ytdl_2.py is. Actually got a chance to finally add user choice of starting and ending time. Also removed the in-app console, which was nice for me, but visually horrifying for my "clients". Video download is still wip as the default mp4 format downloaded by youtube-dl is not compatible with Vegas which is the program I use for video editing.

---------------------------------------------

21/06/2020: Finally added video downloading option. I still need to test this as much as possible but I guess I'm done with this little project. My uncle gave me 20€ for it: wow.
