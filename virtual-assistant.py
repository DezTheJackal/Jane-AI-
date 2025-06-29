import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import sys
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Check if voices are available and set female voice
if voices:
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
else:
    print("Warning: No voices found. Text-to-speech may not work properly.")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Master!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Master!")   
    else:
        speak("Good Evening Master!")  
   
    speak("I am your Jinnie and you are my master! Let's make some magic! Please tell me how may I help you")       

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # Added for better recognition
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    """
    Secure email sending function
    """
    try:
        # Get email credentials securely
        sender_email = input("Enter your email: ")
        password = getpass.getpass("Enter your email password: ")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to
        msg['Subject'] = "Message from Jinnie Assistant"
        
        # Add body to email
        msg.attach(MIMEText(content, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, to, text)
        server.close()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def safe_file_operation(file_path, operation="open"):
    """
    Safely handle file operations with error checking
    """
    try:
        if os.path.exists(file_path):
            if operation == "open":
                os.startfile(file_path)
                return True
            elif operation == "list":
                return os.listdir(file_path)
        else:
            speak(f"Sorry master, the file or directory {file_path} does not exist.")
            return False
    except Exception as e:
        speak(f"Sorry master, I couldn't access the file. Error: {str(e)}")
        return False

if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()
        
        if query == "none":
            continue

        if "wikipedia" in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results. Please be more specific.")
                print(f"Options: {e.options[:5]}")
            except wikipedia.exceptions.PageError:
                speak("Sorry master, I couldn't find that information on Wikipedia.")
            except Exception as e:
                speak("Sorry master, there was an error searching Wikipedia.")

        elif "open google" in query:
            speak("master, what should i search on google")
            cm = takecommand().lower()
            if cm != "none":
                webbrowser.open(f"https://www.google.com/search?q={cm}")
                speak("Thank you master, You will be redirected to the link soon.")

        elif "open youtube" in query:
            speak("master, what should i search on youtube")
            x = takecommand().lower()
            if x != "none":
                webbrowser.open(f"https://www.youtube.com/results?search_query={x}")
                speak("Thank you master, You will be redirected to the link soon.")
            
        elif "open linkedin" in query:
            webbrowser.open("https://www.linkedin.com/")
            speak("Thank you master, You will be redirected to LinkedIn soon.")
            
        elif "open github" in query:
            webbrowser.open("https://github.com/")
            speak("Thank you master, You will be redirected to GitHub soon.")
            
        elif "open meet" in query:
            webbrowser.open("https://meet.google.com/")   
            speak("Thank you master, You will be redirected to Google Meet soon.") 

        elif "open facebook" in query:
            webbrowser.open("https://www.facebook.com/")
            speak("Thank you master, You will be redirected to Facebook soon.")

        elif "play music" in query:
            music_dir = 'D:\\music'  # Change this path as needed
            songs = safe_file_operation(music_dir, "list")
            if songs:
                print(songs)    
                safe_file_operation(os.path.join(music_dir, songs[0]))
                speak("Playing music for you master")
            else:
                speak("Sorry master, I couldn't find your music directory.")

        elif "play video" in query:
            speak("ok master i am playing videos")
            video_dir = 'D:\\video'  # Change this path as needed
            videos = safe_file_operation(video_dir, "list")
            if videos and len(videos) > 1:
                safe_file_operation(os.path.join(video_dir, videos[1]))
            else:
                speak("Sorry master, I couldn't find your video directory or videos.")

        elif "play song on cloud" in query:
            speak("tell me the song name!")
            p = takecommand()
            if p != "none":
                webbrowser.open(f"https://soundcloud.com/search?q={p}")
                speak("Now playing on SoundCloud")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Master, the time is {strTime}. Hope you are not late. Have a good day.")

        elif "open pdf" in query:
            # Updated to use a more generic path - user should modify this
            pdf_path = input("Please enter the full path to your PDF file: ")
            if safe_file_operation(pdf_path):
                speak("Opening PDF file.")
            
        elif "open teams" in query:
            # More flexible Teams opening
            teams_paths = [
                'C:/Users/Hp/AppData/Local/Microsoft/Teams/Update.exe --processStart "Teams.exe"',
                'C:/Program Files/Microsoft/Teams/Update.exe --processStart "Teams.exe"',
                'C:/Program Files (x86)/Microsoft/Teams/Update.exe --processStart "Teams.exe"'
            ]
            
            opened = False
            for path in teams_paths:
                if safe_file_operation(path.split(' --')[0]):
                    os.system(f'"{path}"')
                    speak("Thank you master, You will be redirected to Teams App.")
                    opened = True
                    break
            
            if not opened:
                speak("Sorry master, I couldn't find Microsoft Teams on your system.")

        elif "open code blocks" in query:
            codeblocks_paths = [
                "C:/Program Files/CodeBlocks/codeblocks.exe",
                "C:/Program Files (x86)/CodeBlocks/codeblocks.exe"
            ]
            
            opened = False
            for path in codeblocks_paths:
                if safe_file_operation(path):
                    speak("Thank you master, You will be redirected to Code Blocks.")
                    opened = True
                    break
            
            if not opened:
                speak("Sorry master, I couldn't find Code Blocks on your system.")

        elif "open vs code" in query:
            vscode_paths = [
                "C:/Users/Hp/AppData/Local/Programs/Microsoft VS Code/Code.exe",
                "C:/Program Files/Microsoft VS Code/Code.exe",
                "C:/Program Files (x86)/Microsoft VS Code/Code.exe"
            ]
            
            opened = False
            for path in vscode_paths:
                if safe_file_operation(path):
                    speak("Thank you master, You will be redirected to VS Code.")
                    opened = True
                    break
            
            if not opened:
                # Try opening through command line
                try:
                    os.system('code')
                    speak("Thank you master, You will be redirected to VS Code.")
                except:
                    speak("Sorry master, I couldn't find VS Code on your system.")
            
        elif "open command prompt" in query:
            os.system('start cmd')
            speak("Thank you master, You will be redirected to Command Prompt.")
            
        elif "why you came" in query:
            speak("Thanks to the session conducted by IEEE RAIT session, I am Jinnie version 1.O created by Aayushi Mittal. further its secret")
            
        elif "you live" in query:
            speak("I live in desert island magic Lamp. It's all so magical and lonely. Phenomenal cosmic powers ... Itty bitty living space.")    
      
        elif "who" in query:
            speak("The ever impressive, the long contained, often imitated, but never duplicated … Jinnie of the lamp!")    

        elif "how" in query:
            speak("Thank you master for asking me this question. I am Wonderful, magnificent, glorious, punctual!. What about you")  

        elif "your name" in query:
            speak("Thanks for Asking my name, myself Jinnie aka Aladin ka Jin naam to suna hoga")  
            
        elif "age" in query:
            speak("Ten thousand years will give you such a crick in the neck!") 
            
        elif "good" in query:
            speak("Splendid! Absolutely marvelous!")  
             
        elif "hi" in query:
            speak("Hi, myself Jinnie aka Aladin ka Jin naam to suna hoga version 1.O. How you doing master")
 
        elif "send mail" in query:
            try:
                speak("What should I say?")
                content = takecommand()
                if content != "none":
                    to = input("Enter recipient email address: ")
                    if sendEmail(to, content):
                        speak("Email has been sent successfully!")
                    else:
                        speak("Sorry master, I couldn't send the email. Please check your credentials.")
            except Exception as e:
                speak("Sorry, I am not able to send this email. Better Luck next time")

        elif "exit" in query:
            speak("thanks for using me Master, apologies for annoying you, have a good day... Exit Jinnie version 1.O")
            sys.exit()
            
        elif "treasure" in query:
            speak("CAVE OF WONDERS...") 
            speak("Who disturbs my slumber?")  
            speak("The diamond in the rough!")    
            speak("Touch nothing but the lamp.")  
            speak("YOU HAVE TOUCHED THE FORBIDDEN TREASURE! NOW YOU WILL NEVER AGAIN SEE THE LIGHT OF DAY!")  
            speak("Exit Jinnie version 1.O")
            sys.exit()
            
        elif "cave of wonder" in query:
            speak("Who disturbs my slumber?")  
            speak("The diamond in the rough!")    
            speak("Touch nothing but the lamp.")  
            speak("YOU HAVE TOUCHED THE FORBIDDEN TREASURE! NOW YOU WILL NEVER AGAIN SEE THE LIGHT OF DAY!")  
            speak("Exit Jinnie version 1.O")
            sys.exit()
            
        elif "free" in query:
            speak("Im free. Im free Quick, wish for something outrageous, say, I want the Nile. Wish for the Nile, try that.")  
            speak("Im history, no, Im mythology, no, I don't care what I am Im free")
            speak("Im free, I'm free at last, Im hitting the road, Im off to see the world! Im.")    
            speak("Im gonna to miss you. No matter what anyone says, you'll always be a prince to me.")  
            speak("Thank you and bye bye")  
            speak("Exit Jinnie version 1.O")
            sys.exit()
        
        else:
            speak("hmmm..... ")
            speak("That... is quite a big wish you got there. Do you have anything more reasonable?")
            print("You can try these:")
            print("\n* open google \n* open youtube \n* the time \n* wikipedia [topic] \n* send mail \n* play music \n* open vs code \n* free \nmuch more ...\n")
