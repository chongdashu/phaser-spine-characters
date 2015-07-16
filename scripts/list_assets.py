import os
import json
import re
import random

'''
Global variables
'''
template = None

'''
Constants
'''

PNG_PATH = "../assets/modularcharacters/PNG/"
TEMPLATE_JSON_PATH = "../assets/json/character_template.json"


def get_asset_files(part):
    return get_files_in_folder(PNG_PATH + part.title())


def get_files_in_folder(path):
    if os.path.isfile(path):
        return [path.split("/")[-1]]
    files = []
    for folder in os.listdir(path):
        files += get_files_in_folder(path + "/" + folder)
    return files


def get_random(part):

    options = template["options"]
    # character = template["character"]

    format = template["options"][part]["format"]
    format_keys = re.findall("\<([a-z]+)\>", format)

    obj = {}

    image_name = format

    for key in format_keys:
        choices = options[part][key]

        if type(choices) == dict:
            prev_key = None
            while (not prev_key or prev_key not in format_keys):
                prev_key = format_keys[format_keys.index(key)-1]

            prev_key_choice = obj[prev_key]
            choices = choices[prev_key_choice]

        if type(choices) == int:
                choices = range(1, 1+choices)

        if type(choices) == list:

            choice = random.choice(choices)

            obj[key] = choice

    for key in format_keys:
        image_name = image_name.replace("<%s>" % (key), str(obj[key]))

    image_name += ".png"

    return obj, image_name


def main():

    if not os.path.isdir(PNG_PATH):
        print "Could not locate the path to modularcharacters/PNG"

    global template

    top_categories = [top_category for top_category in os.listdir(PNG_PATH) if not top_category.startswith(".")]
    print "Listing the different %s top-level categories." % (len(top_categories))
    print "---------------------------------------------"
    for top_category in top_categories:
        print "|-%s" % (top_category)

    # Validate
    template = json.loads(open(TEMPLATE_JSON_PATH).read())
    for key, option in template["options"].iteritems():

        ok, image_set, folder_files = check_assets(key, option["folder"])
        print "All %s \tOK?:\t%s\t(Total: %s)\t(Files: %s)" % (key, ok, len(image_set), len(folder_files))


def check_assets(part_key, folder_key, n=5000):
    all_ok = True
    image_names = []
    folder_files = get_asset_files(folder_key)
    for i in range(n):
        obj, image_name = get_random(part_key)
        ok = image_name in folder_files
        all_ok = all_ok and ok
        if not all_ok:
            print "Couldn't find '%s' for part %s in folder %s" % (image_name, part_key, folder_key)
            break
        image_names.append(image_name)

    return all_ok, set(image_names), folder_files


if __name__ == "__main__":
    main()
