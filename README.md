# Spine-Characters

An example project to get some character images working working
together in Spine.

## Status

This is still in-development.

## Descriptions

### Assets

#### JSON

JSON files serves as a data format to store information, probably particular useful for passing between server and client.

0. `character_template.json` is a schema for a character.

## Scripts

The scripts folder contains some useful scripts. Here are a list of them:

0. `list_assets.py`: Looks through the `character_template.json` schema and uses it to generate different possible image names for each part of the character. This is just a utility script to make sure that no PNG image file in `assets/modularcharacters/PNG` is unused.

0. `image_processing.py`: Looks through a bunch of the assets to help to normalize them in a way that doesn't require spine-js/spine-canvas to recalculate the UVs each time textures are swapped.   
    + Note: To run scripts, you will need the following python packages.
     0. Pillow (i.e., pip install Pillow)


### Character Changes

I detected some naming inconsistencies in some of the files provided in the character pack. These were detected by the script `list_assets.py` above. The following list specifies which asset files, particularly PNG files, were renamed from the original set in order to maintain a consistent naming convention.

+ In `Pants/Yellow/`: renamed `legYellow_<...>` to `pantsYellow_<...>` for consistency.
+ In `Shirts/White/`: renamed `armWhite_<...>` to `whiteArm_<...>` for consistency.
+ In `Shirts/Yellow/`: renamed `shirtYellow<...>` to `yellowShirt<...>` for consistency.

### Normalizing images

Because of the way Spine handles bone attachments -- some categories of images have been normalized such that they are of the same size and center-aligned, where possible. Transparent pixels are placed to pad up images that were initially smaller. 


## Included  External Resources

Thanks to generous folks who have provided many different libraries/tools that have made this project possible.

### External Libraries

External libraries that this project makes use of are included,
together with their respective licenses. 

0. [Phaser](http://www.phaser.io)
0. [jQuery](http://jquery.com)
0. [Twitter Bootstrap](http://getbootstrap.com)
0. [Bootstrap Material Design](https://fezvrasta.github.io/bootstrap-material-design/bootstrap-elements.html)

### External Assets

External resources that are used here are also included,
together with their respective licenses.

0. [Kenney's Modular Character Pack](http://kenney.nl/assets/modular-characters)
