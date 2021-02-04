import threading, os, winsound

Data = open("Data.txt", "r")
Lines = Data.readlines()
LeftMouseClicks = int(Lines[0][Lines[0].find("Left Clicks: ") + 13:])  # Get the number after the "Left Clicks: " string
RightMouseClicks = int(
    Lines[1][Lines[1].find("Right Clicks: ") + 14:])  # I add 13 because that the legnth of the string
MiddleMouseClicks = int(Lines[2][Lines[2].find("Middle Clicks: ") + 15:])  # "Left Clicks: " so that I get all the
MouseScrolls = int(Lines[3][Lines[3].find("Scrolls: ") + 9:])  # characters after it.
KeyPresses = int(Lines[4][Lines[4].find("Key Presses: ") + 13:])
LastLeftMouseClicksValue = LeftMouseClicks  # Need those variables so that I can throttle how many times it saves to
LastRightMouseClicksValue = RightMouseClicks  # txt file
LastMiddleMouseClicksValue = MiddleMouseClicks
LastMouseScrollsValue = MouseScrolls
LastKeyPressesValue = KeyPresses


def Quit():
    print("Quitting...")
    winsound.Beep(1000, 100)  # Makes a 1khz noise so that I know it actually worked
    os._exit(1)  # I have no idea what the heck this does but it terminates all the running threads which is what I need


# and apparently I need to have an int as an argument and idk whats the difference between each number but 1 worked so
# thats what I used.

def Save():
    global LeftMouseClicks  # need to make them global or else they will use local variables instead
    global RightMouseClicks
    global MiddleMouseClicks
    global MouseScrolls
    global LastLeftMouseClicksValue
    global Data
    global LastMiddleMouseClicksValue
    global LastMouseScrollsValue
    global LastRightMouseClicksValue
    global KeyPresses
    global LastKeyPressesValue
    Data.close()  # close the previously opened file at the start of the scipt
    Data = open("Data.txt", "w")  # open the same file in write mode
    Data.write(
        f"Left Clicks: {LeftMouseClicks}\nRight Clicks: {RightMouseClicks}\nMiddle Clicks: {MiddleMouseClicks}\nScrolls: {MouseScrolls}\nKey Presses: {KeyPresses}")
    Data.close()


def InitializeMouse():
    from pynput import mouse

    def on_click(x, y, button, pressed):
        global LeftMouseClicks  # same global thingy mentioned earlier
        global RightMouseClicks
        global MiddleMouseClicks
        global MouseScrolls
        global LastLeftMouseClicksValue
        global Data
        global LastMiddleMouseClicksValue
        global LastMouseScrollsValue
        global LastRightMouseClicksValue
        if pressed == True and button == button.left:  # check if its a left click
            LeftMouseClicks += 1
            print(LeftMouseClicks)
            if LeftMouseClicks - LastLeftMouseClicksValue == 50:  # check if left clicks was clicked then save
                LastLeftMouseClicksValue = LeftMouseClicks
                Save()
        if pressed == True and button == button.right:  # check if its a right click
            RightMouseClicks += 1
            print(RightMouseClicks)
            if RightMouseClicks - LastRightMouseClicksValue == 20:
                LastRightMouseClicksValue = RightMouseClicks
                Save()
        if pressed == True and button == button.middle:  # check if its a middle click
            MiddleMouseClicks += 1
            print(MiddleMouseClicks)
            if MiddleMouseClicks - LastMiddleMouseClicksValue == 10:
                LastMiddleMouseClicksValue = MiddleMouseClicks
                Save()

    def on_scroll():
        global Data  # same global thingy mentioned earlier
        global LastMouseScrollsValue
        global MouseScrolls
        MouseScrolls += 1
        print(MouseScrolls)
        if MouseScrolls - LastMouseScrollsValue == 50:  # check if its a scroll
            LastMouseScrollsValue = MouseScrolls
            Save()

    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


def InitializeKeyboard():
    from pynput import keyboard
    # hotkey thingy idk how it works exactly I just copied it from the internet
    current = set()

    COMBINATIONS = [
        {keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l}
    ]

    def on_press(key):  # also hotkey thingy
        if any([key in COMBO for COMBO in COMBINATIONS]) and not key in current:
            current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            Quit()

    def on_release(key):
        global Data  # same global thingy mentioned earlier
        global KeyPresses
        global LastKeyPressesValue
        KeyPresses += 1
        print(KeyPresses)
        if any([key in COMBO for COMBO in COMBINATIONS]):  # this if statement is for the hotkey thingy
            current.remove(key)
        if KeyPresses - LastKeyPressesValue == 100:  # The reason I am only counting the released keys is because if I
            LastKeyPressesValue = KeyPresses  # hold a key for a while it will register multiple key presses but you
            Save()  # can only release a key once after pressing it.

    with keyboard.Listener(on_press=on_press, on_release=on_release) as KeyboardListener:
        KeyboardListener.join()


MouseThread = threading.Thread(target=InitializeMouse, args=())  # Create a thread for the mouse
KeyboardThread = threading.Thread(target=InitializeKeyboard, args=())  # Create a thread for the keyboard
# start both threads
MouseThread.start()
KeyboardThread.start()