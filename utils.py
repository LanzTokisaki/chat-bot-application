from io import BytesIO
from PIL import Image

import PIL
import base64
import re

def image_to_base64(img) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    return "data:image/png;base64," + base64.b64encode(img_byte).decode()


def base64_to_image(data) -> PIL.Image:
    image = re.sub('data:image\/(.*?);base64,', '', data)
    return Image.open(BytesIO(base64.b64decode(image)))