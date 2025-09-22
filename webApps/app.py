#app.py
import keyboard
from http.cookiejar import debug
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
#from flask_cors import CORS
import threading
import time
from bs4 import BeautifulSoup  # Для парсинга nmap
import subprocess
import json
import platform
from ourClass.ClassFunctionsOS import Windows_system, Commands
import os
import re
import PIL
import webbrowser
from datetime import datetime
import logging
from tqdm import tqdm
import pyautogui  # Для эмуляции нажатий
import sys


    # ПУТИ
project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом
script_path = r'C:\Users\User\PythonProject3\.venv\start_voicecontrol.bat'
discord = 'C:\\Users\\User\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe'
discord_fix = 'C:\\Users\\User\\Desktop\\DiscordFix_6.0.3426\\pre-configs\\general (ALT2).bat'

    # .txt ФАЙЛЫ
WebLogs ='.txt/Web/WebLogs.txt'
Story = '.txt/Web/Story.txt'
path_to_pass = '../.txt/Web/pass.txt'

    # ФУНКЦИИ
def get_client_mac(ip):
    try:
        if platform.system() == "Windows":
            cmd = f"arp -a {ip}"
            output = subprocess.check_output(cmd, shell=True).decode('cp866')  # Важно: кодировка cp866!
            for line in output.split('\n'):
                if ip in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]
        else:  # Linux/Mac
            cmd = f"arp -n {ip}"
            output = subprocess.check_output(cmd, shell=True).decode()
            if "ether" in output.lower():
                return output.split()[2]
    except Exception as e:
        print(f"Ошибка получения MAC: {e}")
    return "Unknown"

def get_geolocation(ip):
    if ip.startswith(('192.168.', '10.')):
        return {"country": "Local", "city": "Local", "isp": "Local"}
    try:
        response = requests.get(API_IPGEOLOCATION.format(ip), timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    "country": data.get('country', 'Unknown'),
                    "city": data.get('city', 'Unknown'),
                    "isp": data.get('isp', 'Unknown')
                }
    except:
        pass
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}


def scan_network():
    """Сканирование локальной сети с помощью nmap"""
    try:
        if platform.system() == "Windows":
            cmd = "nmap -sn 192.168.1.0/24"  # Подставь свою подсеть!
        else:
            cmd = "nmap -sn 192.168.1.0/24 | grep -E 'Nmap scan|MAC'"

        result = subprocess.check_output(cmd, shell=True).decode()
        devices = []

        if platform.system() == "Windows":
            # Парсим вывод nmap для Windows
            lines = result.split('\n')
            for line in lines:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip('()')
                    devices.append({"ip": ip, "mac": "Unknown"})
        else:
            # Парсим вывод nmap для Linux/Mac
            soup = BeautifulSoup(result, 'html.parser')
            for host in soup.find_all('host'):
                ip = host.address.get('addr')
                mac = host.find('address', {'addrtype': 'mac'})
                devices.append({
                    "ip": ip,
                    "mac": mac.get('addr') if mac else "Unknown"
                })
        return devices
    except Exception as e:
        print("Ошибка сканирования:", e)
        return []


    # ПЕРЕМЕННЫЕ
port = 5000
host = '0.0.0.0'
pet = False
OpenSurs = False
PASSWORD = Windows_system._read(path_to_pass)
AdminMode = False
num_AdminMode = 0
dateTime = datetime.now()
loginfo = None
web = False


app = Flask(__name__)
app.secret_key = 'i_like_gey_pron'  # Замените на свой секретный ключ
app.config['SESSION_TYPE'] = 'filesystem'
# Отключаем защиту для быстрого тестирования (в продакшене нужно настроить правильно)
#app.config['CORS_HEADERS'] = 'Content-Type'
Session(app)
#CORS(app)

os.system(f'start {project_dir}\\.bat\\stop_all.bat')



    # КОМАНДЫ
