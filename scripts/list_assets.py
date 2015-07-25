import os
import json
import re
import random
import shutil

'''
Global variables
'''
template = None
options = None
character = None
c = None

'''
Constants
'''

JSON_PATH = "../assets/json/"
PNG_PATH = "../assets/modularcharacters/PNG/"
PARTS_SCHEMA_PATH = "../assets/json/character_parts.json"
CHARACTER_TEMPLATE_PATH = "../assets/json/character_template.json"


def ensurePathForFile(filename):
    directory = os.path.dirname(filename)
    if not os.path.isdir(directory):
        print "*Note* Folder '%s' doesn't exist. Creating for file '%s'" %(directory,filename)
        os.makedirs(directory)


def ensurePathForFolder(foldername):
    if not os.path.exists(foldername):
        print "*Note* Folder '%s' doesn't exist. Creating now." %(foldername)
        os.makedirs(foldername)


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

    options = template["parts"]

    format = template["parts"][part]["format"]
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


def generate_character():

    character_template = json.loads(open(CHARACTER_TEMPLATE_PATH).read())
    character = {}

    character["template_version"] = character_template["template_version"]
    character["parts"] = {}

    for part_key, part_obj in character_template["parts"].iteritems():
        part_type = part_obj["part_type"]
        part_obj["part_info"], part_obj["image"] = get_random(part_type)

        character["parts"][part_key] = part_obj

    return character


def save_character(character, path, indent=4):
    s = json.dumps(character, indent=indent)
    open(path, "w").write(s)


def get_image_path(image_name, folder=""):

    files = [f for f in os.listdir(folder) if os.path.isfile(folder + "/" + f)]
    if image_name in files:
        return folder + "/" + image_name

    folders = [f for f in os.listdir(folder) if os.path.isdir(folder + "/" + f)]

    for fold in folders:
        path = get_image_path(image_name, folder + "/" + fold)
        if path:
            return path


def save_character_images(character, target_folder):
    key_and_images = [(part_key, part_obj["image"]) for (part_key, part_obj) in character["parts"].iteritems()]

    for part_key, image in key_and_images:
        path = get_image_path(image, PNG_PATH)
        if not path:
            print "Can't find: %s" % (path)
            exit(0)
        ensurePathForFolder(target_folder)
        shutil.copy2(path, target_folder + "/%s-%s" % (part_key, image))


def main():

    if not os.path.isdir(PNG_PATH):
        print "Could not locate the path to modularcharacters/PNG"

    global template
    global character

    character = json.loads(open(CHARACTER_TEMPLATE_PATH).read())

    top_categories = [top_category for top_category in os.listdir(PNG_PATH) if not top_category.startswith(".")]
    print "Listing the different %s top-level categories." % (len(top_categories))
    print "---------------------------------------------"
    for top_category in top_categories:
        print "|-%s" % (top_category)

    # Validate
    template = json.loads(open(PARTS_SCHEMA_PATH).read())
    assets_set = set([])
    for key, option in template["parts"].iteritems():
        ok, image_set, folder_files = check_assets(key, option["folder"])
        assets_set.update(image_set)
        print "All %s \tOK?:\t%s\t(Total: %s)\t(Files: %s)" % (key, ok, len(image_set), len(folder_files))
    print "Total assets generatable: %s" % (len(assets_set))
    print "Total assets available: %s" % (len(get_files_in_folder(PNG_PATH)))

    all_files_set = set(get_files_in_folder(PNG_PATH))
    all_files_set.difference_update(assets_set)

    if len(all_files_set) > 0:
        print "Here are the missing generatable files:"
        for image in all_files_set:
            print image

    global c
    c = generate_character()

    ## Generate a random character, no indent so that I can copy and paste it directly.
    ensurePathForFile("../gen/json/random_character.json")
    save_character(c, "../gen/json/random_character.json", indent=None)


    # save_character(c, JSON_PATH + "character_generated.json")
    # save_character_images(c, "../gen/spine")


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
