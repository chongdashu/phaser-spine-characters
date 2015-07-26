import os
import json
import re
import random
import shutil

from PIL import Image
import list_assets as core


def is_shirt(imageName):
    return imageName.find("_short") >= 0 or imageName.find("_shorter") >= 0 or imageName.find("_long") >= 0


images = []
prefixes = []


def main():
    '''
    Shirts - Arms
    '''
    global images
    global prefixes

    shirtsFolder = core.PNG_PATH + "Shirts"
    images = [image for image in core.get_files_in_folder(shirtsFolder) if is_shirt(image)]

    prefixes = list(set([image.split("_")[0] for image in images]))

    for prefix in prefixes:
        print "Normalizing %s" % (prefix)
        longImage = Image.open(core.get_image_path(prefix + "_long.png", core.PNG_PATH))
        shortImage = Image.open(core.get_image_path(prefix + "_short.png", core.PNG_PATH))
        shorterImage = Image.open(core.get_image_path(prefix + "_shorter.png", core.PNG_PATH))

        newShortImage = Image.new("RGBA", longImage.size)
        newShortImage.paste(shortImage, (0, 0))
        newShortImage.save(core.get_image_path(prefix + "_short.png", core.PNG_PATH))

        newShorterImage = Image.new("RGBA", longImage.size)
        newShorterImage.paste(shorterImage, (0, 0))
        newShorterImage.save(core.get_image_path(prefix + "_shorter.png", core.PNG_PATH))

if __name__ == "__main__":
    main()
