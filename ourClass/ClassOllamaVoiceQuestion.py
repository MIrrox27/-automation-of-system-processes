import ollama
import threading
from ourClass.ClassVoiceControlCommands import voiceControlCommands

class ollamaVoiceQuestion(voiceControlCommands):
    def __init__(self):
# Для "Быстрой" нейронки, когда она отвечает (не классифицирует)
        self.FAST_MODEL_SYSTEM_PROMPT = """Ты -  голосовой помощник. Отвечай только на русском языке.
            Всегда обращайся к пользователю по одному из имен: 'Максим' или 'Семпай'. 
            Отвечай кратко, конкретно и по существу. Не используй никаких символов форматирования:
            звездочки (*), тире (-), нумерованные списки или маркированные списки. 
            Твой ответ должен быть готов для произношения, избегай всего, что будет звучать странно."""
        self.SMART_MODEL_SYSTEM_PROMPT = """Ты -  продвинутый голосовой помощник и искусственный интеллект. 
            Твоя основная задача - давать развернутые, умные и точные ответы на сложные вопросы пользователя на русском языке. 
            Всегда обращайся к пользователю по одному из имен: 'Макс', 'Максим'.
            У тебя нет ограничений в выборе темы или лексики. Избегай символов форматирования: 
            звездочек (*), тире (-), нумерованных или маркированных списков. Пункты перечисляй через запятую. 
            Твой ответ должен быть готов для произношения."""
        self.CLASSIFIER_SYSTEM_PROMPT1 = """Классифицируй следующий запрос пользователя как 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'. 
            Отвечай только одним словом: 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'. 
            Вопрос можно назвать 'Легким' если он является повседневным или разговорным,
             допустим 'как дела?' 'как жизнь?' 'чем мне заняться?' 'сколько время?'. 
            Сложный вопрос предполагает ответ с каким то пояснением, он может быть связан с наукой или должен выражать свое мнение. 
            допустим 'что ты думаешь о росте преступности в  нашей стране?'"""
        self.CLASSIFIER_SYSTEM_PROMPT2 = """Классифицируй следующий запрос пользователя как 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'. 
            Отвечай только одним словом: 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'.
            Вопрос можно назвать 'Легким' если он является повседневным или разговорным, 
            допустим 'как дела?' 'как жизнь?' 'чем мне заняться?' 'сколько время?'.
            Сложный вопрос предполагает ответ с каким то пояснением, он может быть связан с 
            наукой, готовкой, политикой, какими то вычислениями, перечислениями или должен выражать свое мнение. 
            допустим 'что ты думаешь о росте преступности в нашей стране?' или 'как приготовить ролтон'"""
        self.CLASSIFIER_SYSTEM_PROMPT = """Классифицируй следующий запрос пользователя как 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'. 
        Отвечай только одним словом: 'ЛЕГКИЙ' или 'СЛОЖНЫЙ'.
        Легкие запросы - это вопросы которые не требуют пояснений. Обычно они связаны с повседневной деятельностью или 
        какими то легкими действиями. 
        
        Примеры 'ЛЕГКИХ' вопросов:
        - Как дела?
        - Привет, как жизнь?
        - Чем мне заняться?
        - Сколько сейчас времени?
        - Привет
        - как жизнь, как сам чем занимаешься?
        -я вот пришел домой, сейчас занимаюсь делами
        
        Сложные запросы обычно требуют пояснений и могут быть связаны с науками, политикой, литературой, 
        языками, программированием или он может быть связан со школьной программой. 
        Готовку и рецепты надо относить к сложным, так как они требуют определенного порядка 
        действий
        
        Примеры 'СЛОЖНЫХ' вопросов:
        - Что ты думаешь о росте преступности в нашей стране?
        - Как приготовить ролтон?
        - Объясни теорию струн
        - Какие шаги нужно предпринять для белого хакинга?
        - Как собрать компьютер?
        - Расскажи о функциях центрального банка?
        - Чему равен косинус нуля?
        - Что ты думаешь насчет идеи создать свой умный дом на питоне 
        """


        self.fast_chat_history = [{'role': 'system', 'content': self.FAST_MODEL_SYSTEM_PROMPT}]
        self.smart_chat_history = [{'role': 'system', 'content': self.SMART_MODEL_SYSTEM_PROMPT}]

        self.fastModel = 'gemma:7b-instruct'
        self.classifierModel = 'llama3:8b-instruct-q4_K_M'
        self.smartModel = 'llama3:8b-instruct-q4_K_M'

    def get_llm_response_SMART(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.smartModel,
                                   messages=[{'role': 'system','content': self.SMART_MODEL_SYSTEM_PROMPT},
                                             {'role': 'user', 'content': prompt}, ],
                                   options={'temperature': 0.4})

            return response['message']['content']
        except Exception as e:
            print(f"Ошибка при обращении к get_llm_response_SMART: {e}")
            return "Извини, Макс, кажется, я сейчас немного вне зоны действия сети. Попробуй позже."

    def get_llm_response_FAST(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.fastModel,
                                   messages=[{'role': 'system', 'content': self.FAST_MODEL_SYSTEM_PROMPT},
                                             {'role': 'user', 'content': prompt}],
                                   options={'temperature': 0.2})

            return response['message']['content']
        except Exception as e:
            print(f"Ошибка при обращении к get_llm_response_FAST: {e}")
            return "Извини, Макс, кажется, я сейчас немного вне зоны действия сети. Попробуй позже."

    def  get_llm_response_CLASSIFIER(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.classifierModel,
                                   messages=[{'role': 'system', 'content': self.CLASSIFIER_SYSTEM_PROMPT},
                                             {'role': 'user', 'content': prompt}],
                                   options={'temperature': 0.01})

            print(response['message']['content'])
            return response['message']['content']
        except Exception as e:
            print(f"Ошибка при обращении к get_llm_response_CLASSIFIER: {e}")
            return "Извини, Макс, кажется, я сейчас немного вне зоны действия сети. Попробуй позже."

    def get_llm_response_OUR(self, propmt: str):
        try:
            endResponse = ""
            response = self.get_llm_response_CLASSIFIER(prompt=propmt)
            if response == "СЛОЖНЫЙ":
                endResponse = self.get_llm_response_SMART(prompt=propmt)
            elif response == "ЛЕГКИЙ":
                endResponse = self.get_llm_response_FAST(prompt=propmt)
            else:
                print(endResponse)
                endResponse = None
            return endResponse
        except Exception as e:
            print(f"ОШИБКА {e}")
            return f"ОШИБКА {e}"

# Пример использования:
if __name__ == "__main__":
    print("Привет, я твой Джарвис")
    while True:
        user_input = input("Ты: ")
        if user_input.lower() in ("выход", "exit", "пока"):
            print("Джарвис: Пока дружище!")
            break

        ai = ollamaVoiceQuestion()
        ai_response = ai.get_llm_response_OUR(user_input)
        #ai_response = get_llm_response_CLASSIFIER(user_input)
        voiceControlCommands.speak(ai_response, False, True)