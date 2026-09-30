from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        # If it's a left click, print the coordinates
        if button == mouse.Button.left:
            print(f"Clicked at X: {x}, Y: {y}")
        
        # If it's a right click, stop the listener completely
        elif button == mouse.Button.right:
            print("\nRight-click detected. Stopping script...")
            return False  # Returning False kills the pynput listener

print("Listening... LEFT-CLICK to print coordinates. RIGHT-CLICK to exit.")

# Start the listener without blocking the main loop awkwardly
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

"""
example output:


"""