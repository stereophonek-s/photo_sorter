# Photos and Clips Organizer

## Overview

This program provides an intuitive graphical interface to organize photos and video files by sorting them into folders based on their modification timestamps (year and month). It includes features to handle filename conflicts, allowing users to skip conflicting files or rename them with incremented names. The app also previews images for quick decision-making during conflicts.

---

## Features

- **Folder Selection**: Browse and select source and destination folders via a graphical interface.
- **File Organization**: Automatically organizes files into `Year/Month` subfolders in the destination folder.
- **Conflict Resolution**: Handles duplicate file names with options to:
  - Skip the conflicting file.
  - Rename the file by appending a counter to its name.
- **Preview**: Displays previews of conflicting image files side-by-side.
- **File Info**: Shows file name and size information for quick reference.
- **Support for Various File Types**:
  - Images: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`
  - Non-image files show only basic info.

---

## Requirements

- Python 3.5 or higher.
- Required Python libraries:
  - `tkinter` (built-in for most Python distributions).
  - `os` (standard library).
  - `shutil` (standard library).
  - `Pillow` (install via `pip install pillow`).

---

## Installation

1. Clone or download this repository.
2. Ensure Python 3.5+ is installed on your system.
3. Install dependencies:
   ```bash
   pip install pillow
How to Use
Run the script:
bash
Копиране на код
python organizer.py
Source Folder: Select the folder containing files to organize.
Destination Folder: Select the folder where organized files will be saved.
Click Start Organizing to begin the process.
If a file conflict occurs:
Skip: Move to the next file without resolving the conflict.
Rename: Automatically rename the file to avoid overwriting.
GUI Layout
Source Folder Input:
Text field and "Browse" button to select the source directory.
Destination Folder Input:
Text field and "Browse" button to select the destination directory.
File Preview Area:
Displays the current file and conflicting file (if applicable).
File Info Panel:
Shows the file name and size for the current and conflicting files.
Control Buttons:
Start Organizing: Begins file processing.
Skip: Skips a file in conflict.
Rename: Renames a file in conflict to resolve it.
Notes
Files are organized based on their last modified timestamp.
Non-image files are processed without previews.
The app creates necessary subfolders (Year/Month) in the destination folder.
License
This program is open-source and provided under the MIT License.

Screenshots
(Include screenshots of the interface here, if applicable.)

Enjoy organizing your files efficiently with Photos and Clips Organizer! 😊
