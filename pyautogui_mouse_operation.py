import pyautogui
import time

time.sleep(5)  # Wait for 5 seconds before starting the mouse operations

#mouse oper
pyautogui.moveTo(100, 100, duration=1)  # Move the mouse to (100, 100) over 1 second
pyautogui.click(100, 100, duration=1)  # click the mouse to (100, 100) over 1 second
pyautogui.rightclick(150, 100, duration=1)  # rightclick the mouse to (100, 100) over 1 second
pyautogui.leftclick(150, 100, duration=1)  # leftclick the mouse to (100, 100) over 1 second
pyautogui.doubleClick(100, 150, duration=1)  # double-click the mouse to (100, 100) over 1 second
pyautogui.dragTo(100, 150, duration=1)  # drag the mouse to (100, 100) over 1 second

time.sleep(1)  # Wait for 1 second before scrolling
pyautogui.scroll(500)  # scroll the mouse to scroll down 500 units ; if used -500, it will scroll up 500 units