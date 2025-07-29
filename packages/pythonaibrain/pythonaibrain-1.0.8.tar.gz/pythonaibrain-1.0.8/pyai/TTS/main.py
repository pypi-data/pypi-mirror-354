import subprocess
try:
    import win32com.client
except:
    subprocess.run(['pip', 'install', 'pywin32'])
    import win32com.client
import pyttsx3
import sys

voice_list = ['microsoft david desktop', 'microsoft zira desktop', 'microsoft mark desktop']

class TTS:
    def __init__(self, text: str | None = 'Hello from Py AI') -> None:
        self.text = text

    def OsType(self) -> str:
        return sys.platform

    def say(self, voice: str | None = 'Male', **name) -> None:
        if voice.lower() == 'male':
            index = 0

        elif voice.lower() == 'female':
            index = 1

        else:
            print(f'Invalid voice name : {voice}')
            index = 0

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[index].id)

        engine.say(self.text)
        engine.runAndWait()

def speak(text: str = 'Hi', voice: str | None = 'Male'):
    TTS(text).say(voice= voive)
