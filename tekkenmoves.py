# import pyautogui
# import keyboard

# def myMove():
#     pyautogui.press('z')
#     pyautogui.press('s')
#     pyautogui.press('x')
#     pyautogui.press('z')
    
#     # Press 'x' and 'a' simultaneously
#     pyautogui.keyDown('x')
#     pyautogui.press('a')
#     pyautogui.keyUp('x')
    
#     pyautogui.press('s')
#     pyautogui.press('s')
#     pyautogui.press('a')
#     pyautogui.press('s')

# keyboard.add_hotkey('o', myMove, suppress=True, trigger_on_release=True)

# # This keeps the program running to listen for the hotkey
# keyboard.wait('esc')

import win32api
import win32con
import time
import threading

# Key codes for pywin32
VK_CODE = {
    'a': 0x41,
    's': 0x53,
    'x': 0x58,
    'z': 0x5A,
    'o': 0x4F,
    'esc': 0x1B,
}

def press_key(hexKeyCode):
    win32api.keybd_event(hexKeyCode, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(hexKeyCode, 0, win32con.KEYEVENTF_KEYUP, 0)

def myMove():
    press_key(VK_CODE['z'])
    press_key(VK_CODE['s'])
    press_key(VK_CODE['x'])
    press_key(VK_CODE['z'])
    
    # Press 'x' and 'a' simultaneously
    win32api.keybd_event(VK_CODE['x'], 0, 0, 0)
    press_key(VK_CODE['a'])
    win32api.keybd_event(VK_CODE['x'], 0, win32con.KEYEVENTF_KEYUP, 0)
    
    press_key(VK_CODE['s'])
    press_key(VK_CODE['s'])
    press_key(VK_CODE['a'])
    press_key(VK_CODE['s'])

def hotkey_listener():
    while True:
        if win32api.GetAsyncKeyState(VK_CODE['o']):
            myMove()
            time.sleep(0.5)  # debounce delay
        if win32api.GetAsyncKeyState(VK_CODE['esc']):
            break

listener_thread = threading.Thread(target=hotkey_listener)
listener_thread.start()

# This keeps the program running
listener_thread.join()