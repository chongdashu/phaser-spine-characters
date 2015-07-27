import os
import json
import re
import random
import shutil

from PIL import Image
import list_assets as core


def is_shirt(imageName):
    return imageName.find("_short") >= 0 or imageName.find("_shorter") >= 0 or imageName.find("_long") >= 0


def normalize_shirts_or_pants(shirtsOrPants="Shirts"):

    shirtsFolder = core.PNG_PATH + shirtsOrPants
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


images = []
prefixes = []


def main():
    '''
    Shirts - Arms
    '''
    global images
    global prefixes

    # normalize_shirts_or_pants("Shirts")
    # normalize_shirts_or_pants("Pants")

    hairColors = ["Black", "Blonde", "Brown 1", "Brown 2", "Grey", "Red", "Tan", "White"]
    for hairColor in hairColors:
        folder = "Hair" + "/" + hairColor
        images = [image for image in core.get_files_in_folder(core.PNG_PATH + "Hair" + "/" + hairColor)]
        print "Analyzing %s" % (folder)
        maxWidth = 0
        maxHeight = 0
        maxWidthImageName = ""
        maxHeightImageName = ""
        for image in images:
            im = Image.open(core.get_image_path(image, core.PNG_PATH))
            if (im.size[0] > maxWidth):
                maxWidth = im.size[0]
                maxWidthImageName = image
            if (im.size[1] > maxHeight):
                maxHeight = im.size[1]
                maxHeightImageName = image
        print "size.max = (%s,%s), names=(%s,%s)" % (maxWidth, maxHeight, maxWidthImageName, maxHeightImageName)


if __name__ == "__main__":
    main()
