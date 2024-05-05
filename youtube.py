from pytube import YouTube
import signal 
import sys
#Simple function to ignore interrupts by the user
interrupt = False
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
      video = YouTube(url)
      #stream filter only the audio
      stream = video.streams.filter(only_audio=True).first()
      stream.download(filename=f"{video.title}.mp3")
      #On success print 
      print("\nThe video is downloaded in MP3")
   except:
      print("\nUnable to download video please try again or a different URL")      
signal.signal(signal.SIGINT, sigHandler)
#Now run main script to download youtube video audio
# Main loop
while True:
   try:
      url = getInput()
      downloadAudio(url)
   except (KeyboardInterrupt, EOFError):
      if keyboardInterrupt():
         sys.exit(0)