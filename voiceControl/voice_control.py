# main.py
import os
import time
import vosk
from vosk import Model, KaldiRecognizer
import re
import json
import ctypes
from ctypes import wintypes
import pycaw
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import subprocess #для управления
import shutil #для управления
import pyautogui #для управления
import pywinauto.application
from pywinauto.application import Application
from cryptography.fernet import Fernet
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pyttsx3
from json import loads
import webbrowser
import datetime
import requests
import pywinauto
import time
import pyaudio
import pyautogui
import threading
from ourClass.ClassFunctionsOS import Windows_system, Commands
from ourClass.ClassVoiceControlCommands import voiceControlCommands
from ourClass.ClassOllamaVoiceQuestion import ollamaVoiceQuestion

path_helper_name = '../.txt/voiceControl/helper_name.txt'

def _helper_name():
    global path_helper_name
    with open(path_helper_name, 'r', encoding="utf-8") as file:
        helper_name = file.readline()
    return helper_name.title()

def _new_helper_name(new_name):
    with open(path_helper_name, 'w', encoding="utf-8") as file:
        file.write(new_name.title())
    return new_name

if (_helper_name() == None) or not (os.path.exists(path_helper_name)):
    with open(path_helper_name, 'w', encoding="utf-8") as file:
        file.write('Компьютер')
    print('Установлено имя по умолчанию (Компютер)')


def voice_control():
    volume_deffolt = 10
    voice_response = False
    dop1 = False
    hotKay = False
    passsword = "12345"
    helper_name = _helper_name()

    engine = pyttsx3.init()
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"  # Вставляем  ID  выбранного  голоса
    engine.setProperty('voice', voice_id)
    print("Запуск...")
    model_path = f'../VoiceModels/vosk-model-small-ru-0.22'
    print(model_path)
