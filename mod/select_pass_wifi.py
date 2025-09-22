import os
import winreg
#import pywin32
import ctypes
#import pywin32
import pywifi
from pywifi import const
from itertools import permutations, product
import threading
from time import time, sleep
import queue




nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = [
    'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e',
    'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
    'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o',
    'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
    'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y',
    'Z', 'z'
]
special_characters = [
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\',
    ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
]

mass = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e',
    'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
    'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o',
    'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
    'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y',
    'Z', 'z'
]
mass_s2 = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e',
    'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
    'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o',
    'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
    'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y',
    'Z', 'z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\',
    ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
]


attempts = 0
password = '14882285242'
project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом
def selection_password(length):
    def password1(result_queue, stop_event, length):
        global password, project_dir

        print('поток 1 запущен\n')
        mass_s = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e',
            'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
            'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o',
            'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
            'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y',
            'Z', 'z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
            '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\',
            ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
        ]
        attempts = 0
        start = time()
        for combo in product(mass_s, repeat=length):
            attempts += 1
            current_password = ''.join(combo)  # Создаем строку из кортежа
            #print('поток 1', current_password)
            if current_password == password:  # Сравниваем строку с паролем
                end = time()
                print(f'поток 1:Пароль найден: {current_password} за {attempts} попыток и {end - start} секунд')
                result_queue.put(current_password)  # Помещаем результат в очередь
                stop_event.set()  # Сигнализируем о завершении работы
                return current_password
                exit(0)  # Останавливаем цикл, если пароль найден

    def password2(result_queue, stop_event, length):
        global password

        print('поток 2 запущен\n')
        mass_s = [
            'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e',
            'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
            'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o',
            'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
            'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y',
            'Z', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
            '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\',
            ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
        ]
        attempts = 0
        start = time()
        for combo in product(mass_s, repeat=length):
            attempts += 1
            current_password = ''.join(combo)  # Создаем строку из кортежа
            # print(current_password)
            if current_password == password:  # Сравниваем строку с паролем
                end = time()
                print(f'поток 2: Пароль найден: {current_password} за {attempts} попыток и {end - start} секунд')
                result_queue.put(current_password)  # Помещаем результат в очередь
                stop_event.set()  # Сигнализируем о завершении работы
                return current_password
                exit(2)  # Останавливаем цикл, если пароль найден

    def password3(result_queue, stop_event, length):
        global password

        print('поток 3 запущен\n')
        mass_s = [
            'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd',
            'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b',
            'v', 'k', 'j', 'x', 'q', 'z', '1', '2', '3', '4',
            '5', '6', '7', '8', '9', '0', 'E', 'T', 'A', 'O',
            'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M',
            'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X',
            'Q', 'Z', '!', '@', '#', '$', '%', '^', '&', '*',
            '(', ')', '-', '_', '=', '+', '{', '}', '[', ']',
            '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.',
            '?', '/'

        ]
        attempts = 0
        start = time()
        for combo in product(mass_s, repeat=length):
            attempts += 1
            current_password = ''.join(combo)  # Создаем строку из кортежа
            # print(current_password)
            if current_password == password:  # Сравниваем строку с паролем
                end = time()
                print(f'поток 3: Пароль найден: {current_password} за {attempts} попыток и {end - start} секунд')
                result_queue.put(current_password)  # Помещаем результат в очередь
                stop_event.set()  # Сигнализируем о завершении работы
                return current_password
                exit(3)  # Останавливаем цикл, если пароль найден

    def password4(result_queue, stop_event, length):
        global password

        print('поток 4 запущен\n')
        mass_s = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '!', '@', '#', '$', '%', '_', '-', '*', '&'
        ]
        attempts = 0
        start = time()
        for combo in product(mass_s, repeat=length):
            attempts += 1
            current_password = ''.join(combo)  # Создаем строку из кортежа
            # print(current_password)
            if current_password == password:  # Сравниваем строку с паролем
                end = time()
                print(f'поток 4: Пароль найден: {current_password} за {attempts} попыток и {end - start} секунд')
                result_queue.put(current_password)  # Помещаем результат в очередь
                stop_event.set()  # Сигнализируем о завершении работы
                return current_password
                exit(4)  # Останавливаем цикл, если пароль найден

    def password_populares(result_queue, stop_event):
        # Загрузка паролей из файла
        with open(f'{project_dir}\\.txt\\WiFi_passwords.txt', 'r', encoding='utf-8') as file:
            mass_pass = [line.strip() for line in file]  # Читаем все строки и убираем \n

        attempts = 0
        start = time()

        for combo in mass_pass:
            attempts += 1
            current_password = combo

            if current_password == password:
                end = time()
                print(f'База : Пароль найден: {current_password} за {attempts} попыток и {end - start} секунд')
                result_queue.put(current_password)
                stop_event.set()
                return current_password

        # Если пароль не найден
        print("Пароль не найден в списке.")
        with open(f'{project_dir}\\.txt\\WiFi_passwords.txt', 'a', encoding='utf-8') as file:
            file.write(f'\n{password}')
        return None

    # Создаем очередь для хранения результата
    result_queue = queue.Queue()
    stop_event = threading.Event()

    thread1 = threading.Thread(target=password1, args=(result_queue, stop_event, length))
    thread1.daemon = True
    thread2 = threading.Thread(target=password2, args=(result_queue, stop_event, length))
    thread2.daemon = True
    thread3 = threading.Thread(target=password3, args=(result_queue, stop_event, length))
    thread3.daemon = True
    thread4 = threading.Thread(target=password4, args=(result_queue, stop_event, length))
    thread4.daemon = True
    password_popular = threading.Thread(target=password_populares, args=(result_queue, stop_event))
    password_popular.daemon = True

    #if __name__ == "__main__":
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    password_popular.start()


    stop_event.wait()  # Блокируем основной поток до тех пор, пока не будет установлен флаг

    if not result_queue.empty():
        result = result_queue.get()  # Получаем результат из очереди
        print("Получен результат:", result)

    while True:
        if (thread1.is_alive()) and (thread2.is_alive()) and (thread3.is_alive()) and (thread4.is_alive()) and (password_popular.is_alive()):
            time.sleep(1)  # Ждем 1 секунду перед следующей проверкой
        else:
            print("Потоки завершены.")
            break
    exit(0)


sel_password = selection_password(8)
#print(sel_password)


















