import pyttsx3
import os
from ourClass.ClassFunctionsOS import Commands, Windows_system
engine = pyttsx3.init()
project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"  # Вставляем  ID  выбранного  голоса
engine.setProperty('voice', voice_id)

class voiceControlCommands(Commands):
    @staticmethod
    def speak(text, dop1, voice_response):
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

if __name__ == "__main__":
    voiceControlCommands.speak('ааа', False, True)