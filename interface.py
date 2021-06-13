from tkinter import *
import tkinter as tk
import speech_recognition as sr
listener = sr.Recognizer()
import pyttsx3
engine = pyttsx3.init()
import time
import main



my_text = "Tap to talk !"

root=Tk()

root.geometry('800x670+100+30')
root.title('ChatBot created by Dahouari-Sabri-Bartaouch')
root.config(bg='gray')

logoPic=PhotoImage(file='pic.png')

logoPicLabel=Label(root,image=logoPic,bg='gray')
logoPicLabel.pack(pady=5)

centerFrame=Frame(root)
centerFrame.pack()


textarea=Text(centerFrame,font=('times new roman',20,'bold'),height=10, wrap='word')
scrollbar=Scrollbar(centerFrame,orient="vertical", command=textarea.yview)

textarea.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill="y")
textarea.pack(side="left",fill="both", expand=True)
textarea.see(END)
textarea.yview_pickplace(END)
textarea.yview(END)

textarea.tag_config('warning', background="yellow", foreground="red")
textarea.tag_config('blue', foreground="blue")
textarea.tag_config('green', foreground="green")


questionField=Entry(root,font=('verdana',20,'bold'))
questionField.pack(pady=15,fill=X)



askPic=PhotoImage(file='ask.png')
mic=PhotoImage(file='mic.png')




def botReply():
    if questionField.get()!='':
        textarea.config(state="normal")
        command = questionField.get()
        textarea.insert(END, 'You : ')
        textarea.insert(END, command+"\n", 'blue')
        res = main.getResponse(questionField.get())
        textarea.insert(END, 'KIK : ')
        textarea.insert(END, res+"\n\n",'green')
        textarea.config(state="disabled")
        questionField.delete(0,'end')
        #talk(res)
        


def talk(message):
    engine.say(message)
    engine.runAndWait()
    engine.stop()


askButton=Button(root,image=askPic, height = 80, width = 90,command=botReply)
askButton.pack(side=RIGHT)


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
        
    return command

##

def deleteText():
    textarea.config(state="normal")
    textarea.delete('1.0',END)
    textarea.config(state="disabled")

myButton=Button(root, text='Clear conversation',bg='gray', fg='red', height=2, width=20, command=deleteText).place(x=320,y=610)
#btnListening=Button(root, text='start .....',bg='gray', fg='red', height=2, width=20)
#btnListening.pack(side=TOP, anchor=NW)
def listening():
    #btnListening['text']="Listening ..."
    startTalkingButton['state'] = DISABLED
    command=take_command()
    questionField.insert(0,command)
    botReply()
    startTalkingButton['state'] = NORMAL
    #btnListening['text']=""


startTalkingButton = Button(root,image=mic, text ="TALK", fg='red', height = 80, width = 90, command = listening)
startTalkingButton.pack(side=LEFT)

def click(event):
    askButton.invoke()

def intro():
    textarea.config(state="normal")
    textarea.insert('end', "  Starting ...  ".center(50,'*')+"\n", 'warning')
    textarea.config(state="disabled")

def deleteText():
    textarea.config(state="normal")
    textarea.delete('1.0',END)
    textarea.config(state="disabled")
def startChat():
    textarea.config(state="normal")
    textarea.insert(END, "KIK : ")
    textarea.insert(END, "Welcome Sir"+"\n\n",'green')
    textarea.config(state="disabled")
    talk("Welcome Sir")


root.bind('<Return>',click)



root.after(90, intro)
#root.after(100, main.runningBot)
root.after(100, deleteText)
root.after(120, startChat)


root.mainloop()
