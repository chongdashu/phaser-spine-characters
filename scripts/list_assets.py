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


def get_random(part):

    options = template["options"]
    character = template["character"]

    format = template["options"][part]["format"]
    format_keys = re.findall("\%([a-z]+)", format)

    obj = {}

    image_name = ""
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
            image_name += str(choice)

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



if __name__ == "__main__":
    main()

    obj, image_name = get_random("hair")

    print obj
    print image_name

