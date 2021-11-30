import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 125)
rate = engine.getProperty('rate')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("My current speaking rate is " + str(rate))
engine.runAndWait()