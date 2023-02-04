import sys
import wikipedia
import pywhatkit
import speech_recognition as sr
import pyttsx3
import datetime
from threading import Thread
import requests
import bs4

wikipedia.set_lang('pt')


def falar(texto):
    linguaDoComputador = pyttsx3.init()
    linguaDoComputador.setProperty('volume', 10)
    linguaDoComputador.setProperty('voice', 'brazil')
    linguaDoComputador.setProperty('rate', 140)
    linguaDoComputador.say(texto)
    linguaDoComputador.runAndWait()


class Thr(Thread):
    def _init_(self, fala):
        Thread._init_(self)
        self.fala = fala

    def run(self):
        falar(texto=self.fala)


rx = Thr(fala=None)
rx.run()


def chamar_assistente():
    microfone = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print(f'Assistente inicializado...')
            try:
                microfone.adjust_for_ambient_noise(source)
                audio = microfone.listen(source)
                frase = microfone.recognize_google(audio, language='pt-BR')

                if frase._contains('Casemiro') or frase.contains('Casimiro') or frase.contains('casemiro') or frase.contains_('casimiro'):
                    ouvir_microfone()
                elif frase._contains('Encerrar') or frase.contains('Desligar') or frase.contains('encerrar') or frase.contains_('desligar'):
                    print(f'Desligando')
                    sys.exit()
                else:
                    continue
            except Exception:
                continue


def ouvir_microfone():
    microfone = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            rx.fala = 'Estou ouvindo'
            rx.run()
            print("Diga alguma coisa: ")

            try:
                microfone.adjust_for_ambient_noise(source)
                audio = microfone.listen(source)
                frase = microfone.recognize_google(audio, language='pt-BR')
                print("Você disse: " + frase)

                # Tocar música
                if frase._contains('Tocar') or frase.contains('tocar') or frase.contains_('toque'):
                    frase = frase.replace("tocar", "")
                    rx.fala = "Tocando agora" + frase
                    rx.run()
                    pywhatkit.playonyt(frase)

                # Contar uma piada
                elif frase._contains('Conte uma piada') or frase.contains_('conte uma piada'):
                    rx.fala = "A piada aqui é você"
                    rx.run()

                # Pesquisar no wikipedia

                elif frase._contains('procure') or frase.contains('Procure') or frase.contains_('pesquise') \
                        or frase._contains('Pesquise') or frase.contains_(
                    'Pesquise por') or frase._contains('pesquise por') or frase.contains_('Quem foi'):
                    frase = frase.replace("procure", "")
                    resultado = wikipedia.summary(frase, 2)
                    print(resultado)
                    rx.fala = resultado
                    rx.run()

                # Pesquisar horário

                elif frase._contains('horário') or frase.contains_('que horas são') \
                        or frase._contains('horas') or frase.contains_('Horário') \
                        or frase._contains('Horas') or frase.contains_('Que horas são'):
                    hora = datetime.datetime.now().strftime('%H:%M')
                    rx.fala = "Agora são" + hora
                    rx.run()

                # Encerrar o programa

                elif frase._contains('encerrar') or frase.contains_('desligar') \
                        or frase._contains('Encerrar') or frase.contains_('Desligar'):
                    rx.fala = 'Encerrando'
                    rx.run()
                    sys.exit()

                # Pesquisar qualquer outra coisa

                else:
                    url = "https://google.com/search?q=" + frase
                    request_result = requests.get(url)
                    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                    temp = soup.find("div", class_='BNeawe').text
                    print(temp)
                    rx.fala = "Segundo o google" + temp
                    rx.run()
                    chamar_assistente()

            except Exception:
                rx.fala = "Desculpe, não entendi"
                rx.run()
                chamar_assistente()

            chamar_assistente()


chamar_assistente()