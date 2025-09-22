# FunctionOS.py
import os
import tkinter as tk
from pywinauto import application
from pywinauto import Application, Desktop
import time
import webbrowser
import win32gui
import ctypes
import pygetwindow as gw
import pyautogui
import base64
import hashlib
from cryptography.fernet import Fernet
import keyboard


social_media = ["ВКонтакте", "вконтакте", "youtube", "YouTube", "TikTok", "Telegram", "x.com", "Google"]
desk_wins = []
title = None
custom_key = "17F75Bj45C28aB3EDE8dE7f3A9Fj044"
key = base64.urlsafe_b64encode(hashlib.sha256(custom_key.encode()).digest())
#cipher = Fernet(key)
project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом
class Windows_system:
    @staticmethod
    def get_windows_info():
        global project_dir
        desk_win = Desktop(backend="uia").windows()
        num = 0
        global desk_wins
        desk_wins.clear()
        for window in desk_win:
            num += 1
            desk_wins.append(window.window_text())
            print(num, ") ", window.window_text())
            #return (num, ") ", window.window_text())
        return num, [window.window_text() for window in desk_win]

    @staticmethod
    def close_SM():
        desk_wins = Windows_system.get_windows_info()
        for win_title in desk_wins:
            for sm in social_media:
                if sm.lower() in win_title.lower():
                    try:
                        app = pywinauto.Application().connect(title=win_title)
                        app.close()
                        print(f"Закрыто окно: {win_title}")
                    except pywinauto.findwindows.ElementNotFoundError:
                        print(f"Не удалось закрыть окно: {win_title}")
                    break

    # Получаем дескриптор активного окна
    @staticmethod
    def get_active_window():
        hwnd = ctypes.windll.user32.GetForegroundWindow()  # Получаем дескриптор активного окна
        return hwnd

    # Получаем заголовок окна по дескриптору
    @staticmethod
    def get_window_title(hwnd):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        title = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
        return title.value

    # Свернуть активное окно
    @staticmethod
    def minimize_active_window():
        hwnd = Windows_system.get_active_window()
        if hwnd:
            title = Windows_system.get_window_title(hwnd)
            window = gw.getWindowsWithTitle(title)
            if window:
                window[0].minimize()  # Скрываем (сворачиваем) окно
                print(f"Окно '{window[0].title}' успешно скрыто.")
                return f"Окно '{window[0].title}' успешно скрыто."
            else:
                print("Активное окно не найдено.")
                return "Активное окно не найдено."
        else:
            print("Не удалось получить активное окно.")
            return "Не удалось получить активное окно."

    # Закрыть активное окно
    @staticmethod
    def close_active_window():
        hwnd = Windows_system.get_active_window()
        if hwnd:
            title = Windows_system.get_window_title(hwnd)
            window = gw.getWindowsWithTitle(title)
            if window:
                # Используем pyautogui для закрытия окна
                pyautogui.hotkey('alt', 'f4')  # Отправляем комбинацию Alt+F4 для закрытия окна
                print(f"Окно '{window[0].title}' успешно закрыто.")
                return f"Окно '{window[0].title}' успешно скрыто."
            else:
                print("Активное окно не найдено.")
                return "Активное окно не найдено."
        else:
            print("Не удалось получить активное окно.")
            return "Не удалось получить активное окно."

    @staticmethod
    def _pause():
        pyautogui.press('space')

    @staticmethod
    def _alt_tab():
        #pyautogui.hotkey('alt', 'tab')
        keyboard.press_and_release('alt+tab')

    @staticmethod
    def _ctrl_z():
        pyautogui.hotkey('ctrl', 'z')

    @staticmethod
    def off_computer(num):
        for i in range(num):
            #pyautogui.hotkey('alt', 'tab')
            keyboard.press_and_release('alt+tab')
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)

    @staticmethod
    def close_windows(num):
        for i in range(num):
            #pyautogui.hotkey('alt', 'tab')
            keyboard.press_and_release('alt+tab')
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(1)

    @staticmethod
    def screen():
        pyautogui.hotkey('win', 'printscreen')

    @staticmethod
    def prank_winLock(ms, color):
        win = tk.Tk()
        #win.deiconify()
        win.geometry('2800x2800')
        win.overrideredirect(True)  # убрать рамку окна
        win.resizable(False, False)  # запрет изменять размер окна
        win.attributes('-topmost', True)  # поверх всех окон
        win.configure(bg=color)
        win.after(ms, win.destroy)
        win.mainloop()
        #win.withdraw()

    @staticmethod
    def _write(info, path_to_file):
        with open(path_to_file, 'a', encoding="utf-8") as file:
            file.write(info)
            return info

    @staticmethod
    def _read(path_to_file):
        with open(path_to_file, 'r', encoding="utf-8") as file:
            info = file.readline()
        return info

    @staticmethod
    def start_diskord(path_to_fix, path_to_app):
        os.system(f'start {path_to_fix}')
        pyautogui.FAILSAFE = False
        time.sleep(2)
        pyautogui.press('tab', presses=2)
        pyautogui.press('enter')
        time.sleep(6)
        os.system(f'start {path_to_app}')





class Commands(Windows_system):
    @staticmethod
    def ht_1():
        webbrowser.open('http://127.0.0.1:5000')
    @staticmethod
    def ht_2():
        print('ты нажал на кнопку')

    @staticmethod
    def ht_3():
        Windows_system.get_windows_info()

    @staticmethod
    def start_google():
        os.system("start Chrome")

    @staticmethod
    def start_opera():
        os.system("start Opera Air")

    @staticmethod
    def open_folder(path):
        os.system(f'start {path}')

    @staticmethod
    def PCoff(AdminMode, numAdminMode):
        if AdminMode == True and numAdminMode > 1000:
            os.system("shutdown /s /t 1") # выключить комп

    @staticmethod
    def CMD():
        os.system('start CMD')

    @staticmethod
    def com1():
        return 'команда выполнена'

    @staticmethod
    def clear():
        return ''

    @staticmethod
    def new_local_console():
        webbrowser.open("http://127.0.0.1:5000/my_console")

    @staticmethod
    def new_open_comsole():
        webbrowser.open("http://192.168.0.106:5000/my_console")

    @staticmethod
    def start_voice_control():
        os.system(f'start {project_dir}\\.bat\\voice_control.bat')
        output = "запуск голосового управления..."
        return output

    @staticmethod
    def up_v():
        keyboard.send("volume up")

    @staticmethod
    def down_v():
        keyboard.send("volume down")

    @staticmethod
    def mute():
        keyboard.send("volume mute")

    @staticmethod
    def stop_all(pet):
        os.system(f'start {project_dir}\\.bat\\stop_all.bat')
        output = "остановка питомца..."
        pet = False
        return output




if __name__ == "__main__": # это для отдельной проверки
    print("open")
    #Windows_system.start_diskord('C:\\Users\\User\\Desktop\\DiscordFix_6.0.3426\\pre-configs\\general (ALT2).bat','C:\\Users\\User\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe')
    keyboard.add_hotkey("*+-", lambda: keyboard.send("volume up"))





















