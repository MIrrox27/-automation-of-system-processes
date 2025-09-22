from ourClass.ClassFunctionsOS import Commands
import requests
import time

class HTTPService(Commands):
    def __init__(self, url):
        self.url = url
        self.colorParametrs = {
        "red": {'D5': 0, 'D6': 1, 'D7': 0}, # D5 - зеленый, D6 - красный, D7 - синий
        "blue": {'D5': 0, 'D6': 0, 'D7': 1},
        "green": {'D5': 1, 'D6': 0, 'D7': 0},
        "white": {'D5': 1, 'D6': 1, 'D7': 1},
        "black": {'D5': 0, 'D6': 0, 'D7': 0},
        "off": {'D5': 0, 'D6': 0, 'D7': 0},
        "violet": {'D5': 0, 'D6': 1, 'D7': 1},
        "turquoise": {'D5': 1, 'D6': 0, 'D7': 1},
        "yellow": {'D5': 1, 'D6': 1, 'D7': 0}

        }
        self.response = requests.get(self.url, {'message': "Connected"})

    def send(self, parametrs):
        self.response = requests.get(self.url, parametrs)
        if self.response.status_code == 200:
            return print('Ответ от сервера:', self.response.text)
        else:
            return print('Ошибка:', self.response.status_code)

    def set_color(self, color):
        if color in self.colorParametrs:
            self.send(self.colorParametrs[color])
        else:
            print('Ошибка: Неверный цвет')



if __name__ == "__main__":
    server = f"http://192.168.0.120/light"
    requets = HTTPService(url=server)
    while True:
        color = input()
        requets.set_color(color)



