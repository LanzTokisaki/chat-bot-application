from PIL import ImageOps
from io import BytesIO
from datetime import datetime
from google_images_download import google_images_download

import wikipedia as _wikipedia
import utils
import random
import requests
import base64



# Constants
ERROR_INVALID_ARG = "Error. Please provide a valid argument."
ERROR_MISSING_ARG = "Error. Please provide an argument."

ERROR_MISSING_IMAGE = "Error. Please provide an image."
ERROR_MISSING_KEYWORD = "Error. Please provide a keyword."
ERROR_MISSING_TEXT = "Error. Please provide a text."

ERROR_MATH = "Error. The text provided does not appear to be a basic math problem."
ERROR_WIKIPEDIA = "Error. The text provided does not match any pages."


image_downloader = google_images_download.googleimagesdownload()


class MessageInfo:
    def __init__(self, text: str = None, image=None):
        self.text = text
        self.image = image

    def toJson(self) -> dict:
        return {
            "text": self.text,
            "image": self.image
        }



def calculate(msg: MessageInfo) -> MessageInfo:
    if ' ' in msg.text:
        problem = msg.text.split(' ', 1)[1]
        try:
            text = str(eval(problem))
        except:
            text = ERROR_MATH
    else:
        text = ERROR_MISSING_TEXT

    return MessageInfo(text)


def coinflip(_: MessageInfo) -> MessageInfo:
    outcomes = ["Heads", "Tails"]
    text = random.choice(outcomes)

    return MessageInfo(text)


def date(msg: MessageInfo) -> MessageInfo:
    date = datetime.date(datetime.now())

    if ' ' in msg.text:
        arguments = msg.text.split(' ', 1)[1]
        day = date.strftime("%d")
        month = date.strftime("%B")
        year =  date.strftime("%Y")
        week = date.strftime("%A")

        text = arguments.lower().replace("day", day) \
                                .replace("month", month) \
                                .replace("year", year) \
                                .replace("week", week) \
            
        if text == arguments:
            text = ERROR_INVALID_ARG

    else:
        text = date.strftime('%B %d, %Y (%A)')

    return MessageInfo(text)


def image(msg: MessageInfo) -> MessageInfo:
    
    if ' ' in msg.text:
        arguments = msg.text.split(' ', 1)[1].replace(", ", ",")
        args = {"keywords": arguments,
                "limit": 20,
                "silent_mode": True,
                "print_urls": False, 
                "no_download": True,
                "format": "png"}

        keywords = arguments.split(",")

        results = image_downloader.download(args)[0]

        msgs = []

        for keyword in keywords:
                    
            result = random.choice(results[keyword])
            response = requests.get(result)

            data = ("data:" + response.headers['Content-Type'] + ";" +
                    "base64," + base64.b64encode(response.content).decode("utf-8"))

            msg_info = MessageInfo(text=None, image=data)
            msgs.append(msg_info)
            
        return msgs

    else:
        return MessageInfo(ERROR_MISSING_KEYWORD)


def flip(msg: MessageInfo) -> MessageInfo:
    text = ""
    image = None

    if not msg.image:
        text = ERROR_MISSING_IMAGE
    
    else:
        image = msg.image
        im = utils.base64_to_image(image)
        im = ImageOps.flip(im)
        image = utils.image_to_base64(im)

    return MessageInfo(text, image)


def hi(_: MessageInfo) -> MessageInfo:
    return MessageInfo("Hello!")


def help(_: MessageInfo) -> MessageInfo:

    with open("help.txt", 'r') as R:
        msgs = R.readlines()
    

    msgs = [MessageInfo(msg) for msg in msgs]
    
    return msgs


def hello(_: MessageInfo) -> MessageInfo:
    return MessageInfo("Hi!")


def mirror(msg: MessageInfo) -> MessageInfo:
    text = ""
    image = None

    if not msg.image:
        text = ERROR_MISSING_IMAGE
    
    else:
        image = msg.image
        im = utils.base64_to_image(image)
        im = ImageOps.mirror(im)
        image = utils.image_to_base64(im)

    return MessageInfo(text, image)


def rotate(msg: MessageInfo) -> MessageInfo:
    text = image = None

    if not msg.image:
        text = ERROR_MISSING_IMAGE
    elif ' ' not in msg.text:
        text = ERROR_MISSING_ARG 
    else:
        argument = msg.text.split(' ', 1)[1].lower()

        degree = None

        if argument in ["l", "left"]:
            degree = 90
        elif argument in ["r", "right"]:
            degree = -90
        else:
            text = ERROR_INVALID_ARG

        if degree:
            image = msg.image
            im = utils.base64_to_image(image)
            im = im.rotate(degree, expand=1)
            image = utils.image_to_base64(im)

    return MessageInfo(text, image)


def repeat(msg: MessageInfo) -> MessageInfo:
    if not ' ' in msg.text and not msg.image:
        text = ERROR_MISSING_TEXT
    else:
        try:
            text = msg.text.split(' ', 1)[1]
        except:
            text = ''
    
    image = msg.image
    return MessageInfo(text, image)


def reverse(msg: MessageInfo) -> MessageInfo:
    if ' ' in msg.text:
        text = msg.text.split(' ', 1)[1][::-1]
    else:
        text = ERROR_MISSING_TEXT
    
    return MessageInfo(text)


def rng(msg: MessageInfo) -> MessageInfo:
    min = 0
    max = 100

    if ' ' in msg.text:
        splitted = msg.text.split(' ')

        if len(splitted) == 3:
            min = splitted[1]
            max = splitted[2]
        else:
            max = splitted[1]
    
    try:
        min = int(min)
        max = int(max)
        text = str(random.randint(min, max))
    except:
        text = ERROR_INVALID_ARG

    return MessageInfo(text)


def time(msg: MessageInfo) -> MessageInfo:
    time  = datetime.time(datetime.now())

    if ' ' in msg.text:
        arguments = msg.text.split(' ', 1)[1]

        hour = time.strftime("%I")
        if hour.startswith("0"):
            hour = hour[1:]
            
        minute = time.strftime("%M")
        seconds =  time.strftime("%S")
        period = time.strftime("%p")

        text = arguments.lower().replace(" hour", hour) \
                                .replace("h", hour) \
                                .replace("minute", minute) \
                                .replace("m", minute) \
                                .replace("second", seconds) \
                                .replace("s", seconds) \
                                .replace("period", period) \
                                .replace("p", period)

        if text == arguments:
            text = ERROR_INVALID_ARG

    else:
        text = datetime.time(datetime.now()).strftime("%I:%M %p")
        if text.startswith("0"):
            text = text[1:]

    return MessageInfo(text)


def wikipedia(msg: MessageInfo) -> MessageInfo:
    splitted = msg.text.split(' ', 1)

    msgs = []

    if len(splitted) == 0:
        text = ERROR_MISSING_TEXT
    else:
        arguments = splitted[1]
        try:
            r = _wikipedia.page(arguments, auto_suggest=False)

            msgs.append(MessageInfo(r.summary))
            msgs.append(MessageInfo("Source: " + r.url))
            
        except:
            text = ERROR_WIKIPEDIA
            
    
    return msgs

