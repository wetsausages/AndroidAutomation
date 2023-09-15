import os
import threading
from time import sleep

def execute(command):
    os.system(f"adb {command}")

def tap(x, y, delay=0.5):
    execute(f"shell input tap {x} {y}")
    sleep(delay)

def swipe(x1, y1, x2, y2, duration=1, delay=0.5):
    execute(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    sleep(delay)

def input_text(text, delay=0.5):
    execute(f'shell input text "{text}"')
    sleep(delay)

def press_button(keycode, delay=0.5):
    execute(f"shell input keyevent {keycode}")
    sleep(delay)

def pinch(x1a, y1a, x2a, y2a, x1b, y1b, x2b, y2b):
    swipe1_thread = threading.Thread(target=swipe, args=(x1a, y1a, x2a, y2a))
    swipe2_thread = threading.Thread(target=swipe, args=(x1b, y1b, x2b, y2b))
    swipe1_thread.start()
    swipe2_thread.start()