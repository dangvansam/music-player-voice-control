import pyttsx3
engine = pyttsx3.init()

def t2s(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
    