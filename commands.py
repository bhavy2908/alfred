import pyautogui
import subprocess
import os
import time

# Disable pyautogui's fail-safe feature
pyautogui.FAILSAFE = False

def move_cursor(direction, distance=50):
    if direction == "up":
        pyautogui.moveRel(0, -distance)
    elif direction == "down":
        pyautogui.moveRel(0, distance)
    elif direction == "left":
        pyautogui.moveRel(-distance, 0)
    elif direction == "right":
        pyautogui.moveRel(distance, 0)

def click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def double_click():
    pyautogui.doubleClick()

def type_text(text):
    pyautogui.typewrite(text)

def press(arg):
    pyautogui.press(arg)

def scroll(direction):
    if direction == "up":
        pyautogui.scroll(200)
    elif direction == "down":
        pyautogui.scroll(-200)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot saved as screenshot.png")

def open_app(app):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(app)
        else:  # For macOS and Linux
            subprocess.call(["open", app])
    except Exception as e:
        print(f"Couldn't open {app}: {e}")

def minimize_window():
    pyautogui.hotkey('win', 'down')

def maximize_window():
    pyautogui.hotkey('win', 'up')

def close_window():
    pyautogui.hotkey('alt', 'f4')

def switch_window():
    pyautogui.hotkey('alt', 'tab')

def adjust_volume(action):
    if action == "increase":
        pyautogui.press('volumeup')
    elif action == "decrease":
        pyautogui.press('volumedown')
    elif action == "mute":
        pyautogui.press('volumemute')

def system_search(query):
    pyautogui.hotkey('win', 's')
    time.sleep(0.5)
    pyautogui.typewrite(query)
    pyautogui.press('enter')

def wait():
    time.sleep(0.5)


# Dictionary mapping command names to functions
command_map = {
    "move": move_cursor,
    "click": click,
    "right click": right_click,
    "double click": double_click,
    "type": type_text,
    "press": press,
    "scroll": scroll,
    "take screenshot": take_screenshot,
    "open": open_app,
    "minimize window": minimize_window,
    "maximize window": maximize_window,
    "close window": close_window,
    "switch window": switch_window,
    "adjust volume": adjust_volume,
    "search": system_search,
    "wait": wait,
}

def execute_command(command, args=None):
    if command in command_map:
        if args:
            command_map[command](*args)
        else:
            command_map[command]()
    else:
        print(f"Unknown command: {command}")