# Projeto-PicLib
Pic-Lib Project \
Jens Andreas & Pedro Travessa \
FC60919 and FC59479 \
# Project Part 1: 
*PicLib_Phase1.py* \
Creates a library enables you to create a collection based on the images given by the desired folder. \
It will be asked for a path to the respective folder before running, if the path isn't valid it will assume as correct path the current working directory. \
It creates a named folder "Album" in your directory with the images ordered by Date.
# Project Part 2: 
*PicLib_Phase2.py* \
This App enables an edit interface for **.jpg** or **.png** images and allows the user to search and interact with the metadata (Adding or removing Tags and Date) \
\
**Must replace path directly in code:** \
Imports all **.jpg** or **.png** files in the folder into the image display box. \
\
Buttons displayed at start:
- **Date button**, Displays the ate of an selected image
- **Page Navigation Arrow buttons**, If possible Navigate trough the pages.
- **T button**, the user opens the TagCollection (afterwards the user can choose the **+T button** which has the functionality to add a new Tag driven by a popup). 
- **S button**, the user can search the shown images with the mentioned Tag from TagCollection.
- **Change Image Display button**,

Selecting one and only one image:
- The **R90 button** appears when one image at a time is selected activating it´s function(90º degree rotation).
- The **Date button** of the selected image is displayed at the bottom row, shows up a popup to change the Date of that image when pressed (Displays 00:00:00 as hours but if you press again it will update to only display date as correct)
- The **Zip button** appears, the user as the option to create a ZIP file with that image (or more).The zip path stands for the **Name of the folder**, if you want to create that zip in another folder than the one you working at(default) you can put the path to the desired folder.

Selecting more than one image:
- The **+T button** allows the user to add a tag available in a TagCollection to one
or more images.
- The **-T button** allows the user to remove the tags related to those images.
- The **Zip button** appears, the user as the option to create a ZIP file with that image (or more).The zip path stands for the **Name of the folder**, if you want to create that zip in another folder than the one you working at(default) you can put the path to the desired folder.

**Observations:** \
When searching for tags it will display until 3 times the picture with that tag. \
You can add a tag to the image directly but it won display in the Tag Collection to solve that you must add a tag in tag collection and then add the tag you added with add tag button to the selected image/images.
**Filenames:** \
*PicLib_Phase1.py* \
*PicLib_Phase2.py*