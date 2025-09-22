if __name__ == "__main__":
    stop = input()
    print("Подключение")

    parametrs = {
        "red": {'D5': 0, 'D6': 1, 'D7': 0},
        "blue": {'D5': 0, 'D6': 0, 'D7': 1},
        "green": {'D5': 1, 'D6': 0, 'D7': 0},
        "white": {'D5': 1, 'D6': 1, 'D7': 1},
        "black": {'D5': 0, 'D6': 0, 'D7': 0}
    }
    server = f"http://192.168.0.118/light"
    requets = HTTPService(url=server, parametrs=parametrs)
    print("Подключено")

    for i in range(100):
        color = input("Введите цвет (на английском): ")
        color = color.lower()
        requets = HTTPService(url=server, parametrs=parametrs[color])
        requets.send()