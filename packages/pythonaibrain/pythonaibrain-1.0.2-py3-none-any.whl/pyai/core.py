import os
import json
import random
import re
import nltk
import pyjokes
import importlib.resources
import yfinance as yf
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from collections import Counter
from functools import lru_cache

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import subprocess
import webbrowser
from .Grammar import correct_grammar
from .eye import EYE
from .MathAI import MathAI
from .Camera import Start
from .Search import Search
import json
from typing import List

Help = """# PythonAI Brain
Make your first offline AI Assistant in python. No complex setup, No advance coding. No API key required. Just install configure and run!
## Installation
Install pythonaibrain package.
```bash
pip install pythonaibrain==1.0.2
```

## Modules
- Camera
- TTS
- PTT
- Context
- Brain
- Advance Brain

### Camera
PyAI supports Camera to click photos, make videos and scane QR and Bar Code, it can save photos or videos and also send Images and Videos to PyAI to take answer

#### Example
For start your camera
```python
# Import modules
import pyai
from pyai import Camera
import tkinter as tk
from tkinter import *

root = tk.Tk() # Create the GUI
Camera(root) # Call the Function and pass the master as root
root.mainloop() # Start GUI app
```
Or, 
```python
from pyai.Camera import Start
Start()
```

Or, 
``` python
from pyai import Brain

brain = Brain ()
brain.process_messages('Click Photo')
```

From this you can easly use camera in your program.

## TTS
TTS stands for **Text To Speech**, it convert text into both **Male** voice and **Female** voice.

### Example
``` python
# Import modules
import pyai
from pyai import TTS

tts = TTS(text = 'Hello World')
tts.say(voice= 'Male') # for male voice
tts.say(voice= 'Female') #for female voice
```

> tts.say() -> By default it takes Male voice
> tts.say(voice= 'Male') -> Pass the voice as Male
> tts.say(voice= 'Female') -> Pass the voice as Female

## PTT
PTT stands for **PDF To Text**, it can extract text from a given image

### Example
```python
# Import modules
import pyai
from pyai import PTT

ptt = PTT(path = 'example.jpeg') # You can change example.jpeg from your file name
print(ppt) # PTT returns the text extract from the given pdf
```

### Syntax
```python
ITT(path: str = None)
```

Give your own file path.

## Context
It is a module in pyai which can able to extract answers from the give context

### Example
```python
# Import modules
import pyai
from pyai import Contexts

context = '''
Patanjali Ayurved is an Indian company. It was founded by Baba Ramdev and Acharya Balkrishna in 2006.
'''

question = 'Who founded Patanjali Ayurved?'
contexts = Contexts()
answer = contexts.ask(context= context, question= question)
```
Or, Also
```python
# Import modules
import pyai
from pyai import Contexts as contexts

context = '''
Patanjali Ayurved is an Indian company. It was founded by Baba Ramdev and Acharya Balkrishna in 2006.
'''

question = 'Who founded Patanjali Ayurved?'
answer = contexts.ask(context= context, question= question)
```

## Brain
It's a simple brain module which configure the input message.

### What it does
It classify the input message and find the type of message, like

- Question
- Answer
- Command
- Shutdown
- Make Directory
- Statement
- Name
- Know
- Start

It also extract the name, location, and age from the given message, by using NER.

#### Question
The Brain Module classify the given message weather it is a question or something else if answer then returns Question.

#### Answer
The Brain Module classify the given message weather it is a answer or something else if answer then returns Answer.

#### Command
The Brain Module classify the given message weather it is a command or something else if command then returns Command

#### Shutdown
The Brain Module also classify the given message weather the given command shutdown or not if it is then it shutdown your device and it returns Shutdown

But there are few issue releated to it :
- This command doesn't support website to run this command, because it need a terminal support.
- This doesn't run or work on Android, IOS.

#### Make Directory
The Brain Module also classify the given message weather the given command Make Directory or not if it is then it create a Directory on your device and returns Make Dir.

It generally comes under File handling of the PyAI Module which is also known as fh.

#### Statement
The Brain Module also classify the given message weather the given command statement or not, if it is then it statement then it returns Statement.

Statement -> It means a simple text which is not a question, answer, command, etc...  It a simple text. Like for example:
```text
The sun rises in the east.
```

#### Name
The Brain Module also classify the given message weather the given command name or not, if it is then it name then it returns Name.

Name -> It means the input message is caring name or specify the name like

```text
I'm Divyanshu.

Myself Divyanshu.

Divyanshu Sinha
```

#### Know
Know is similar to Statement.

```text
Do you know ___ ?
```
Like that.

#### Start
The Brain Module also classify the given message weather the given command start or not, if it is then it start any thing on your device and it returns Start.

Like:
```text
Start www.youtube.com
```
Or,
```text
Start Notepad
```

But it have issue:
- It doesn't works with website, because it support terminals like CMD for Window and etc.
- It also doesn't works in Android, IOS.

### How to create intents.json
You should know how to create a *intents.json* for run this **Brain Module**.

#### Pattern to create a *intents.json* file:
```json
{
    "intents":[{
        "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey", "What's up?", "Howdy", "Greetings", "Hi there", "Is anyone there?", "Yo!"],
      "responses": ["Hello! How can I help you today?", "Hey there!", "Hi! What can I do for you?"]
    },
    {
        "tag": "bye",
        "pattern": ["By", "See you soon", "See u soon", "Take care"],
        "responce":["Bye! have a greate day", "See you"]
    },
    ]
}
```
From this way you can create your own database.
> Remember this Database file in .json

### How to use **Brain Module**
To use **Brain Module** we should import Brain from **PyAI**

```python
from pyai import Brain
```

After importing the Module we use it in our main program as,

```python
brain = Brain(intents_path= 'intents.json') # Use can replace intents.json with you database file name but extention should be same (.json)

# Also Use
brain = Brain() # This will also work
```

After this, we predict the message type of we can say classify the message

```python
message = input('Message : ')
message_type = brain.predict_message_type(message= message) # On using predict_message_type() function we get the type of message is (question, answer, statement, command, shutdown, make directory, name, know, etc...)
```
By gating the message type, we find the perfect answer for the message
```python
if message_type in ['Question', 'Answer']:
    print(f'Answer : {brain.process_messages(message = message)}')

```
From these things you can create your own AI Assistant. But this is basic.

For Advance we can use Advance Brain Module.
### Advance Brain
This is advance version of **Brain Module**
It work like Brain but smartly.

### What it does
It classify the input message and find the type of message, like

- Question
- Answer
- Command
- Shutdown
- Make Directory
- Statement
- Name
- Know
- Start

It also extract the name, location, and age from the given message, by using NER.

#### Question
The Brain Module classify the given message weather it is a question or something else if answer then returns Question.

#### Answer
The Brain Module classify the given message weather it is a answer or something else if answer then returns Answer.

#### Command
The Brain Module classify the given message weather it is a command or something else if command then returns Command

#### Shutdown
The Brain Module also classify the given message weather the given command shutdown or not if it is then it shutdown your device and it returns Shutdown

But there are few issue releated to it :
- This command doesn't support website to run this command, because it need a terminal support.
- This doesn't run or work on Android, IOS.

#### Make Directory
The Brain Module also classify the given message weather the given command Make Directory or not if it is then it create a Directory on your device and returns Make Dir.

It generally comes under File handling of the PyAI Module which is also known as fh.

#### Statement
The Brain Module also classify the given message weather the given command statement or not, if it is then it statement then it returns Statement.

Statement -> It means a simple text which is not a question, answer, command, etc...  It a simple text. Like for example:
```text
The sun rises in the east.
```

#### Name
The Brain Module also classify the given message weather the given command name or not, if it is then it name then it returns Name.

Name -> It means the input message is caring name or specify the name like

```text
I'm Divyanshu.

Myself Divyanshu.

Divyanshu Sinha
```

#### Know
Know is similar to Statement.

```text
Do you know ___ ?
```
Like that.

#### Start
The Brain Module also classify the given message weather the given command start or not, if it is then it start any thing on your device and it returns Start.

Like:
```text
Start www.youtube.com
```
Or,
```text
Start Notepad
```

But it have issue:
- It doesn't works with website, because it support terminals like CMD for Window and etc.
- It also doesn't works in Android, IOS.

### How to create intents.json
You should know how to create a *intents.json* for run this **Advance Brain Module**.

#### Pattern to create a *intents.json* file:
```json
{
    "intents":[{
        "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey", "What's up?", "Howdy", "Greetings", "Hi there", "Is anyone there?", "Yo!"],
      "responses": ["Hello! How can I help you today?", "Hey there!", "Hi! What can I do for you?"]
    },
    {
        "tag": "bye",
        "pattern": ["By", "See you soon", "See u soon", "Take care"],
        "responce":["Bye! have a greate day", "See you"]
    },
    ]
}
```
From this way you can create your own database.
> Remember this Database file in .json

## How to use **Advance Brain Module**
To use **Advance Brain Module** we should import Brain from **PyAI**

```python
from pyai import AdvanceBrain
```

After importing the Module we use it in our main program as,

```python
advance_brain = AdvanceBrain(intents_path= 'intents.json') # Use can replace intents.json with you database file name but extention should be same (.json)

# Also
advance_brain = AdvanceBrain() # This also work
```

After this, we predict the message type of we can say classify the message

```python
message = input('Message : ')
message_type = advance_brain.predict_message_type(message= message) # On using predict_message_type() function we get the type of message is (question, answer, statement, command, shutdown, make directory, name, know, etc...)
```
By gating the message type, we find the perfect answer for the message
```python
if message_type in ['Question', 'Answer']:
    print(f'Answer : {advance_brain.process_messages(message = message)}')

```

## Python AI Modules and their use
| Module Name | Description |
| :---: | :---:|
|Brain| It is use to create Brain for AI by passing **.json** file (or, **Knowledge for Brain**)|
|AdvanceBrain|It is use to create Advance Brain for AI by passing **.json** file (or, **Knowledge for Brain**). It can understand better than Brain|
|TTS|Convert text into Voice|
|PTT|PDF into Text|
|Camera|Use camera to click photos and make videos|
|Context|Get Answer from the context for the respective question|



## PythonAI Brain also provides built-in AI Assistant
If you don't want to create your own AI assistant by coding or you want to see how this modules work you can also use PyBrain which is a built-in python AI assistance, provided by pythonaibrain == 1.0.2

### How to use it
```python
import PyBrain
PyBrain('-g')
```

By using this you can use PyBrain in GUI.

Or,
```python
import PyBrain
PyBrain('-w')
```
By using this you can use PyBrain in Web.

Or,
```python
import PyBrain
PyBrain('-h')
```
By using this Help panel open.

---
### Visit [PyPI](https://pypi.org/project/pythonaibrain/1.0.2) for installation.
"""