class CommandsWeb(Commands):

    def start_cat(pet):
        if pet == False:
            os.system(f'start {project_dir}\\.bat\\Pet1_cat.bat')
            output = "запуск питомца..."
            pet = True
        elif pet == True:
            os.system(f'start {project_dir}\\.bat\\stop_all.bat')
            output = "запуск питомца..."
            time.sleep(3)
            os.system(f'start {project_dir}\\.bat\\Pet1_cat.bat')
            pet = True

    def fulfillCommandsWeb(command, route, device_info):
        global pet, OpenSurs, PASSWORD, num_AdminMode, AdminMode, WebLogs, Story, dateTime, loginfo
        output = ''
        loginfo = None
        dateTime = datetime.now()

        commands = {
            '/com1': Commands.com1,
            f'/off_computer:{PASSWORD}': lambda: Commands.PCoff(AdminMode=AdminMode, numAdminMode=num_AdminMode),
            '/clear': Commands.clear,
            "/open_chrome": Commands.start_google,
            '/win_min': Windows_system.minimize_active_window,
            '/win_close': Windows_system.close_active_window,
            '/al': Windows_system._alt_tab,
            '/wind': Windows_system._alt_tab,
            '/pause': Windows_system._pause,
            '/screen': Windows_system.screen,
            '/sc': Windows_system.screen,
            "/open_opera": Commands.start_opera,
            "/new_local_console": Commands.new_local_console,
            '/new_open_comsole': Commands.new_open_comsole,
            "/start_voice_control": Commands.start_voice_control,
            "/check_windows": Windows_system.get_windows_info,
            '/cw': Windows_system.get_windows_info,
            '/logout': lambda: session.pop('logged_in', None),
            '/clear_session': session.clear,
            '/up': Commands.up_v,
            '/+': Commands.up_v,
            '/dw': Commands.down_v,
            '/-': Commands.down_v,
            '/mute': Commands.mute,
            '//': Commands.mute,
            "/stop_all": lambda: Commands.stop_all(pet=pet),
            "/start_cat": lambda:CommandsWeb.start_cat(pet=pet),
            '/cmd': Commands.CMD
        }
        if command in commands:
            return commands[command]()

        elif (command == f"/dev_true_pass_{PASSWORD}"):
                OpenSurs = True
                output = "режим разработчика активирован"

        elif (command == f"/dev_falce_pass_{PASSWORD}"):
            OpenSurs = False
            output = "режим разработчика выключен"

        elif ('/change_pass_' in command):
            match = re.search(r"/change_pass_(.+)", command.lower())  # Ищем текст "Найди в гугле" далее любой текст (.+)
            if match:
                query = match.group(1)  # Извлекаем запрос из текста
                PASSWORD = Windows_system._write(query, path_to_pass)
                output = f'пароль изменен на {PASSWORD}'

        elif ('/win_close_' in command):
            match = re.search(r"/win_close_(.+)", command.lower())
            if match:
                wind = match.group(1)  # Извлекаем запрос из текста
            Windows_system.close_windows(wind)

        elif ('/set_a_requests_' in command):
            if OpenSurs == True:
                OpenSurs = False
                AdminMode = True
                match = re.search(r"/set_a_requests_(.+)", command.lower())
                if match:
                    ms = match.group(1)  # Извлекаем запрос из текста
                    if (int(ms) < 100):
                        loginfo = f'num_AdminMode = {num_AdminMode} --> num_AdminMode = {int(ms)} '
                        num_AdminMode = int(ms)
                        output = f'вы приобрели {ms} запросов админа, режим разработчика выключен'
                    else:
                        output = 'слишком много админских запросов\n сосите бимбу'

            else:
                output = 'вы не включили режим разработчика'


        elif ("/set_black_win_" in command):
            match = re.search(r"/set_black_win_(.+)",command.lower())
            if match:
                ms = match.group(1)  # Извлекаем запрос из текста
                s = ms * 1000
                Windows_system.prank_winLock(ms, 'black')

        elif ("/set_white_win_" in command):
            match = re.search(r"/set_white_win_(.+)",command.lower())
            if match:
                ms = match.group(1)  # Извлекаем запрос из текста
                s = ms * 1000
                Windows_system.prank_winLock(ms, 'white')

        elif ("/set_blue_win_" in command):
            match = re.search(r"/set_blue_win_(.+)",command.lower())
            if match:
                ms = match.group(1)  # Извлекаем запрос из текста
                s = ms * 1000
                Windows_system.prank_winLock(ms, 'blue')

        elif ("/set_red_win_" in command):
            match = re.search(r"/set_red_win_(.+)",command.lower())
            if match:
                ms = match.group(1)  # Извлекаем запрос из текста
                s = ms * 1000
                Windows_system.prank_winLock(ms, 'red')

        elif ("/set_violet_win_" in command):
            match = re.search(r"/set_violet_win_(.+)", command.lower())
            if match:
                ms = match.group(1)  # Извлекаем запрос из текста
                s = ms * 1000
                Windows_system.prank_winLock(ms, 'violet')


        else:
            if num_AdminMode <= 0:
                AdminMode = False

            if AdminMode == True:
                if num_AdminMode > 0:
                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                        output = result.stdout + '\n' + result.stderr
                        num_AdminMode -= 1
                        loginfo = f'num_AdminMode ({num_AdminMode})- 1; num_AdminMode = {num_AdminMode}'
                    except Exception as e:
                                output = str(e)
            else:
                output = f"команда {command} не найдена"
            if output == " " or output == "" or output == '' or output == '' or output == None:
                output = ''

            else:
                output = '>> ' + output
        if num_AdminMode < 1:
            num_AdminMode = 0
        loginfo = f'{loginfo}; pet = {pet}, OpenSurs = {OpenSurs}, password = {PASSWORD}, num_AdminMode = {num_AdminMode}, AdminMode = {AdminMode}'
        with open(Story, 'a') as story:
            story.write(f'\n--[INPUT]--[{dateTime}]--[{device_info}]--{route}--INPUT:"{command}"')
            story.write(f'\n--[LOGS]--[{dateTime}]--[{device_info}]--{route}--LOGS:"{loginfo}"')
            story.write(f'\n--[OUTPUT]--[{dateTime}]--[{device_info}]--{route}--OUTPUT:"{output}"\n')

        return(output)


    # КОД САЙТА
