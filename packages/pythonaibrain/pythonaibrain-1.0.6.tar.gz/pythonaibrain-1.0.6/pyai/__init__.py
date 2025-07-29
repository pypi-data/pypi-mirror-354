from .core import Brain, AdvanceBrain
from .TTS import TTS
from .TTS import TTS as text
#from .STT import STT, STTModel
from .Camera import Camera
from .Camera import Start
from .Context import Contexts as contexts
from .Context import Contexts
from .Memory import Memory
from .Memory import Memory as memory
#from .TTI import TTI
import nltk

if input('Want to download nltk data (y/n) : ').lower()[0] == "y":
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
    nltk.download('treebank', quiet=True)
    nltk.download('brown', quiet=True)
    nltk.download('conll2000', quiet=True)
    nltk.download('movie_reviews', quiet=True)
    nltk.download('names', quiet=True)
    nltk.download('gazetteers', quiet=True)
    nltk.download('tagsets', quiet=True)
    nltk.download('help/tagsets', quiet=True)

__doc__ = """
PythonAI Brain
Make your first AI Assistant in python. No complex setup, No advance coding. Just install configure and run!

Installation
Install pythonaibrain package.

pip install pythonaibrain==1.0.6
Modules
Camera
TTS
PTT
Memory
Context
Brain
Advance Brain
Camera
PyAI supports Camera to click photos and make videos, it can save photos or videos and also send Images and Videos to PyAI to take answer

Example
For start your camera

# Import modules
import pyai
from pyai import Camera
import tkinter as tk
from tkinter import *

root = tk.Tk() # Create the GUI
Camera(root) # Call the Function and pass the master as root
root.mainloop() # Start GUI app
From this you can easly use camera in your program.

Or,

from pyai.Camera import Start
Start()

Or,

from pyai import Brain

brain = Brain()
brain.process_messages('Click Photo')

TTS
TTS stands for Text To Speech, it convert text into both Male voice and Female voice.

Example
# Import modules
import pyai
from pyai import TTS

tts = TTS(text = 'Hello World')
tts.say(voice= 'Male') # for male voice
tts.say(voice= 'Female') #for female voice
tts.say() -> By default it takes Male voice tts.say(voice= 'Male') -> Pass the voice as Male tts.say(voice= 'Female') -> Pass the voice as Female


PTT
PTT stands for PDF To Text, it can extract text from a given image

Example
# Import modules
import pyai
from pyai import PTT

itt = ITT(path = 'example.jpeg') # You can change example.jpeg from your file name
text = itt.outputs() # It returns the text extract from the given image
Syntax
PTT(path: str = None)
Give your own file path.

Context
It is a module in pyai which can able to extract answers from the give context

Example
# Import modules
import pyai
from pyai import Contexts

context = '''
Patanjali Ayurved is an Indian company. It was founded by Baba Ramdev and Acharya Balkrishna in 2006.
'''

question = 'Who founded Patanjali Ayurved?'
contexts = Contexts()
answer = contexts.ask(context= context, question= question)
Or, Also

# Import modules
import pyai
from pyai import Contexts as contexts

context = '''
Patanjali Ayurved is an Indian company. It was founded by Baba Ramdev and Acharya Balkrishna in 2006.
'''

question = 'Who founded Patanjali Ayurved?'
answer = contexts.ask(context= context, question= question)
Brain
It's a simple brain module which configure the input message.

What it does
It classify the input message and find the type of message, like

Question
Answer
Command
Shutdown
Make Directory
Statement
Name
Know
Start
It also extract the name, location, and age from the given message, by using NER.

Question
The Brain Module classify the given message weather it is a question or something else if answer then returns Question.

Answer
The Brain Module classify the given message weather it is a answer or something else if answer then returns Answer.

Command
The Brain Module classify the given message weather it is a command or something else if command then returns Command

Shutdown
The Brain Module also classify the given message weather the given command shutdown or not if it is then it shutdown your device and it returns Shutdown

But there are few issue releated to it :

This command doesn't support website to run this command, because it need a terminal support.
This doesn't run or work on Android, IOS.
Make Directory
The Brain Module also classify the given message weather the given command Make Directory or not if it is then it create a Directory on your device and returns Make Dir.

It generally comes under File handling of the PyAI Module which is also known as fh.

Statement
The Brain Module also classify the given message weather the given command statement or not, if it is then it statement then it returns Statement.

Statement -> It means a simple text which is not a question, answer, command, etc... It a simple text. Like for example:

The sun rises in the east.
Name
The Brain Module also classify the given message weather the given command name or not, if it is then it name then it returns Name.

Name -> It means the input message is caring name or specify the name like

I'm Divyanshu.

Myself Divyanshu.

Divyanshu Sinha
Know
Know is similar to Statement.

Do you know ___ ?
Like that.

Start
The Brain Module also classify the given message weather the given command start or not, if it is then it start any thing on your device and it returns Start.

Like:

Start www.youtube.com
Or,

Start Notepad
But it have issue:

It doesn't works with website, because it support terminals like CMD for Window and etc.
It also doesn't works in Android, IOS.
How to create intents.json
You should know how to create a intents.json for run this Brain Module.

Pattern to create a intents.json file:
{
    "intents":[{
        "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey", "What's up?", "Howdy", "Greetings", "Hi there", "Is anyone there?", "Yo!"],
      "responses": ["Hello! How can I help you today?", "Hey there!", "Hi! What can I do for you?"]
    },
    {
        "tag": "bye",
        "patterns": ["By", "See you soon", "See u soon", "Take care"],
        "responces":["Bye! have a greate day", "See you"]
    },
    ]
}
From this way you can create your own database.

Remember this Database file in .json

How to use Brain Module
To use Brain Module we should import Brain from PyAI

from pyai import Brain
After importing the Module we use it in our main program as,

brain = Brain(intents_path= 'intents.json') # Use can replace intents.json with you database file name but extention should be same (.json). Or u can also use Brain() it can also work
After this, we predict the message type of we can say classify the message

message = input('Message : ')
message_type = brain.predict_message_type(message= message) # On using predict_message_type() function we get the type of message is (question, answer, statement, command, shutdown, make directory, name, know, etc...)
By gating the message type, we find the perfect answer for the message

if message_type in ['Question', 'Answer']:
    print(f'Answer : {brain.process_messages(message = message)}')

From these things you can create your own AI Assistant. But this is basic.

For Advance we can use Advance Brain Module.

Advance Brain
This is advance version of Brain Module It work like Brain but smartly.

What it does
It classify the input message and find the type of message, like

Question
Answer
Command
Shutdown
Make Directory
Statement
Name
Know
Start
It also extract the name, location, and age from the given message, by using NER.

Question
The Brain Module classify the given message weather it is a question or something else if answer then returns Question.

Answer
The Brain Module classify the given message weather it is a answer or something else if answer then returns Answer.

Command
The Brain Module classify the given message weather it is a command or something else if command then returns Command

Shutdown
The Brain Module also classify the given message weather the given command shutdown or not if it is then it shutdown your device and it returns Shutdown

But there are few issue releated to it :

This command doesn't support website to run this command, because it need a terminal support.
This doesn't run or work on Android, IOS.
Make Directory
The Brain Module also classify the given message weather the given command Make Directory or not if it is then it create a Directory on your device and returns Make Dir.

It generally comes under File handling of the PyAI Module which is also known as fh.

Statement
The Brain Module also classify the given message weather the given command statement or not, if it is then it statement then it returns Statement.

Statement -> It means a simple text which is not a question, answer, command, etc... It a simple text. Like for example:

The sun rises in the east.
Name
The Brain Module also classify the given message weather the given command name or not, if it is then it name then it returns Name.

Name -> It means the input message is caring name or specify the name like

I'm Divyanshu.

Myself Divyanshu.

Divyanshu Sinha
Know
Know is similar to Statement.

Do you know ___ ?
Like that.

Start
"The Brain Module classifies the given message whether the given command start or not, if it is then it start any thing on your device and it returns Start.

Like:

Start www.youtube.com
Or,

Start Notepad
But it have issue:

It doesn't works with website, because it support terminals like CMD for Window and etc.
It also doesn't works in Android, IOS.
How to create intents.json
You should know how to create a intents.json for run this Advance Brain Module.

Pattern to create a intents.json file:
{
    "intents":[{
        "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey", "What's up?", "Howdy", "Greetings", "Hi there", "Is anyone there?", "Yo!"],
      "responses": ["Hello! How can I help you today?", "Hey there!", "Hi! What can I do for you?"]
    },
    {
        "tag": "bye",
        "patterns": ["By", "See you soon", "See u soon", "Take care"],
        "responce":["Bye! have a greate day", "See you"]
    },
    ]
}
From this way you can create your own database.

Remember this Database file in .json

How to use Advance Brain Module
To use Advance Brain Module we should import Brain from PyAI

from pyai import AdvanceBrain
After importing the Module we use it in our main program as,

advance_brain = AdvanceBrain(intents_path= 'intents.json') # Use can replace intents.json with you database file name but extention should be same (.json). Or, can also do Advancebrain() It also works.
After this, we predict the message type of we can say classify the message

message = input('Message : ')
message_type = advance_brain.predict_message_type(message= message) # On using predict_message_type() function we get the type of message is (question, answer, statement, command, shutdown, make directory, name, know, etc...)
By gating the message type, we find the perfect answer for the message

if message_type in ['Question', 'Answer']:
    print(f'Answer : {advance_brain.process_messages(message = message)}')

Python AI Modules and their use
| Module Name | Description | | :---: | :---:| |Brain| It is use to create Brain for AI by passing .json file (or, Knowledge for Brain)| |AdvanceBrain|It is use to create Advance Brain for AI by passing .json file (or, Knowledge for Brain). It can understand better than Brain| |TTS|Convert text into Voice| |STT|Convert Voice into Text| |TTI|Convert Text into Image| |ITT|Convert Or, extract Image into Text| |Camera|Use camera to click photos and make videos| |Context|Get Answer from the context for the respective question|

PythonAI Brain also provides built-in AI Assistant
If you don't want to create your own AI assistant by coding or you want to see how this modules work you can also use PyBrain which is a built-in python AI assistance, provided by pythonaibrain == 1.0.2

How to use it
import PyBrain
PyBrain('-g')
By using this you can use PyBrain in GUI.

Or,

import PyBrain
PyBrain('-w')
By using this you can use PyBrain in Web.

Or,

import PyBrain
PyBrain('-h')
By using this Help panel open.

Visit PyPI for installation."""

__version__ = "1.0.6"
__author__ = "Divyanshu Sinha"
__all__ = [
    "Brain",
    "AdvanceBrain",
    "TTS",
    "PTT",
    "Camera",
    "Contexts",
    "Memory",
]