class IntentsManager:
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file
        self.data = self._load_intents()

    def _load_intents(self) -> dict:
        if os.path.exists(self.intents_file):
            try:
                with open(self.intents_file, 'r') as f:
                    return json.load(f)

            except FileNotFoundError:
                path = importlib.resources.files(__package__) / intents_file
                with path.open("r", encoding="utf-8") as f:
                    return json.load(f)

            else:
                here = os.path.dirname(__file__)
                with open(os.path.join(here, intents_file), encoding="utf-8") as f:
                    return json.load(f)

        else:
             # If file does not exist or is invalid, start fresh
            return {"intents": []}

    def save(self):
        try:
            with open(self.intents_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception:
            try:
                path = importlib.resources.files(__package__) / self.intents_file
                with path.open("w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=4)
            except Exception:
                here = os.path.dirname(__file__)
                fallback_path = os.path.join(here, self.intents_file)
                with open(fallback_path, 'w', encoding="utf-8") as f:
                    json.dump(self.data, f, indent=4)

    def add_search_intent(self, query: str, search_results: List[str]):
        """
        Adds or updates an intent for a search query with search results.

        :param query: The original user search query string.
        :param search_results: List of strings representing the search summaries.
        """
        tag = f"search_{query.strip().lower().replace(' ', '_')[:30]}"  # limit length

        # Prepare the new intent
        new_intent = {
            "tag": tag,
            "patterns": [query],
            "responses": search_results if search_results else ["Sorry, no results found."]
        }

        # Check if intent with this tag exists
        intents = self.data.get('intents', [])
        for intent in intents:
            if intent['tag'] == tag:
                # Update existing intent responses (add new responses without duplicates)
                existing_responses = set(intent.get('responses', []))
                updated_responses = list(existing_responses.union(search_results))
                intent['responses'] = updated_responses
                # Optionally, also update patterns if needed
                if query not in intent.get('patterns', []):
                    intent['patterns'].append(query)
                self.save()
                return

        # If not found, append the new intent
        intents.append(new_intent)
        self.data['intents'] = intents
        self.save()

# ----- Sample Training Data -----

class NERDataset(Dataset):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]

class NERModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, tagset_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, tagset_size)

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.lstm(embedded)
        tag_scores = self.fc(output)
        return tag_scores

