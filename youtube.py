from pytube import YouTube
from pytube.cli import on_progress
import signal 
import sys

#Simple function to ignore interrupts by the user
interrupt = False
cacheFlag = False
oauthFlag = False
def sigHandler(sig, frame):
   global interrupt
   interrupt = True
def keyboardInterrupt():
   global interrupt
   answersYes = ["Yes", "Y", "y", "yes", "sure", "yep", "huryep", "Huryep", "duh", "Duh", "yeah", "Yeah", "Hell Yes",  "hell Yes", "Hell yes", "hell yes", "Ok", "OK", "ofcourse", "Ofcourse"]
   answersNo = ["No", "no", "n", "N", "Nope", "nope", "Hurnah", "hurnah", "Hurnope", "hurnope", "Nah", "nah", "Hell No", "hell No", "Hell no", "hell no"]
   print("\nWould you like to exit the program?\n")
   while True:
      try:
         answer = input("Yes or No: ")
         if answer.lower() in answersYes:
            print("Exiting the program....")
            sys.exit(0)
         elif answer.lower() in answersNo:
            print("No selected, returning to main...\n")
            interrupt = False  # Reset the interrupt flag
            return False
         else:
            print("Please enter an acceptable input")
      except EOFError as error:
         print("Unable to accept user input: ", error)
         sys.exit(1)

def getInput():
   global interrupt
   if interrupt:
      if keyboardInterrupt():
            sys.exit(0)
   #Get user input as url
   url = input("Please Enter a url: ")
   return url
def downloadAudio(url):
   try:
      #Set the video object via pytube YouTube
      video = YouTube(url,
        on_progress_callback=on_progress,
        use_oauth=oauthFlag,
        allow_oauth_cache=cacheFlag
      )
      #stream filter only the audio
      stream = video.streams.filter(only_audio=True).first()
      stream.download(filename=f"{video.title}.mp3")
      #On success print 
      print("\nThe video is downloaded in MP3 format")
   except Exception as error:
      print("\nUnable to download video please try again or a different URL: ", error)

def downloadVideo(url):
   try:
      #set the video object via Youtube from pytube
      video = YouTube(url,
         on_progress_callback=on_progress,
         use_oauth=oauthFlag,
         allow_oauth_cache=cacheFlag
      )
      #stream
      stream = video.streams.filter(file_extension='mp4').first()
      stream.download(filename=f"{video.title}.mp4")
      print("The video was downloaded in MP4 format") 
   except Exception as error:
      print("\nUnable to download video please try again or a different URL: ", error)

def login(cacheFlag, oauthFlag):
   try:
      def sigHandler(sig, frame):
         print("\nInterrupt received. Returning to main menu...")
         raise KeyboardInterrupt

      signal.signal(signal.SIGINT, sigHandler)
      while True:        
         print("1. Enable/Disable OAuth cache")
         print("2. Enable/Disable OAuth")
         print("3. Go back")
         if(cacheFlag == False):
            print("OAuth cache is currently disabled")
         else:
            print("OAuth cache is currently enabled")
         if(oauthFlag == False):
            print("OAuth is currently disabled")
         else:
            print("OAuth is currently enabled")
         loginOptions = input("Please enter a menu option: ")
         if(loginOptions == "1"):
            if(cacheFlag == False):
               cacheFlag = True
               print("OAuth cache is now set to enabled")
            else:
               cacheFlag = False
               print("OAuth cache is now set to disabled")
         elif(loginOptions == "2"):
            if(oauthFlag == False):
               oauthFlag = True
               print("OAuth is now set to enabled")
            else:
               oauthFlag = False
               print("OAuth is now set to disabled")
         elif(loginOptions == "3"):
            break
         else:
            print("That is not a menu option please enter a valid input")        
      return cacheFlag, oauthFlag  # Return the modified flags
   except KeyboardInterrupt:
      if keyboardInterrupt():
         sys.exit(0)
      return cacheFlag, oauthFlag  # Return the flags even if interrupted in case user selects no
   except Exception as error:
      print("Unable to authenticate: ", error)
      
signal.signal(signal.SIGINT, sigHandler)
#Now run main script to download youtube video audio
# Main loop
while True:
   try:
      
      print("1. Login options")
      print("2. Download a YouTube video's audio")
      print("3. Download a YouTube video")
      print("4. Exit the program")
      option = input("Please enter a menu option: ")
      if(option == "1"):
         cacheFlag, oauthFlag = login(cacheFlag, oauthFlag)
      elif(option == "2"):
         url = getInput()
         downloadAudio(url)
      elif(option == "3"):
         url = getInput()
         downloadVideo(url)
      elif(option == "4"):
         if keyboardInterrupt():
            sys.exit(0)
      else:
         print("That is not a menu option please enter a valid input")
         
         
   except (KeyboardInterrupt, EOFError):
      if keyboardInterrupt():
         sys.exit(0)