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


def normalize_hair():

    hairColors = ["Black", "Blonde", "Brown 1", "Brown 2", "Grey", "Red", "Tan", "White"]

    # gender = "Man"
    # gender = "Woman"
    gender = "an"      # "an" is contained in both "Man" and "Woman"

    for hairColor in hairColors:
        folder = "Hair" + "/" + hairColor
        images = [image for image in core.get_files_in_folder(core.PNG_PATH + "Hair" + "/" + hairColor)]
        images = [image for image in images if image.find(gender) >= 0]
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

        for image in images:
            newImage = Image.new("RGBA", (maxWidth, maxHeight))
            oldImage = Image.open(core.get_image_path(image, core.PNG_PATH))

            offsetX = 0
            offsetY = 0

            # Male
            # offsetX = 0
            # offsetY = (maxHeight - oldImage.size[1])

            # Female
            # offsetX = (maxWidth - oldImage.size[0])/2
            # offsetY = 0

            # an
            # Only do this after  normalizing both male and females!
            if image.find("Woman") >= 0:
                offsetX = (maxWidth - oldImage.size[0])/2
                offsetY = 0
            elif image.find("Man") >= 0:
                offsetX = 7  # magic number from photoshop
                offsetY = -18  # magic number from photoshop

            newImage.paste(oldImage, (offsetX, offsetY))
            newImage.save(core.get_image_path(image, core.PNG_PATH))

            print "Normalizing: %s, %s, offset=(%s,%s)" % (image, oldImage.size, offsetX, offsetY)

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
    # normalize_hair()

    # TODO: normalize_eyebrows
    # TODO: normalize_mouth

    images = core.get_files_in_folder(core.PNG_PATH + "Face/Eyebrows")
    for image in images:
        maxWidth = 0
        maxHeight = 0
        maxWidthImageName = ""
        maxHeightImageName = ""
        im = Image.open(core.get_image_path(image, core.PNG_PATH))
        if (im.size[0] > maxWidth):
            maxWidth = im.size[0]
            maxWidthImageName = image

        if (im.size[1] > maxHeight):
            maxHeight = im.size[1]
            maxHeightImageName = image
    print "size.max = (%s,%s), names=(%s,%s)" % (maxWidth, maxHeight, maxWidthImageName, maxHeightImageName)

    for image in images:
        newImage = Image.new("RGBA", (maxWidth, maxHeight))
        oldImage = Image.open(core.get_image_path(image, core.PNG_PATH))

        offsetX = 0
        # offsetY = 0

        # offsetX = (maxWidth - oldImage.size[0])/2
        offsetY = (maxHeight - oldImage.size[1])/2

        newImage.paste(oldImage, (offsetX, offsetY))
        # newImage.save(core.get_image_path(image, core.PNG_PATH))

        print "Normalizing: %s, %s, offset=(%s,%s)" % (image, oldImage.size, offsetX, offsetY)


if __name__ == "__main__":
    main()
