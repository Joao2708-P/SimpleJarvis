import requests
import speech_recognition as sr
import pyttsx3 as tts3  # Biblioteca de texto em voz'
import pywhatkit
import datetime
import wikipedia
import bs4

wikipedia.set_lang('pt')
# voices = engine.getProperty('voices') #Alterando para uma voz feminina
#  # setando a voz feminina

listenner = sr.Recognizer()
engine = tts3.init()
engine.setProperty('voice', 'brazil')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_Comand():
    try:
        with sr.Microphone() as source:
            print("Fale...")
            voice = listenner.listen(source)
            comand = listenner.recognize_google(voice, language='pt-BR')
            comand = comand.lower()
            if 'jarvis' in comand:
                comand = comand.replace('jarvis', '')
                print(comand)
    except:
        pass
    return comand

def run_jarvis():

    comand = take_Comand()
    
    if 'play' in comand:
        song = comand.replace('play', '')
        pywhatkit.playonyt(song)
        talk("Musica tocando " + song)
        print("Tocando...")

    elif 'horas' in comand:
        hora = datetime.datetime.now().strftime('%H:%M')
        talk("Agora são: " + hora + "horas")
        print(hora)

    elif 'pesquisar' in comand:
        comando = comand.replace('pesquisar', '')
        result = wikipedia.summary(comando, 2)
        talk(result)
        print(result)

    else:
        print("Desculpe não entendi")
run_jarvis()