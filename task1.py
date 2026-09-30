import pyautogui
import time
from datetime import datetime
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# 1. Press Windows Key + R to open the Run dialog
pyautogui.hotkey('win', 'r')

# 2. Short pause to allow the Run dialog window to appear
time.sleep(0.5)

# 3. Type 'excel' and press Enter to launch it
pyautogui.typewrite('chrome', interval=0.1)  # Type 'chrome' with a 0.1 second delay between each character
pyautogui.press('enter')
time.sleep(2)  # Wait for Chrome to open

print("Chrome browser launched successfully.")
weather_url = "https://weather.com/en-IN/in/delhi/city/new-delhi/today?Goto=Redirected"

# Focus the address bar using keyboard shortcut (Ctrl + L)
pyautogui.hotkey('ctrl', 'l')
time.sleep(0.5)

# Type the website URL
pyautogui.write(weather_url, interval=0.1)
pyautogui.press('enter')
time.sleep(3)  # Wait for the weather page to load before selecting text

# 4. Define the exact pixel coordinates for the start and end of the sentence
# (Hover your mouse and use pyautogui.displayMousePosition() to find these)
start_x, start_y = 23, 413  # Front of the first word
end_x, end_y = 203, 821      # End of the last word


# 5. Move to the start and drag to the end
pyautogui.moveTo(start_x, start_y, duration=0.5)
pyautogui.dragTo(end_x, end_y, duration=1.0, button='left')

# 6. Copy the highlighted sentence (use 'command' instead of 'ctrl' on Mac)
time.sleep(0.2)
pyautogui.hotkey('ctrl', 'c')

copied_text = pyperclip.paste().strip()
if not copied_text:
    raise RuntimeError("No text was copied. Check the selection coordinates and try again.")

# 7. Press Windows Key + R to open the Run dialog
pyautogui.hotkey('win', 'r')
time.sleep(0.5)

# 8. Type 'excel' and press Enter to launch it
pyautogui.write('excel', interval=0.1)  # Type 'excel' with a 0.1 second delay between each character
pyautogui.press('enter')

print("Excel launched successfully.")

#to start typing the date and time in the first cell, we can use the following code:
# 9. Wait for Excel to open and be ready
time.sleep(5)  # Wait for Excel to open and be ready

print("Typing the current date and time in the first cell...")
# 10. Type the current date and time in the first cell
pyautogui.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), interval=0.1)  # Type the current date and time with a 0.1 second delay between each character


#10. going to next cell
pyautogui.press('tab')  # Move to the next cell

#11. Paste the copied sentence into the next cell
pyautogui.hotkey('ctrl', 'v')  # Paste the copied sentence (use 'command' instead of 'ctrl' on Mac)

#12. going to next cell
pyautogui.press('enter')  # Move to the next cell

pyautogui.typewrite("Great day ahead!")  