class NERTagger:
    def __init__(self, train_data, max_len=100, embed_dim=64, hidden_dim=128):
        self.max_len = max_len
        self.train_data = train_data

        # Build vocabulary and tags
        self.word_counter = Counter()
        self.tag_set = set()

        for words, tags in train_data:
            self.word_counter.update(words)
            self.tag_set.update(tags)

        self.word2idx = {w: i+1 for i, w in enumerate(self.word_counter)}
        self.word2idx["<PAD>"] = 0

        self.tag2idx = {t: i for i, t in enumerate(self.tag_set)}
        self.idx2tag = {i: t for t, i in self.tag2idx.items()}

        # Encode data
        self.X, self.Y = self.encode_dataset(train_data)

        # Create dataset and dataloader
        self.dataset = NERDataset(torch.tensor(self.X), torch.tensor(self.Y))
        self.loader = DataLoader(self.dataset, batch_size=2, shuffle=True)

        # Initialize model
        self.model = NERModel(len(self.word2idx), embed_dim, hidden_dim, len(self.tag2idx))
        self.loss_function = nn.CrossEntropyLoss(ignore_index=self.tag2idx.get("O", -100))
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

    def encode(self, words, tags):
        x = [self.word2idx.get(w, 0) for w in words]
        y = [self.tag2idx[t] for t in tags]

        if len(x) < self.max_len:
            pad_len = self.max_len - len(x)
            x += [0] * pad_len
            y += [self.tag2idx.get("O", 0)] * pad_len
        return x[:self.max_len], y[:self.max_len]

    def encode_dataset(self, dataset):
        X = []
        Y = []
        for words, tags in dataset:
            x, y = self.encode(words, tags)
            X.append(x)
            Y.append(y)
        return X, Y

    def train(self, epochs=10):
        print('NER TRANING STARTED!')
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for inputs, labels in self.loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)

                outputs = outputs.view(-1, len(self.tag2idx))
                labels = labels.view(-1)

                loss = self.loss_function(outputs, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            #print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(self.loader):.4f}")
            print('NER TRANING COMPLETED!')

    def predict(self, sentence):
        self.model.eval()
        with torch.no_grad():
            words = sentence.split()
            x = [self.word2idx.get(w, 0) for w in words]
            if len(x) < self.max_len:
                x += [0] * (self.max_len - len(x))
            x = torch.tensor([x])
            outputs = self.model(x)
            preds = torch.argmax(outputs, dim=2)[0].tolist()
            tags = [self.idx2tag[p] for p in preds[:len(words)]]
            return list(zip(words, tags))

def predict_entities(message: str = "I'm PYAI"):
    # Prepare your training data in format: list of (words_list, tags_list)
    train_data = [

        # --- Names ---
        (["My", "name", "is", "Aryan"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Divyanshu"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Priya"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Amit"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Neha"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Rahul"], ["O", "O", "O", "NAME"]),
        (["My", "name", "is", "Sneha"], ["O", "O", "O", "NAME"]),
        (["I", "am", "Meera"], ["O", "O", "NAME"]),
        (["He", "is", "Karan"], ["O", "O", "NAME"]),
        (["She", "is", "Anjali"], ["O", "O", "NAME"]),

        # --- Locations ---
        (["I", "live", "in", "Delhi"], ["O", "O", "O", "LOCATION"]),
        (["I", "live", "in", "Mumbai"], ["O", "O", "O", "LOCATION"]),
        (["I", "live", "in", "Patna"], ["O", "O", "O", "LOCATION"]),
        (["He", "is", "from", "Chennai"], ["O", "O", "O", "LOCATION"]),
        (["She", "stays", "in", "Bangalore"], ["O", "O", "O", "LOCATION"]),
        (["I", "am", "from", "Kolkata"], ["O", "O", "O", "LOCATION"]),
        (["I", "am", "Dev", "from", "Hyderabad"], ["O", "O", "NAME", "O", "LOCATION"]),

        # --- Ages ---
        (["I", "am", "19", "years", "old"], ["O", "O", "AGE", "O", "O"]),
        (["I", "am", "24", "years", "old"], ["O", "O", "AGE", "O", "O"]),
        (["She", "is", "22", "years", "old"], ["O", "O", "AGE", "O", "O"]),
        (["He", "is", "30"], ["O", "O", "AGE"]),
        (["I", "was", "born", "in", "2005"], ["O", "O", "O", "O", "AGE"]),
        (["Age", "is", "25"], ["O", "O", "AGE"]),
        (["My", "age", "is", "32"], ["O", "O", "O", "AGE"]),
    ]


    # Initialize tagger
    tagger = NERTagger(train_data)

    # Train model
    tagger.train(epochs=5)

    # Predict on a new sentence
    return tagger.predict(message)

class FrameClassifier(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(FrameClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.net(x)

class FrameClassifierEngine:
    def __init__(self, intents_path="intents.json"):
        self.frame_map = {
            0: "Statement", 1: "Question", 2: "Command", 3: "Answer",
            4: "Name", 5: "Know", 6: "Shutdown", 7: "Make Dir", 8: "Start"
        }

        self.command_keywords = {
            "shutdown": ["shutdown", "/s", "power off"],
            "start": ["start", "launch", "run"],
            "open": ["open", "show", "display"],
            "restart": ["restart", "reboot"],
            "mkdir": ["mkdir", "make directory"]
        }

        self.train_sentences = [
            "How are you?", "Open the door", "The sun rises in the east", "What time is it?",
            "Close the window", "She is reading a book", "Is this your pen?", "Start the engine",
            "He likes football", "Where do you live?", "1+1 is 2", "I am Divyanshu",
            "Myself Divyanshu", "Do you know", "Shutdown /s /t 0", "Mkdir", "Start"
        ]
        self.train_labels = [1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 4, 4, 5, 6, 7, 8]

        self.vectorizer = CountVectorizer()
        self.X_train = self.vectorizer.fit_transform(self.train_sentences).toarray()
        self.y_train = np.array(self.train_labels)

        self.X_tensor = torch.tensor(self.X_train, dtype=torch.float32)
        self.y_tensor = torch.tensor(self.y_train, dtype=torch.long)

        self.model = FrameClassifier(self.X_train.shape[1], len(self.frame_map))
        self.loss_fn = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)

        self.intents_path = intents_path
        self._load_intents()

    def _load_intents(self):
        if os.path.exists(self.intents_path):
            with open(self.intents_path, "r") as f:
                self.intents = json.load(f)
        else:
            self.intents = []

    def _save_intents(self):
        with open(self.intents_path, "w") as f:
            json.dump(self.intents, f, indent=2)

    def train(self, epochs=150):
        print("Training Frame Classifier...")
        for epoch in range(epochs):
            self.model.train()
            outputs = self.model(self.X_tensor)
            loss = self.loss_fn(outputs, self.y_tensor)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        print("Training Complete!")

    def predict(self, sentence):
        self.model.eval()
        vec = self.vectorizer.transform([sentence]).toarray()
        tensor = torch.tensor(vec, dtype=torch.float32)
        with torch.no_grad():
            output = self.model(tensor)
            predicted = torch.argmax(output, dim=1).item()
        return self.frame_map.get(predicted, "Unknown")

    def detect_command_type(self, sentence):
        for command, keywords in self.command_keywords.items():
            for kw in keywords:
                if kw.lower() in sentence.lower():
                    return command.upper()
        return "GENERIC_COMMAND"

    def handle_know_intent(self, sentence):
        for intent in self.intents:
            for pattern in intent["patterns"]:
                if pattern.lower() in sentence.lower():
                    return np.random.choice(intent["responses"])
        
        # Auto-learn new "know" question
        new_intent = {
            "tag": "auto_learned",
            "patterns": [sentence],
            "responses": ["I don't know that yet, but I've learned it now."]
        }
        self.intents.append(new_intent)
        self._save_intents()
        return new_intent["responses"][0]

    def classify(self, sentence):
        frame = self.predict(sentence)

        if frame == "Command":
            cmd_type = self.detect_command_type(sentence)
            return cmd_type
        
        elif frame == "Know":
            #reply = self.handle_know_intent(sentence)
            #return reply
            return "Know"

        else:
            return frame
engine = FrameClassifierEngine()
engine.train()
def predict_frame(sentence):
    return engine.classify(sentence)

# ────────────────────────────────────────────────
# 🔤 UTILS
# ────────────────────────────────────────────────
def tokenize(text):
    return [ord(c) for c in text.lower()]

def pad_sequence(seq, max_len):
    return seq + [0] * (max_len - len(seq))


# ────────────────────────────────────────────────
# 🧠 MODEL
# ────────────────────────────────────────────────
class LanguageClassifierModel(nn.Module):
    def __init__(self, vocab_size=256, embed_dim=32, hidden_dim=64, output_size=4):
        super(LanguageClassifierModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        x = self.embedding(x)
        _, h_n = self.rnn(x)
        return self.fc(h_n.squeeze(0))


# ────────────────────────────────────────────────
# 📦 DATA PREP
# ────────────────────────────────────────────────
def prepare_language_data(data):
    texts = [tokenize(t[0]) for t in data]
    labels = [t[1] for t in data]
    max_len = max(len(t) for t in texts)
    X = [pad_sequence(t, max_len) for t in texts]
    le = LabelEncoder()
    y = le.fit_transform(labels)

    X = torch.tensor(X, dtype=torch.long)
    y = torch.tensor(y, dtype=torch.long)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    return X_train, X_test, y_train, y_test, le, max_len


# ────────────────────────────────────────────────
# 🏋️ TRAINING
# ────────────────────────────────────────────────
def train_language_classifier(X_train, y_train, output_size, epochs=100):
    print ('Traning Started!')
    model = LanguageClassifierModel(output_size=output_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            acc = (outputs.argmax(1) == y_train).float().mean()
            #print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}, Accuracy: {acc:.2f}")
    print('Traning Completed!')
    
    return model


# ────────────────────────────────────────────────
# 🔍 INFERENCE
# ────────────────────────────────────────────────
def predict_language(text, model, label_encoder, max_len):
    model.eval()
    tokens = tokenize(text)
    padded = pad_sequence(tokens, max_len)
    input_tensor = torch.tensor([padded], dtype=torch.long)
    with torch.no_grad():
        output = model(input_tensor)
        pred = output.argmax(1).item()
    return label_encoder.inverse_transform([pred])[0]


# ────────────────────────────────────────────────
# 🧪 TEST FUNCTION
# ────────────────────────────────────────────────
def language_classifier(message: str = 'Hello'):
    data = [
        ("hello how are you", "english"),
        ("what is your name", "english"),
        ("bonjour comment ça va", "french"),
        ("je m'appelle pierre", "french"),
        ("hola como estas", "spanish"),
        ("me llamo carlos", "spanish"),
        ("tum kaise ho", "hindi"),
        ("mera naam divyanshu hai", "hindi")
    ]

    # Prepare data
    X_train, X_test, y_train, y_test, le, max_len = prepare_language_data(data)

    # Train model
    model = train_language_classifier(X_train, y_train, output_size=len(le.classes_))

    return predict_language(message, model, le, max_len)

# ───────────────────────────────────────────────
# 🔤 VOCAB HELPERS
# ───────────────────────────────────────────────
def build_vocab(sentences):
    vocab = {"<pad>": 0, "<sos>": 1, "<eos>": 2}
    idx = 3
    for sentence in sentences:
        for word in sentence.lower().split():
            if word not in vocab:
                vocab[word] = idx
                idx += 1
    return vocab

def encode(sentence, vocab):
    return [vocab[word] for word in sentence.lower().split()]

def pad(seq, max_len):
    return seq + [0] * (max_len - len(seq))

# ───────────────────────────────────────────────
# 📦 DATASET
# ───────────────────────────────────────────────
class TranslationDataset(Dataset):
    def __init__(self, corpus, src_vocab, tgt_vocab):
        self.pairs = corpus
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab
        self.max_src_len = max(len(s.split()) for s, _ in corpus)
        self.max_tgt_len = max(len(t.split()) for _, t in corpus) + 1

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        src, tgt = self.pairs[idx]
        src_enc = encode(src, self.src_vocab)
        tgt_enc = [1] + encode(tgt, self.tgt_vocab) + [2]  # <sos> ... <eos>
        src_pad = pad(src_enc, self.max_src_len)
        tgt_pad = pad(tgt_enc, self.max_tgt_len)
        return torch.tensor(src_pad), torch.tensor(tgt_pad)

# ───────────────────────────────────────────────
# 🧠 MODELS
# ───────────────────────────────────────────────
class Encoder(nn.Module):
    def __init__(self, input_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(input_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, x):
        x = self.embed(x)
        _, hidden = self.rnn(x)
        return hidden

class Decoder(nn.Module):
    def __init__(self, output_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(output_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, x, hidden):
        x = self.embed(x.unsqueeze(1))
        output, hidden = self.rnn(x, hidden)
        output = self.fc(output.squeeze(1))
        return output, hidden

# ───────────────────────────────────────────────
# 🏋️ TRAINING
# ───────────────────────────────────────────────
def train_translator(corpus, epochs=100):
    source_sentences = [src for src, _ in corpus]
    target_sentences = [tgt for _, tgt in corpus]
    src_vocab = build_vocab(source_sentences)
    tgt_vocab = build_vocab(target_sentences)
    src_ivocab = {v: k for k, v in src_vocab.items()}
    tgt_ivocab = {v: k for k, v in tgt_vocab.items()}

    dataset = TranslationDataset(corpus, src_vocab, tgt_vocab)
    loader = DataLoader(dataset, batch_size=1, shuffle=True)

    encoder = Encoder(len(src_vocab), 32, 64)
    decoder = Decoder(len(tgt_vocab), 32, 64)

    enc_optim = optim.Adam(encoder.parameters(), lr=0.005)
    dec_optim = optim.Adam(decoder.parameters(), lr=0.005)
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for epoch in range(epochs):
        total_loss = 0
        for src, tgt in loader:
            enc_optim.zero_grad()
            dec_optim.zero_grad()
            hidden = encoder(src)

            loss = 0
            dec_input = tgt[:, 0]
            for t in range(1, tgt.size(1)):
                output, hidden = decoder(dec_input, hidden)
                loss += loss_fn(output, tgt[:, t])
                dec_input = tgt[:, t]

            loss.backward()
            enc_optim.step()
            dec_optim.step()
            total_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            #print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")
            pass

    return encoder, decoder, dataset, src_vocab, tgt_vocab, tgt_ivocab

# ───────────────────────────────────────────────
# 🔍 TRANSLATE
# ───────────────────────────────────────────────
def translate(text, encoder, decoder, dataset, src_vocab, tgt_ivocab):
    encoder.eval()
    decoder.eval()
    src = encode(text, src_vocab)
    src = pad(src, dataset.max_src_len)
    src_tensor = torch.tensor([src])
    hidden = encoder(src_tensor)

    dec_input = torch.tensor([1])  # <sos>
    result = []

    for _ in range(dataset.max_tgt_len):
        output, hidden = decoder(dec_input, hidden)
        pred = output.argmax(1).item()
        if pred == 2:
            break
        result.append(tgt_ivocab.get(pred, "?"))
        dec_input = torch.tensor([pred])

    return " ".join(result)

def translate_to_en(message: str = ""):
    corpus = [
        ("mera naam ravi hai", "my name is ravi"),
        ("tum kaise ho", "how are you"),
        ("hola como estas", "hello how are you"),
        ("je m'appelle pierre", "my name is pierre"),
        ("my name is ravi", "my name is ravi")
    ]

    # Step 2: Train
    encoder, decoder, dataset, src_vocab, tgt_vocab, tgt_ivocab = train_translator(corpus)
    return translate(message, encoder, decoder, dataset, src_vocab, tgt_ivocab)


class FrameClassifierAdvance(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.net(x)

class FramePredictorAdvance:
    def __init__(self, sentences, labels, class_map):
        self.vectorizer = CountVectorizer()
        self.X_train = self.vectorizer.fit_transform(sentences).toarray()
        self.y_train = np.array(labels)
        self.class_map = class_map
        self.model = FrameClassifierAdvance(self.X_train.shape[1], len(class_map))

    def train(self, epochs=150):
        print("Frame Classifier Training Started!")
        X_tensor = torch.tensor(self.X_train, dtype=torch.float32)
        y_tensor = torch.tensor(self.y_train, dtype=torch.long)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)

        for epoch in range(epochs):
            self.model.train()
            outputs = self.model(X_tensor)
            loss = loss_fn(outputs, y_tensor)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (epoch + 1) % 10 == 0:
                #print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
                pass
        print("Frame Classifier Training Complete!")

    def predict(self, sentence):
        input_vec = self.vectorizer.transform([sentence]).toarray()
        input_tensor = torch.tensor(input_vec, dtype=torch.float32)
        with torch.no_grad():
            output = self.model(input_tensor)
            predicted = torch.argmax(output, dim=1).item()
        return self.class_map.get(predicted)

class NERDatasetAdvance(Dataset):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]

class NERModelAdvance(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, tagset_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, tagset_size)

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.lstm(embedded)
        return self.fc(output)

class NERTrainerAdvance:
    def __init__(self, train_data, max_len=100):
        self.max_len = max_len
        self.train_data = train_data
        self.word2idx = {}
        self.tag2idx = {}
        self.idx2tag = {}

        self.build_vocab()
        self.model = NERModelAdvance(len(self.word2idx), 64, 64, len(self.tag2idx))

    def build_vocab(self):
        word_counter = Counter()
        tag_set = set()
        for words, tags in self.train_data:
            word_counter.update(words)
            tag_set.update(tags)
        self.word2idx = {w: i + 1 for i, w in enumerate(word_counter)}
        self.word2idx["<PAD>"] = 0
        self.tag2idx = {t: i for i, t in enumerate(tag_set)}
        self.idx2tag = {i: t for t, i in self.tag2idx.items()}

    def encode(self, words, tags):
        x = [self.word2idx.get(w, 0) for w in words]
        y = [self.tag2idx[t] for t in tags]
        if len(x) < self.max_len:
            pad_len = self.max_len - len(x)
            x += [0] * pad_len
            y += [self.tag2idx["O"]] * pad_len
        return x[:self.max_len], y[:self.max_len]

    def train(self, epochs=50, batch_size=2):
        X, Y = [], []
        for words, tags in self.train_data:
            x, y = self.encode(words, tags)
            X.append(x)
            Y.append(y)

        X = torch.tensor(X)
        Y = torch.tensor(Y)
        dataset = NERDatasetAdvance(X, Y)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)

        for epoch in range(1, epochs + 1):
            self.model.train()
            total_loss = 0
            for batch_x, batch_y in loader:
                optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = criterion(outputs.view(-1, len(self.tag2idx)), batch_y.view(-1))
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            if epoch % 10 == 0:
                print(f"Epoch {epoch} Loss: {total_loss:.4f}")
        print("NER Training Complete!")

    def predict(self, sentence):
        self.model.eval()
        tokens = word_tokenize(sentence)
        encoded, _ = self.encode(tokens, ["O"] * len(tokens))
        input_tensor = torch.tensor([encoded])
        with torch.no_grad():
            outputs = self.model(input_tensor)
            predictions = torch.argmax(outputs, dim=2).squeeze().tolist()
        entities = {"NAME": None, "AGE": None, "LOCATION": None}
        for token, pred in zip(tokens, predictions):
            label = self.idx2tag.get(pred, "O")
            if label in entities and entities[label] is None:
                entities[label] = token
        return entities


class ChatbotModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(ChatbotModel, self).__init__()

        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)

        return x

class ChatbotAssistant:
    def __init__(self, intents_path, condition= True, function_mapping=None):
        self.model = None
        self.intents_path = intents_path
        self.documents = []
        self.vocabulary = []
        self.intents = []
        self.intents_responses = {}
        self.function_mapping = function_mapping

        self.X = None
        self.Y = None

    @staticmethod
    def tokenize_and_lemmatizer(text):
        lemmatizer = nltk.WordNetLemmatizer()

        words = nltk.word_tokenize(text)
        words = [lemmatizer.lemmatize(word.lower()) for word in words]

        return words

    def bag_of_words(self, words):
        return [1 if word in words else 0 for word in self.vocabulary]

    def parse_intents(self):
        lemmatizer = nltk.WordNetLemmatizer()

        if os.path.exists(self.intents_path):
            try:
                with open(self.intents_path, 'r') as f:
                    intents_data = json.load(f)

            except FileNotFoundError:
                path = importlib.resources.files(__package__) / "intents.json"
                with path.open("r", encoding="utf-8") as f:
                    intents_data = json.load(f)

            else:
                here = os.path.dirname(__file__)
                with open(os.path.join(here, "intents.json"), encoding="utf-8") as f:
                    intents_data = json.load(f)

            for intent in intents_data['intents']:
                if intent['tag'] not in self.intents:
                    self.intents.append(intent['tag'])
                    self.intents_responses[intent['tag']] = intent['responses']

                for pattern in intent['patterns']:
                    pattern_words = self.tokenize_and_lemmatizer(pattern)
                    self.vocabulary.extend(pattern_words)
                    self.documents.append([pattern_words, intent['tag']])

            self.vocabulary = sorted(set(self.vocabulary))

    def prepare_data(self):
        bags = []
        indices = []

        for document in self.documents:
            words = document[0]
            bag = self.bag_of_words(words)

            intent_index = self.intents.index(document[1])

            bags.append(bag)
            indices.append(intent_index)

        self.X = np.array(bags)
        self.Y = np.array(indices)

    def train_model(self, batch_size, lr, epochs):
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        Y_tensor = torch.tensor(self.Y, dtype=torch.long)

        dataset = TensorDataset(X_tensor, Y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = ChatbotModel(self.X.shape[1], len(self.intents))

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)  # lr stands for learning rate

        print('Model Traning!')
        for epoch in range(epochs):
            running_loss = 0.0

            for batch_X, batch_Y in loader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_Y)
                loss.backward()
                optimizer.step()
                running_loss += loss

        print("Model Training complete.")

    def save_model(self, model_path, dimension_path):
        torch.save(self.model.state_dict(), model_path)

        with open(dimension_path, 'w') as f:
            json.dump({'input_size': self.X.shape[1], 'output_size': len(self.intents)}, f)

    def load_model(self, model_path, dimension_path):
        with open(dimension_path, 'r') as f:
            dimensions = json.load(f)

        self.model = ChatbotModel(dimensions['input_size'], dimensions['output_size'])
        self.model.load_state_dict(torch.load(model_path, weights_only=True))

    #@lru_cache(maxsize = None)
    def process_message(self, input_message):
        words = self.tokenize_and_lemmatizer(input_message)
        bag = self.bag_of_words(words)

        bag_tensor = torch.tensor([bag], dtype=torch.float32)

        self.model.eval()

        with torch.no_grad():
            predictions = self.model(bag_tensor)

        predicted_class_index = torch.argmax(predictions, dim=1).item()
        predicted_intent = self.intents[predicted_class_index]

        if predicted_intent == "python_code_execution":  # If the intent is to execute Python code
            return self.execute_code(input_message)

        if predicted_intent == "joke":  # If the intent is to execute joke
            return pyjokes.get_joke()

        if predicted_intent == 'click':
            data = Start()
            return data

        if predicted_intent == 'fallback_search':
            intents_manager = IntentsManager(self.intents_path)
            s = Search(input_message)
            s.run()
            search_summaries = s.get_results_str()
            if condition:
                intents_manager.add_search_intent(input_message, search_summaries)
            else:
                pass
            return search_summaries

        if predicted_intent == 'solve_math_problem':
            return MathAI(input_message)

        if predicted_intent == "see_me":
            eye = EYE()
            if 'person' in eye:
                return 'Yes! I can see you.'

        if predicted_intent == 'TTS' or predicted_intent == 'speak':
            return 'TTS'

        if predicted_intent == "help":
            return Help

        if predicted_intent == "open" or predicted_intent == "search":
            return list("OPEN", predicted_intent.replace('open', '') or predicted_intent.replace('search', ''))

        if self.intents_responses[predicted_intent]:
            return correct_grammar(random.choice(self.intents_responses[predicted_intent]))

        else:
            return "I didn't understand that."

    def execute_code(self, query):
        try:
            code = query.split('run python')[-1].strip()  # Extracting the Python code from the message
            # Run the code
            local_scope = {}
            exec(code, {"__builtins__": None}, local_scope)  # Restricting the built-ins to None
            result = local_scope.get('result', 'No output')  # Get the result of execution
            return f"The result of the Python code is: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

def predictFrameAdvance(sentence: str | None = None):
    train_sentences = [
    "How are you?",
    "Open the door",
    "The sun rises in the east",
    "What time is it?",
    "Close the window",
    "She is reading a book",
    "Is this your pen?",
    "Start the engine",
    "He likes football",
    "Where do you live?",
    "1+1 is 2",
    "I am Divyanshu",
    "Myself Divyanshu",
    "Do you know",
    "Shutdown /s /t 0",
    "Mkdir",
    "Start"
    ]

    frame_map = {0: "Statement", 1: "Question", 2: "Command", 3: "Answer", 4: "Name", 5: "Know", 6: "Shutdown", 7: "Make Dir", 8: "Start"}
    train_labels = [1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 4, 4, 5, 6, 7, 8]

    predict_frames = FramePredictorAdvance(train_sentences, train_labels, frame_map)
    return predict_frames.predict(sentence)

def predictNER(sentence: str | None = ''):
    train_data = [
    (["My", "name", "is", "Aryan"],         ["O", "O", "O", "NAME"]),
    (["My", "name", "is", "Divyanshu"],         ["O", "O", "O", "NAME"]),
    (["My", "name", "is", "Vaishnavi"],         ["O", "O", "O", "NAME"]),
    (["My", "name", "is", "Bhumi"],         ["O", "O", "O", "NAME"]),
    (["My", "name", "is", "Yesh"],         ["O", "O", "O", "NAME"]),
    (["I", "live", "in", "Jaipur"],         ["O", "O", "O", "LOCATION"]),
    (["I", "am", "19", "years", "old"],     ["O", "O", "AGE", "O", "O"]),
    (["She", "is", "Meera"],                ["O", "O", "NAME"]),
    (["She", "stays", "in", "Goa"],         ["O", "O", "O", "LOCATION"]),
    (["Age", "is", "24"],                   ["O", "O", "AGE"]),
    (["I", "am", "Dev", "from", "Lucknow"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "Jamshedpur"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "Munger"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "Patna"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "Rachi"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "India"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["I", "am", "Dev", "from", "Jamalpur"], ["O", "O", "NAME", "O", "LOCATION"]),
    (["born", "in", "2003"],                ["O", "O", "AGE"]),
    (["I", "am", "Dev", "from", "Lucknow", ".", "My", "age", "is", "19"], ["O", "O", "NAME", "O", "LOCATION", "O", "O", "O", "O", "AGE"]),
    ]

    return NERTrainerAdvance(train_data).predict(sentence)

class Brain:
    def __init__(self, intents_path: str = r'.\intents.json', condition= True, **function_mapping) -> None:
        self.assistant = ChatbotAssistant(intents_path, condition, function_mapping=function_mapping)

        self.assistant.parse_intents()
        self.assistant.prepare_data()
        self.assistant.train_model(8, 0.001, 100)

    def translator(self, message: str | None = None) -> str:
        '''It is used to translate message into english.'''
        return translate_to_en(message)

    def classify_language(self, message: str | None = None) -> str:
        '''
        1. english.
        2. hindi.
        3. french.
        4. spanish
        '''
        return language_classifier(message)

    def predict_message_type(self, message: str | None = None) -> str:
        '''It Returns:
            1. Statement.
            2. Question.
            3. Answer.
            4. Command.
            5. Shutdown.
            6. Name.
            7. Know.
            8. Make Dir.
            9. Start.'''
        return predict_frame(message)

    def pyai_say(self, *message, **options) -> None:
        print('PYAI :',*message, **options)

    def predict_entitie(self, message: str | None = None) -> str:
        '''It Returns:
            1. NAME.
            2. AGE.
            3. LOCATION.'''
        return predict_entities(message)

    def process_messages(self, message: str | None = None) -> str:
        return self.assistant.process_message(message)

class AdvanceBrain:
    def __init__(self, intents_path: str | None = r'.\intents.json', condition = True, **function_mapping) -> None:
        self.assistant = ChatbotAssistant(intents_path, condition, **function_mapping)
        self.assistant.parse_intents()
        self.assistant.prepare_data()
        self.assistant.train_model(8, 0.001, 100)

    def translator(self, message: str | None = None) -> str:
        '''It is used to translate message into english.'''
        return translate_to_en(message)

    def classify_language(self, message: str | None = None) -> str:
        '''
        1. english.
        2. hindi.
        3. french.
        4. spanish
        '''
        return language_classifier(message)

    def predict_message_type(self, message: str | None = None) -> str:
        '''It Returns:
            1. Statement.
            2. Question.
            3. Answer.
            4. Command.
            5. Shutdown.
            6. Name.
            7. Know.
            8. Make Dir.
            9. Start.'''
        return predictFrameAdvance(message)

    def predict_entitie(self, message: str | None = None) -> str:
        '''It Returns:
            1. NAME.
            2. AGE.
            3. LOCATION.'''
        return predictNER(message)

    def pyai_say(self, *message, **options) -> None:
        print('PYAI :',*message, **options)
        return ''

    def process_messages(self, message: str | None = None) -> str:
        return self.assistant.process_message(message)

__all__ = [
    'Brain',
    'AdvanceBrain'
]
