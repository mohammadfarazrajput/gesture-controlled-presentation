import pyautogui
import time

class SlideController:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 1.0

    def next_slide(self):
        if time.time() - self.last_action_time > self.cooldown:
            pyautogui.press('right')
            print("✅ Next slide")
            self.last_action_time = time.time()

    def previous_slide(self):
        if time.time() - self.last_action_time > self.cooldown:
            pyautogui.press('left')
            print("✅ Previous slide")
            self.last_action_time = time.time()