import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import time


class OrganizerApp:
    def __init__(self, master):
        self.root = master  # Renamed parameter to avoid shadowing 'root'
        self.root.title("Photos and Clips Organizer")

        # Initialize folders and variables
        self.source_folder = ""
        self.destination_folder = ""
        self.current_file = None
        self.conflict_file_path = None
        self.source_image = None
        self.destination_image = None

        # GUI layout
        tk.Label(master, text="Source Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.source_entry = tk.Entry(master, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(master, text="Destination Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.destination_entry = tk.Entry(master, width=50)
        self.destination_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=5, pady=5)

        # Image labels for previews
        self.source_image_label = tk.Label(master)
        self.source_image_label.grid(row=2, column=0, padx=5, pady=5)

        self.destination_image_label = tk.Label(master)
        self.destination_image_label.grid(row=2, column=2, padx=5, pady=5)

        self.file_info = tk.Label(master, text="File Name: -\nSize: -", font=("Arial", 10))
        self.file_info.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(master, text="Start Organizing", command=self.start_organizing).grid(row=4, column=1, padx=5, pady=5)
        self.skip_button = tk.Button(master, text="Skip", command=self.skip_file, state=tk.DISABLED)
        self.skip_button.grid(row=5, column=0, padx=5, pady=5)
        self.rename_button = tk.Button(master, text="Rename", command=self.rename_file, state=tk.DISABLED)
        self.rename_button.grid(row=5, column=2, padx=5, pady=5)

        self.files_to_process = []

    def browse_source(self):
        self.source_folder = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, self.source_folder)

    def browse_destination(self):
        self.destination_folder = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, self.destination_folder)

    def start_organizing(self):
        if not self.source_folder or not self.destination_folder:
            messagebox.showwarning("Warning", "Please select both source and destination folders.")
            return

        # Gather all files from the source folder and subdirectories
        for root_dir, _, files in os.walk(self.source_folder):
            for file in files:
                file_path = os.path.join(root_dir, file)
                self.files_to_process.append(file_path)

        self.process_next_file()

    def process_next_file(self):
        # Check if there are files left to process
        if not self.files_to_process:
            messagebox.showinfo("Info", "Organization complete!")
            self.skip_button.config(state=tk.DISABLED)
            self.rename_button.config(state=tk.DISABLED)
            return

        # Get the next file to process
        self.current_file = self.files_to_process.pop(0)

        # Determine destination folder based on timestamp
        timestamp = os.path.getmtime(self.current_file)
        year_folder = time.strftime("%Y", time.localtime(timestamp))
        month_folder = time.strftime("%m", time.localtime(timestamp))
        destination_folder_path = os.path.join(self.destination_folder, year_folder, month_folder)
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

        # Prepare the final destination path
        final_destination_path = os.path.join(destination_folder_path, os.path.basename(self.current_file))

        # Check for conflicts
        if os.path.exists(final_destination_path):
            # Conflict detected: enable skip and rename buttons
            self.skip_button.config(state=tk.NORMAL)
            self.rename_button.config(state=tk.NORMAL)
            self.conflict_file_path = final_destination_path

            # Display preview or info based on file type
            if self.is_image_file(self.current_file):
                try:
                    self.show_file_preview(self.current_file, final_destination_path)
                except UnidentifiedImageError:
                    self.show_basic_file_info()
            else:
                self.show_basic_file_info()
        else:
            # No conflict: move the file and continue
            self.move_file(self.current_file, final_destination_path)
            self.root.after(100, self.process_next_file)  # Delay to avoid recursive call

    def rename_file(self):
        # Modify filename to add a '1' at the end
        base, ext = os.path.splitext(os.path.basename(self.conflict_file_path))
        counter = 1
        new_name = base + str(counter) + ext
        destination_folder_path = os.path.dirname(self.conflict_file_path)

        # Generate a new name that does not conflict
        while os.path.exists(os.path.join(destination_folder_path, new_name)):
            counter += 1
            new_name = base + str(counter) + ext

        new_destination_path = os.path.join(destination_folder_path, new_name)

        self.move_file(self.current_file, new_destination_path)
        self.skip_button.config(state=tk.DISABLED)
        self.rename_button.config(state=tk.DISABLED)
        self.root.after(100, self.process_next_file)  # Delay to avoid recursive call

    def skip_file(self):
        # Simply skip the current file and move on
        self.skip_button.config(state=tk.DISABLED)
        self.rename_button.config(state=tk.DISABLED)
        self.root.after(100, self.process_next_file)  # Delay to avoid recursive call

    @staticmethod
    def is_image_file(file_path):
        return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))

    def show_file_preview(self, source_path, destination_path):
        # Display source file preview
        img = Image.open(source_path)
        img.thumbnail((200, 200))
        self.source_image = ImageTk.PhotoImage(img)
        self.source_image_label.config(image=self.source_image)

        # Display destination (conflict) file preview
        conflict_img = Image.open(destination_path)
        conflict_img.thumbnail((200, 200))
        self.destination_image = ImageTk.PhotoImage(conflict_img)
        self.destination_image_label.config(image=self.destination_image)

        # Show file information
        file_size = os.path.getsize(source_path) / (1024 * 1024)  # size in MB
        self.file_info.config(text="File Name: {}\nSize: {:.2f} MB".format(os.path.basename(source_path), file_size))

    def show_basic_file_info(self):
        # Display file name and size without previews
        file_size = os.path.getsize(self.current_file) / (1024 * 1024)  # size in MB
        conflict_size = os.path.getsize(self.conflict_file_path) / (1024 * 1024)  # conflict file size in MB
        self.file_info.config(text="Conflict: {}\nSize: {:.2f} MB vs. {:.2f} MB".format(
            os.path.basename(self.current_file), file_size, conflict_size
        ))
        self.source_image_label.config(image='')
        self.destination_image_label.config(image='')

    @staticmethod
    def move_file(source, destination):
        shutil.move(source, destination)


if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()