#C:\Users\Пользователь\PycharmProjects\PythonProject1\.venv\VoiceModels\vosk-model-small-ru-0.22
    FRAME_RATE = 16000
    CHANNELS=1
    MICROPHONE_ID = 1
    sleep = 0

    if not os.path.exists(model_path):
        print("Ошибка: Модель Vosk не найдена!")
        exit(1)
    print(0)
    if model_path != 0:
        model = Model(model_path)
        print("Модель загружена")
    else:
        print("Ошибка загрузки модели")
        exit(1)





    def speak(text):
        if text:
            sempai = " семпай"
            
            if dop1 == True:
                text = text + sempai
                #
            if voice_response == True:
                engine.say(text)
                engine.runAndWait()
                print(text)
                return text
            else:
                print(text)
                return text
        else:
            pass


    def recognize_speech():  # Упрощаем функцию
        while True:
            data = stream.read(8192)  # Читаем данные
            if len(data) == 0:  # Проверяем на пустые данные
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())  # Сразу парсим JSON
                if 'text' in result:
                    return result['text'].lower()
        return None  # Возвращаем None, если ничего не распознано
    

    if not os.path.exists(model_path):
        print("Ошибка: Модель Vosk не найдена!")
        exit(1)
    print(0)
    if model_path != 0:
        model = Model(model_path)
        print("Модель загружена")
    else:
        print("Ошибка загрузки модели")
        exit(1)

    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=FRAME_RATE, input=True, input_device_index=MICROPHONE_ID, frames_per_buffer=8192)  # Увеличили буфер
    stream.start_stream()
    print('\n')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n')
    print(f'Меня зовут {helper_name}')
    print("Готово, слушаю...")
    while True:
        text = recognize_speech()

        if text:

            print(f"Распознано: {text}")
            if helper_name.lower() in text.lower(): 
                speak("Слушаю")
                while True:
                    text = recognize_speech()
                    if text:
                        if sleep >= 2:
                            break
                        print(f"Вы: {text}")
                        if "выход" in text:  # 1
                            exit(0)

                        elif "сменить имя" in text.lower():  # 2
                            speak("Как вы хотите меня называть?")
                            new_name = recognize_speech()
                            if new_name:
                                helper_name = _new_helper_name(new_name)
                                speak(f"Хорошо, я теперь {helper_name}")

                        elif f"{helper_name} выключи комп" in text.lower():  # 3
                            speak("Выключаю компьютер!")
                            # os.system("shutdown /s /t 1") # выключить комп

                        elif ("--" in text.lower()) or (text.lower() == "команда один") or (("называй" in text.lower()) and ("меня" in text.lower()) and ("-" in text.lower())):  # 4
                            dop1 = True
                            speak("слушаюсь")

                        elif (f"ты теперь" in text.lower()):  # 5
                            new_name = re.search(r"ты теперь (.+)", text.lower())
                            if new_name:
                                helper_name = _new_helper_name(new_name.group(1))
                                speak(f"Хорошо, я теперь {helper_name}")

                        elif ("открой" in text.lower()) and ("хром" in text.lower()):  # 6
                            os.system("start Chrome")
                            # speak("эта функция не доступна так как мой создатель ленивая задница которая не хочет поднимать свою жопу со стула и идти пахать.")

                        elif ("найди в гугле" in text.lower() or "Найди в Гугле" in text.lower() or "найди в Гугле" in text.lower()):  # 7
                            match = re.search(r"найди в гугле (.+)",text.lower())  # Ищем текст "Найди в гугле" далее любой текст (.+)
                            if match:
                                query = match.group(1)  # Извлекаем запрос из текста
                                url = f"https://www.google.com/search?q={query}"  # Формируем URL поиска google
                                webbrowser.open(url)  # Открываем URL в браузере
                                speak(f"Поиск: {query}")

                        elif ("найди" in text.lower()):  # 7
                            match = re.search(r"найди (.+)",text.lower())  # Ищем текст "Найди в гугле" далее любой текст (.+)
                            if match:
                                query = match.group(1)  # Извлекаем запрос из текста
                                url = f"https://www.google.com/search?q={query}"  # Формируем URL поиска google
                                webbrowser.open(url)  # Открываем URL в браузере
                                speak(f"Поиск: {query}")

                        elif "перейди в спящий режим" in text.lower():  # 8
                            speak(None)
                            break

                        elif "давай поговорим" in text.lower():  # 9
                            new_voice_response = True
                            voice_response = new_voice_response
                            speak("хорошо, давайте поговорим")

                        elif ("хватит говорить" in text.lower()) or ("помолчи" in text.lower()):  # 10
                            new_voice_response = False
                            voice_response = new_voice_response
                            speak("хорошо")

                        elif "проверь окна" in text.lower():  # 11
                            speak("проверяю")
                            Windows_system.get_windows_info()

                        elif ("включи музыку" in text.lower()): #12
                            os.system('start Яндекс.Музыка')
                            speak("эта функция не доступна так как мой создатель ленивая задница которая не хочет поднимать свою жопу со стула и идти пахать.")

                        elif ("запусти сайт" in text.lower()): #13
                            #WebInterface()
                            #speak("негрз, негрз, негрз, негрз, не буду я запускать сайт")
                            webbrowser.open("http://127.0.0.1:5000")

                        elif ('запусти оперу' in text.lower()): #14
                            os.system('start Opera GX')

                        elif ("запусти командную строку" in text.lower()) or ("запусти консоль виндовс" in text.lower()): #15
                            os.system('start CMD')
                        #
                        elif ('сверни окно' in text.lower()):
                            sp = Windows_system.minimize_active_window()
                            speak(sp)

                        elif ('закрой окно' in text.lower()):
                            sp = Windows_system.close_active_window()
                            speak(sp)

                        elif ('переключи окно' in text.lower()) or ('смени окно' in text.lower()):
                            Windows_system._alt_tab()
                            speak('хорошо')

                        elif ('закрой все окна' in text.lower()) and ('выключи комп'):
                            speak('хорошо')
                            Windows_system.off_computer(18)

                        elif ('закрой все окна' in text.lower()):
                            Windows_system.close_windows(15)

                        elif ('сделай снимок экрана' in text.lower()):
                            Windows_system.screen()

                        elif ('пауза' in text.lower()) or ('старт' in text.lower()) or ('плей' in text.lower()):
                            Windows_system._pause()

                        elif (text == None):
                            sleep =+ 1
                            continue
                        else:
                            stream.stop_stream()
                            ai = ollamaVoiceQuestion()
                            ai_response = ai.get_llm_response_OUR(text)
                            speak(ai_response)
                            stream.start_stream()

                    else:

                        print("Ничего не услышал")  # Добавляем вывод если команда не распознана

    stream.stop_stream()
    stream.close()
    p.terminate()
    

if __name__ == "__main__":
    voice_control()
    


