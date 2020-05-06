import pyttsx3
engine = pyttsx3.init()

def t2s(text):
    engine.say(text)
    engine.runAndWait()
    