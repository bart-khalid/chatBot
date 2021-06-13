import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from pyjokes import jokes_de
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow as tf 
from tensorflow.python.framework import ops
import random
import json
import pickle
import speech_recognition as sr
listener = sr.Recognizer()
import pyttsx3
engine = pyttsx3.init()
import pywhatkit
import datetime
import wikipedia
import pyjokes
import cv2
from playsound import playsound as ps


with open("intents.json", encoding="utf8") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

#tf.reset_default_graph()
ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=100, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)



# say mesessage
def talk(message):
    engine.say(message)
    engine.runAndWait()
    engine.stop()

# recognise voice
voices = engine.getProperty('voices')
def take_command():
    command = ''
    while command == '':
        try:
            with sr.Microphone() as source:
                print('listening...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice, language="en-US")
                command = command.lower()
                if 'KIK' in command:
                    command = command.replace('KIK', '')
                    print(command)
        except:
            pass  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return command   


def getResponse(command):
    respose = ''
    if 'play' in command:
        song = command.replace('play', '')
        #print('Bot : playing ' + song)
        #talk('playing ' + song)
        pywhatkit.playonyt(song)
        #print("Bot : "+'enjoy, I found it for you')
        #talk('enjoy, I found it for you')
        response = 'playing ' +song+',    enjoy, I found it for you'
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        #print('Bot : Current time is ' + time)
        #talk('Current time is ' + time)
        response = 'Current time is ' + time
    elif 'who is' in command :
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        #print("Bot : "+info)
        #talk(info)
        response = info
    elif 'tell me about' in command:
        person = command.replace('tell me about', '')
        info = wikipedia.summary(person, 1)
        #print("Bot : "+info)
        #talk(info)
        response = info
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        #print("Bot : "+joke)
        #talk(joke)
        response = joke
    else :
        results = model.predict([bag_of_words(command, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        responsee = random.choice(responses)
        #print("Bot : "+ responsee)        
        #talk(responsee)
        response = responsee
    return response

def runningBot():
    try :
        ps('intro.mp3')
    except: 
        print("can't open the audio")


def chat():
    
    while True:
        inp = take_command()
        #inp = input("You: ")
        print("you : "+inp)
        if inp.lower() == "quit" or inp.lower() == "thala":
            break
        getResponse(inp)
        
#chat()