
py -m <pip_install>"C:\AI ASSISTANT JARVIS\pycopy-webbrowser-0.0.0.tar.gz"
py -m <pip_install>"C:\AI ASSISTANT JARVIS\pyttsx3-2.90-py3-none-any.whl"
py -m <pip_install>"C:\AI ASSISTANT JARVIS\SpeechRecognition-3.8.1-py2.py3-none-any.whl"
py -m <pip_install>"C:\AI ASSISTANT JARVIS\wikipedia-1.4.0.tar.gz"

import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia



# this method is for taking the commands
# and recognizing the command from the
# speech_Recognition module we will use
# the recongizer method for recognizing
def takeCommand():

	r = sr.Recognizer()

	# from the speech_Recognition module
	# we will use the Microphone module
	# for listening the command
	with sr.Microphone() as source:
		print('Listening')
		
		# seconds of non-speaking audio before
		# a phrase is considered complete
		r.pause_threshold = 0.7
		audio = r.listen(source)
		
		# Now we will be using the try and catch
		# method so that if sound is recognized
		# it is good else we will have exception
		# handling
		try:
			print("Recognizing")
			
			# for Listening the command in indian
			# english we can also use 'hi-In'
			# for hindi recognizing
			Query = r.recognize_google(audio, language='en-in')
			print("the command is printed=", Query)
			
		except Exception as e:
			print(e)
			print("Say that again sir")
			return "None"
		
		return Query

def speak(audio):
	
	engine = pyttsx3.init()
	# getter method(gets the current value
	# of engine property)
	voices = engine.getProperty('voices')
	
	# setter method .[0]=male voice and
	# [1]=female voice in set Property.
	engine.setProperty('voice', voices[1].id)
	
	# Method for the speaking of the assistant
	engine.say(audio)
	
	# Blocks while processing all the currently
	# queued commands
	engine.runAndWait()

def tellDay():
	
	# This function is for telling the
	# day of the week
	day = datetime.datetime.today().weekday() + 1
	
	#this line tells us about the number
	# that will help us in telling the day
	Day_dict = {1: 'Monday', 2: 'Tuesday',
				3: 'Wednesday', 4: 'Thursday',
				5: 'Friday', 6: 'Saturday',
				7: 'Sunday'}
	
	if day in Day_dict.keys():
		day_of_the_week = Day_dict[day]
		print(day_of_the_week)
		speak("The day is " + day_of_the_week)


def tellTime():
	
	# This method will give the time
	time = str(datetime.datetime.now())
	
	# the time will be displayed like
	# this "2020-06-05 17:50:14.582630"
	#nd then after slicing we can get time
	print(time)
	hour = time[11:13]
	min = time[14:16]
	speak(self, "The time is sir" + hour + "Hours and" + min + "Minutes")

def Hello():
	
	# This function is for when the assistant
	# is called it will say hello and then
	# take query
	speak("Hello i am your virtual assistant")
	

def Take_query():

	# calling the Hello function for
	# making it more interactive
	Hello()
	
	# This loop is infinite as it will take
	# our queries continuously until and unless
	# we do not say bye to exit or terminate
	# the program
	while(True):
		
		# taking the query and making it into
		# lower case so that most of the times
		# query matches and we get the perfect
		# output
		query = takeCommand().lower()
		if "open gmail" in query:
			speak("Opening Gmail ")
			
			# in the open method we just to give the link
			# of the website and it automatically open
			# it in your default browser
			webbrowser.open("www.gmail.com")
			continue
		
		elif "open google" in query:
			speak("Opening Google ")
			webbrowser.open("www.google.com")
			continue
			
		elif "which day it is" in query:
			tellDay()
			continue
		
		elif "tell me the time" in query:
			tellTime()
			continue
		
		elif "give me the news" in query:
		        speak("Opening news")
		        webbrowser.open("https://microsoftstart.msn.com/")
		        continue
		        
		elif "give me a currency converter" in query:
			speak("opening a currency converter")
			webbrowser.open("https://www.calculator.net/currency-calculator.html")
			continue
                
		elif "Show me how you look" in query:
			speak(" ok i wil show how i look with the browser")
			webbrowser.open("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.altivex.studio%2Fuk%2Fjournal%2Fai-is-here-to-stay-heres-why%2F&psig=AOvVaw2_R78K1kSJfh4auTHWBVc0&ust=1668953632041000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCLjj1PS2uvsCFQAAAAAdAAAAABAK")
			continue
                
		elif "Open Youtube" in query:
			speak("opening YouTube.com")
			webbrowser.open("https://www.youtube.com/")
			continue

		elif "Open Paypal" in query:
			speak("opening Paypal")
			webrowser.open("https://www.paypal.com/")
			continue
                        
		# this will exit and terminate the program
		elif "bye" in query:
			speak("Bye. Check Out GFG for more exciting things")
			exit()
		
		elif "from wikipedia" in query:
			
			# if any one wants to have a information
			# from wikipedia
			speak("Checking the wikipedia ")
			query = query.replace("wikipedia", "")
			
			# it will give the summary of 4 lines from
			# wikipedia we can increase and decrease
			# it also.
			result = wikipedia.summary(query, sentences=4)
			speak("According to wikipedia")
			speak(result)
		
		elif "tell me your name" in query:
			speak("I am Jane. Your desktop Assistant")

if __name__ == '__main__':
	
	# main method for executing
	# the functions
	Take_query()
