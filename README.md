# Projeto-PicLib
Pic-Lib Project \
Jens Andreas & Pedro Travessa \
FC60919 and FC59479 \
# Project Part 1: 
**File:** *PicLib_Phase1.py* \
Creates a library which enables you to create a collection based on the images given by the desired folder. \
It will be asked for a path to the respective folder before running, if the path isn't valid it will assume as correct path the current working directory. \
It creates a named folder "collectionsRootFolder" in your directory with the images ordered by Date, this file will be needed to work in *PicLib_Phase2.py*. \
It also creates a folder "ImageCollections" which will be used to store a text file with json data to represent the last saved image collection.
# Project Part 2: 
**File:** *PicLib_Phase2.py* \
This App enables an edit interface for **.jpg** or **.png** images and allows the user to search and interact with the metadata (Adding or removing Tags and Date). \
By running *PicLib_Phase2.py* both programs will run, *PicLib_Phase1.py* will run as previously mentioned, and *PicLib_Phase2.py* will start running and give you \
the option to either select a folder from which you will visualize the images, or the option to load a previous collection assuming you have saved one. \
\
**Double Click on Main Panel to Open a Folder** \
Imports all **.jpg** or **.png** files in the folder into the image display box. \
\
Buttons displayed at start:
- **Date button**, Displays the date of an selected image.
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

**Add-On:**\
The program also has two additional features, that are not included as part of Phase I but will be implemented later for better usability.

When the user starts the app and wants to **keep track** of their work, we added a way applied to the removed tag's, in another words, **if the user removes a tag from x image/images and at the end the user wants to know each images he did removed the tag's, the Search button will display a blank tag that serves as reference to the images which tag's were removed**. This blank tag **won´t** display at Tag Collection because it's not a tag it's a reference for those images that the user cleared their tag's.

Also the **Change Image Display**, permits all the ranges until 25 per page and a personalized display for certain numbers for a better and clear fitment in the layout.

**Walkthrough:** \
*Starting:*When we double click on main panel, it opens up file explorer window where users need to select their directory containing .jpeg/.jpg/PNGs. After selecting your Directory, the system will automatically import all jpg's / png's present inside that directory as well as subdirectories.

When searching for a specific tag, images with that tag associated with them are available on a new screen. If you want to remove a tag from the images, you must click on the image to remove the tag and press the T- button, when removing the tag and if there are no other tags in that image, it remains on the screen in case the user wants to replace the tag (where it removes the current one and places a new one), the same happens if the user decides to remove the tag from all displayed images, in the same way they remain on the screen, but without an associated tag. To return to the initial screen after removing the tags from the images and if that is what the user wants (W:Only display the images with the same tag and remove that same tag from the images), you must select the following buttons **'S'->'Reset'- >'OK'** in order to return to the initial screen.

If you want to **Save Collection** you must search with the **'S'** button for a tag or tag's assigned to the images you wanna save, after the search the screen will display those related pictures with selected tag's and in order to save the collection just **click to close** the App and on request close the program will ask you if you want to save or not that collection, Press **Yes** and the collection will be saved.
