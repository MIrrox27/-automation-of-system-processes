import keyboard #pip install keyboard
from ourClass.FunctionsOS import Windows_system, Commands

keyboard.add_hotkey("alt+q", lambda:Windows_system.minimize_active_window())
keyboard.add_hotkey("tab+c+h", lambda:Commands.start_google())
keyboard.add_hotkey("tab+!", lambda:Commands.CMD())
#keyboard.add_hotkey('tab+@', )
keyboard.add_hotkey('capslock+!', lambda:print(1))

input()
