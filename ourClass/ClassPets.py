import tkinter as tk
from sympy.physics.units import speed
from tkinter import *
from tkinter import ttk
import os
import random

class Pets:
    def __init__(self, width, height, x_position, y_position, animations, chances, speed):
        # ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ
        self.width = width  # размер питомца
        self.height = height  # размер питомца
        self.x_position = x_position  # где он находится
        self.y_position = y_position  # где он находится

        # НЕИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ
        self.win1 = tk.Tk()
        self.win1.title('pet')
        self.win1.overrideredirect(True)  # убрать рамку окна
        self.win1.attributes('-transparentcolor', 'white')
        self.win1.geometry(f"{self.width}x{self.height}+{self.x_position}+{self.y_position}")
        self.win1.resizable(False, False)  # запрет изменять размер окна
        self.win1.attributes('-topmost', True)  # поверх всех окон
        self.win1.configure(bg='white')

        # ПАРАМЕТРЫ АНИМАЦИИ
        self.label = tk.Label(self.win1, bg='white')
        self.animations = animations
        self.animation_names = list(animations.keys())  # Получаем список названий анимаций из ключей словаря
        self.chances = chances  # Список шансов для каждой анимации
        self.current_animation_index = random.choices(range(len(self.animation_names)), weights=self.chances)[0]  # Случайная начальная анимация с учетом шансов
        self.this_animation = self.animation_names[self.current_animation_index]  # Устанавливаем первую анимацию
        self.frames = self.animations[self.this_animation]  # Получаем список кадров для текущей анимации
        self.index_frame = 0
        self.speed = speed

    def animation(self):
        # Загружаем текущее изображение
        path = self.frames[self.index_frame]
        self.photo = PhotoImage(file=path)
        self.label.config(image=self.photo)

        # Обновляем индекс кадра
        self.index_frame = (self.index_frame + 1) % len(self.frames)

        # Проверяем, нужно ли переключиться на следующую анимацию
        if self.index_frame == 0:  # Если мы вернулись к первому кадру
            # Выбираем новую анимацию на основе шансов
            self.current_animation_index = random.choices(range(len(self.animation_names)), weights=self.chances)[0]
            self.this_animation = self.animation_names[self.current_animation_index]  # Обновляем текущую анимацию
            self.frames = self.animations[self.this_animation]  # Получаем новые кадры
            self.index_frame = 0  # Сброс индекса при смене анимации

        self.label.after(self.speed, self.animation)  # Планируем следующий кадр

    def start(self):
        self.label.pack()
        self.animation()
        self.win1.mainloop()

if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом

    animations = {
        "normal": [f'./photos/cat/frame1/sprite_{i}.png' for i in range(1, 16)], # +1 к индексу последней фотки
        "happy": [f'./photos/cat/frame2/sprite_{i}.png' for i in range(1, 14)],
        "sad": [f'./photos/cat/frame3/sprite_{i}.png' for i in range(1, 3)]
    }



    # Шансы для каждой анимации (сумма должна быть 100)
    chances = [50, 49, 1]  # 50% для "normal", 30% для "happy", 15% для "sad", 5% для "angry"

    #cat = Pets(115, 105, 170, 95, animations, chances, 150)
    #cat.start()
