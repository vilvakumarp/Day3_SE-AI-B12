import pyautogui
import time

pyautogui.typewrite('Hello, World!', interval=0.1)  # Type 'Hello, World!' with a 0.1 second delay between each character

#hotkeys
pyautogui.hotkey('cmd', 'c')  # Press Cmd+C to copy
pyautogui.hotkey('cmd', 'v')  # Press Cmd+V to paste
pyautogui.hotkey('cmd', 'a')  # Press Cmd+A to select all
pyautogui.hotkey('cmd', 'z')  # Press Cmd+Z to undo
pyautogui.hotkey('cmd', 'y')  # Press Cmd+Y to redo
pyautogui.hotkey('cmd', 's')  # Press Cmd+S to save



#pressing keys
pyautogui.press('enter')  # Press the Enter key
pyautogui.press('tab')  # Press the Tab key
pyautogui.press('backspace')  # Press the Backspace key
pyautogui.press('space')  # Press the Space key

#hold
pyautogui.keyDown('shift')  # Hold the Shift key
pyautogui.typewrite('This text is typed while holding Shift.', interval=0.1)  # Type text while holding Shift (will be in uppercase)
pyautogui.keyUp('shift')  # Release the Shift key
pyautogui.typewrite('This text is typed after releasing Shift.', interval=0.1)  # Type text after releasing Shift (will be in lowercase)
