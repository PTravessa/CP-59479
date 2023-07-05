# Projeto-PicLib
Pic-Lib Project \
Jens Andreas & Pedro Travessa \
FC60919 and FC59479 \
# Project Part 1: 
**File:** *PicLib_Phase1.py* \
Creates a library enables you to create a collection based on the images given by the desired folder. \
It will be asked for a path to the respective folder before running, if the path isn't valid it will assume as correct path the current working directory. \
It creates a named folder "Album" in your directory with the images ordered by Date, this file will be needed to work in *PicLib_Phase2.py*.
# Project Part 2: 
**File:** *PicLib_Phase2.py* \
This App enables an edit interface for **.jpg** or **.png** images and allows the user to search and interact with the metadata (Adding or removing Tags and Date). \
By running *PicLib_Phase2.py* both programs will run, *PicLib_Phase1.py* is started primarily where you are asked for a path input on the command line, this path is for the location of the folder that contains the images you want to use in *PicLib_Phase1.py*. When entering the path, if it is not valid, the current directory in which the program is running is considered as path, reading all the images present in it, after validating the path using the *PicLib_Phase1.py* program, it executes its function and creates a new folder named "Album", this same must be selected when using the App programmed in the *PicLib_Phase2.py*.\
\
**Double Click on Main Panel to Open a Folder** \
Imports all **.jpg** or **.png** files in the folder into the image display box. \
\
Buttons displayed at start:
- **Date button**, Displays the ate of an selected image.
- **Page Navigation Arrow buttons**, If possible Navigate trough the pages.
- **T button**, the user opens the TagCollection (afterwards the user can choose the **+T button** which has the functionality to add a new Tag driven by a popup). 
- **S button**, the user can search the shown images with the mentioned Tag from TagCollection.
- **Change Image Display button**, It manages the amount of images displaying in the main panel until the maximum,25 images per page is reached.

Selecting one and only one image:
- The **R90 button** appears when one image at a time is selected activating it´s function(90º degree rotation).
- The **Date button** of the selected image is displayed at the bottom row, shows up a popup to change the Date of that image when pressed.
- The **Zip button** appears, the user as the option to create a ZIP file with that image (or more).The zip path stands for the **Name of the folder**, if you want to create that zip in another folder than the one you working at(default) you can put the path to the desired folder.

Selecting more than one image:
- The **+T button** allows the user to add a tag available in a TagCollection to one
or more images.
- The **-T button** allows the user to remove the tags related to those images.
- The **Zip button** appears, the user as the option to create a ZIP file with that image (or more).The zip path stands for the **Name of the folder**, if you want to create that zip in another folder than the one you working at(default) you can put the path to the desired folder.

**Observations:** \
When searching for a specific tag, images with that tag associated with them are available on a new screen. If you want to remove a tag from the images, you must click on the image to remove the tag and press the T- button, when removing the tag and if there are no other tags in that image, it remains on the screen in case the user wants to replace the tag (where it removes the current one and places a new one), the same happens if the user decides to remove the tag from all displayed images, in the same way they remain on the screen, but without an associated tag. To return to the initial screen after removing the tags from the images and if that is what the user wants (W:Only display the images with the same tag and remove that same tag from the images), you must select the following buttons **'S'->'Reset'- >'OK'** in order to return to the initial screen.