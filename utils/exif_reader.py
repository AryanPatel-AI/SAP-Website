from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif(image):

    img = Image.open(image)
    exif = img._getexif()

    data = {}

    if exif:
        for tag,value in exif.items():
            name = TAGS.get(tag)
            data[name] = value

    return data