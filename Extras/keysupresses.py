import keyboard
# from pynput import keyboard

# def listen():
#     with keyboard.Events() as events:
#         # Block at most one second
#         event = events.get(112.0)
#         if event is None:
#             print('You did not press a key within one second')
#         else:
#             print('Received event {}'.format(event))
import time
import asyncio
import pyautogui
import keyboard
import os
from datetime import datetime
#import sys
import pystray
from PIL import Image
import webbrowser
from tkinter import messagebox
import platform
import subprocess
import wmi
import itertools
import firebase_admin
from firebase_admin import credentials, firestore
import requests  # Import requests library for network connectivity check
from customtkinter import *
from plyer import notification
import customtkinter as ctk
from dateutil.relativedelta import relativedelta

pyautogui.PAUSE = 0.000001

def is_premium():
    return True

# def hehe():
#     print("pressed alt+up")

# def left_arrow():
#     pyautogui.press('left')

# def down_arrow():
#     if is_premium():
#         pyautogui.press('down')  # Full functionality for the paid version
#     else:
#         return

# # wait = False

# # ## the wait  flag should be flase after 0.1 second

# # async def wait():
# #     if(wait == False):
# #         keyboard.add_hotkey('alt+up', hehe, suppress=True)
# #         wait = True
# #         time.sleep(1)
# #         wait = False
# #         keyboard.remove_hotkey('')
# #         keyboard.remap_hotkey('alt+w', 'up')
# #     else:
# #         print("now now")
# #         return
   

# def up_arrow():
#     if is_premium():
#         # keyboard.add_hotkey('alt+up', hehe, suppress=True)
#         pyautogui.press('up')       # Full functionality for the paid version
#         wait()
#     else:
#         return

# def right_arrow():
#     pyautogui.press('right')

# def page_up_key():
#     if is_premium():
#         pyautogui.press('pageup')  # Full functionality for the paid version
#     else:
#         return

# def page_down_key():
#     if is_premium():
#         pyautogui.press('pagedown')  # Full functionality for the paid version
#     else:
#         return

# def end_key():
#     if is_premium():
#         pyautogui.press('end')  # Full functionality for the paid version
#     else:
#         # print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
#         return

# def home_key():
#     if is_premium():
#         pyautogui.press('home')  # Full functionality for the paid version
#     else:
#         #print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
#         return

# def altup():
#     keyboard.remove_hotkey('alt+up')

# key_actions = {
#     'i': up_arrow,
#     'j': left_arrow,
#     'k': down_arrow,
#     'l': right_arrow
# }

# # Function to handle combinations
# def handle_combination(*keys):
#     for key in keys:
#         key_actions[key]()  # Call the respective function for each key


# # Add hotkeys for all combinations
# keys = ['i', 'j', 'k', 'l']

# # Single key combinations
# for key in keys:
#     keyboard.add_hotkey(f'alt+{key}', handle_combination, args=(key,), suppress=True)

# # Two key combinations
# for combo in itertools.permutations(keys, 2):
#     keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}', handle_combination, args=combo, suppress=True)

# # Three key combinations
# for combo in itertools.permutations(keys, 3):
#     keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}', handle_combination, args=combo, suppress=True)

# # Four key combinations
#     keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}+{combo[3]}', handle_combination, args=combo, suppress=True)
# for combo in itertools.permutations(keys, 4):

# # keyboard.add_hotkey('alt+shift+j', page_down_key, suppress=True)
# # keyboard.add_hotkey('alt+shift+i', page_up_key, suppress=True)
# keyboard.add_hotkey('alt+u', home_key, suppress=True)
# # keyboard.add_hotkey('alt+shift+l', end_key, suppress=True)
# keyboard.add_hotkey('alt+u', home_key, suppress=True)
# keyboard.add_hotkey('alt+o', end_key, suppress=True)
# keyboard.add_hotkey('alt+p', page_up_key, suppress=True)
# keyboard.add_hotkey('alt+;', page_down_key, suppress=True)
# keyboard.add_hotkey('alt+r', altup, suppress=True, trigger_on_release=True)
# # Run the tray icon application
# keyboard.remap_hotkey('alt+i','up')
keyboard.remap_hotkey('alt+k','down')
keyboard.remap_hotkey('alt+l','right')
keyboard.block_key('alt+up')
keyboard.remap_hotkey('alt+j','left')

while True:
    keyboard.wait()

icon.run()