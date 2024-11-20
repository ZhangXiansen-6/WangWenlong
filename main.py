# -*- coding: utf-8 -*-

import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import time

# List to store known virus file MD5 values
md5list = []
# List to store found virus file names
fnameList = []
# Record total scanned files count
file_num = 0


# Read the content of the configuration file
def read_md5_list():
    global md5list
    try:
        with open('md5v.ini') as file:
            md5list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", "MD5 configuration file not found")
        exit()


# Traverse files in the directory and subdirectories
def scan_files(path):
    global fnameList, file_num
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_num += 1
            tmp_filename = os.path.join(dirpath, filename)
            try:
                with open(tmp_filename, 'rb') as fp:
                    data = fp.read()
                    file_md5 = hashlib.md5(data).hexdigest()
                    if file_md5 in md5list:
                        fnameList.append(tmp_filename)
            except Exception as e:
                print(f"Error scanning file {tmp_filename}: {e}")


# Execute the scan
def perform_scan():
    path = app.path_entry.get()
    if not path:
        messagebox.showerror("Error", "Please select a path")
        return

    global fnameList, file_num
    fnameList.clear()
    file_num = 0

    read_md5_list()

    start_time = time.time()
    scan_files(path)
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    results = (
            f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n"
            f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n"
            f"Total Files Scanned: {file_num}\n"
            f"Matched Files: {len(fnameList)}\n"
            "Matched Files:\n" +
            "\n".join(fnameList) +
            f"\nElapsed Time: {elapsed_minutes} min {elapsed_seconds} sec"
    )

    app.results_label.config(text=results)


class VirusScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Scanner")

        self.path_label = tk.Label(root, text="Scan Path:")
        self.path_label.pack()
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack()
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        self.scan_button = tk.Button(root, text="Start Scan", command=perform_scan)
        self.scan_button.pack()

        self.results_label = tk.Label(root, text="", justify=tk.LEFT)
        self.results_label.pack()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:  # Ensure a folder is selected
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirusScannerGUI(root)
    root.mainloop()