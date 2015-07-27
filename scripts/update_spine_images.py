import os
import json
import re
import random
import shutil

from PIL import Image
import list_assets as core

SPINE_IMAGES_PATH = "../assets/spine/character_images/"


def main():
    images = core.get_files_in_folder(SPINE_IMAGES_PATH)
    for image in images:
        if image == ".DS_Store":
            continue
        imageName = image.split("-")[1]

        src = core.get_image_path(imageName, core.PNG_PATH)
        dst = SPINE_IMAGES_PATH + image
        shutil.copyfile(src, dst)

        print "Copying from %s to %s ..." % (src, dst)

if __name__ == "__main__":
    main()