class WebSerwis:

        # ПАРОЛЬ\ЛОГИН
    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        session.pop('logged_in', None)
        if request.method == 'POST':
            password = request.form['password']
            if password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template('access_denied.html')
        return render_template('pass.html')

        #
    @staticmethod
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('home'))

        # КОНСОЛЬ
    @staticmethod
    @app.route("/my_console", methods=['GET', 'POST'])
    def my_console():
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0].strip()
        ua = request.user_agent
        device_type = "Mobile" if ua and any(
            x in ua.platform.lower() for x in ['android', 'iphone', 'ios']) else "Desktop"
        geo = get_geolocation(client_ip)

        device_info = {
            "ip": client_ip,
            "mac": get_client_mac(client_ip),
            "browser": getattr(ua, 'browser', 'Unknown'),
            "os": getattr(ua, 'platform', 'Unknown'),
            "device": device_type,
            "user_agent": str(ua),
            "country": geo.get('country', 'Unknown') if geo else 'Unknown',
            "city": geo.get('city', 'Unknown') if geo else 'Unknown',
            "isp": geo.get('isp', 'Unknown') if geo else 'Unknown',
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if 'logged_in' in session:
            output = ""
            if request.method == 'POST':
                command = request.form.get('command')
                output = CommandsWeb.fulfillCommandsWeb(command, '/my_console', device_info)
            return render_template('console.html', output=output)
        else:
            return redirect(url_for('login'))

        # ДОМАШНЯЯ СТРАНИЦА (ФУНКЦИИ + НАСТРОЙКИ + КНОПКИ ПЕРЕХОДОВ)
    @staticmethod
    @app.route("/")
    def home():
        if 'logged_in' in session:
            return render_template('home.html')
        else:
            return redirect(url_for('login'))

      # ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ, ОБЩАЯ ИНФОРМАЦИЯ
    @staticmethod
    @app.route("/profile")
    def profile():
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0].strip()
        ua = request.user_agent
        device_type = "Mobile" if ua and any(
            x in ua.platform.lower() for x in ['android', 'iphone', 'ios']) else "Desktop"
        geo = get_geolocation(client_ip)

        device_info = {
            "ip": client_ip,
            "mac": get_client_mac(client_ip),
            "browser": getattr(ua, 'browser', 'Unknown'),
            "os": getattr(ua, 'platform', 'Unknown'),
            "device": device_type,
            "user_agent": str(ua),
            "country": geo.get('country', 'Unknown') if geo else 'Unknown',
            "city": geo.get('city', 'Unknown') if geo else 'Unknown',
            "isp": geo.get('isp', 'Unknown') if geo else 'Unknown',
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if 'logged_in' in session:
            return render_template('profile.html')
        else:
            return redirect(url_for('login'))

        # ДОКУМЕНТАЦИЯ ПРОЕКТА (КОМАНДЫ + МОД + CMD)
    @staticmethod
    @app.route('/doc')
    def doc():
        if 'logged_in' in session:
            return render_template('doc_home.html')
        else:
            return redirect(url_for('login'))

        # ТАЧПАД ДЛЯ УПРАВЛЕНИЯ КУРСОРОМ МЫШИ КОМПЬЮТЕРА С ТЕЛЕФОНА
    @staticmethod
    @app.route('/touchpad')
    def touchpad():
        return 'This is touchpad'

        # УДАЛЕННАЯ КЛАВИАТУРА КОМПЬЮТЕРА
    @staticmethod
    @app.route('/keyboard', methods=['POST'])
    def keyboard():
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data'}), 400
        
        key_code = data.get('key')
        action = data.get('action', 'press')
        
        if not key_code:
            return jsonify({'status': 'error', 'message': 'Key code is required'}), 400
        
        key_name = KEY_MAP.get(key_code, key_code.lower().replace('key', ''))
        
        try:
            if action == 'press':
                pyautogui.keyDown(key_name)
            elif action == 'release':
                pyautogui.keyUp(key_name)
            else:
                pyautogui.press(key_name)
            
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
            

        # НАСТРОЙКИ МОДА
    @staticmethod
    @app.route('/settings')
    def settings():
        return "This is settings for this project"

    # sgfgdfgdg



        # ЗАПУСК КОДА
    @staticmethod
    def run_app():
        global host
        app.run(host=host, port=port, debug=True, use_reloader=False)  # use_reloader = False обязательно!
        print("Flask app завершил работу.")



if __name__ == "__main__":

    try:
        WebSerwis.run_app()
    except KeyboardInterrupt:
        print("Ошибка")




