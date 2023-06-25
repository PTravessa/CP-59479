import tkinter as tk
from tkinter import filedialog
import os


class FolderSelectionPopup:
    def __init__(self, default_folder):
        self.default_folder = default_folder
        self.folder_path = None

    def select_folder(self):
        # Create the root window
        root = tk.Tk()
        root.withdraw()

        # Open the folder selection dialog
        folder_path = filedialog.askdirectory(initialdir=os.getcwd())

        # Convert the selected path to the appropriate format
        folder_path = os.path.abspath(folder_path).replace(os.sep, "/")

        self.folder_path = folder_path

    def get_selected_folder(self):
        return self.folder_path
