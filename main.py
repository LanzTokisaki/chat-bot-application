from tkinter import Tk
from tkinter import filedialog

import eel
import importlib
import message_handler
import urllib


root = Tk()
root.attributes('-topmost',True)
root.withdraw()

@eel.expose
def on_message(msg: dict):
    image = None

    if isinstance(msg, str):
        text = msg

    elif isinstance(msg, dict):
        text = msg.get("text", "")
        image = msg.get("image", None)
    
    text = text.strip()
    
    if text.startswith("_"):
        return

    importlib.reload(message_handler)
    
    command = text.split(' ')[0].lower()

    if command in dir(message_handler):
        func = getattr(message_handler, command)

        if not callable(func):
            return 

        msg = message_handler.MessageInfo(text, image)
        response = func(msg)

        if isinstance(response, message_handler.MessageInfo):
            eel.add_bot_message(response.toJson())

        elif isinstance(response, list):
            for res in response:
                if isinstance(res, message_handler.MessageInfo):
                    eel.add_bot_message(res.toJson())


@eel.expose
def save_image(image):

    data = urllib.request.urlopen(image)

    filetypes = (("PNG File", "*.png")
                ,("JPG/JPEG File", "*.jpg;*.jpeg")
                ,("All files", "*.*"))

    filename = filedialog.asksaveasfilename(filetypes=filetypes, parent=root, defaultextension="*.png")

    if filename:
        with open(filename, 'wb') as wb:
            wb.write(data.read())



eel.init("www")
eel.start("index.html")

