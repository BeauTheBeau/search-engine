import os
import fuzzywuzzy
from fuzzywuzzy import fuzz
from indexer import index_files

# GUI imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Global variables
indexed_files, indexed_dirs = [], []
root_dir = os.path.abspath(os.sep)
ignored_extensions = []
file_size_format = "bytes"

# Check for indexes and settings
if os.path.exists("indexed_files.txt") and os.path.exists("indexed_dirs.txt"):
    with open("indexed_files.txt", "r") as f:
        indexed_files = f.read().splitlines()

    with open("indexed_dirs.txt", "r") as f:
        indexed_dirs = f.read().splitlines()

    print("Loaded {} files and {} directories".format(len(indexed_files), len(indexed_dirs)))

if os.path.exists("settings.txt"):
    with open("settings.txt", "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.startswith("root_dir"):
                root_dir = line.split(" = ")[1]

            elif line.startswith("ignored_extensions"):
                ignored_extensions = line.split(" = ")[1]

            elif line.startswith("file_size_format"):
                file_size_format = line.split(" = ")[1]

    print("Loaded settings")
else:
    # Save default settings
    with open("settings.txt", "w") as f:
        f.write("root_dir = " + root_dir + "\n")
        f.write("ignored_extensions = " + str(ignored_extensions) + "\n")
        f.write("file_size_format = " + file_size_format + "\n")


def index():
    global indexed_files, indexed_dirs
    indexed_files, indexed_dirs = index_files(root_dir)
    print("Indexed {} files and {} directories".format(len(indexed_files), len(indexed_dirs)))
    return indexed_files, indexed_dirs


def search_files(query, files):
    results = []
    for file in files:

        file_name = os.path.basename(file)

        if fuzzywuzzy.fuzz.ratio(query, file_name) > 70:
            results.append(file)
    return results


def search_dirs(query, dirs):
    results = []
    for dir in dirs:

        dir_name = os.path.basename(dir)

        if fuzzywuzzy.fuzz.ratio(query, dir_name) > 70:
            results.append(dir)
    return results


# Main GUI
class MainGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("File Searcher")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        self.search_var = StringVar()
        self.search_var.trace("w", self.search)

        self.search_entry = ttk.Entry(self.master, textvariable=self.search_var)
        self.search_entry.pack(fill=X, padx=10, pady=10)

        self.results = ttk.Treeview(self.master, columns=("size", "path"))
        self.results.heading("#0", text="Name")
        self.results.heading("size", text="Size")
        self.results.heading("path", text="Path")
        self.results.column("#0", width=200)
        self.results.column("size", width=100)
        self.results.column("path", width=300)
        self.results.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.results.bind("<Double-1>", self.open_file)

    def search(self, *args):
        query = self.search_var.get()
        files = search_files(query, indexed_files)
        dirs = search_dirs(query, indexed_dirs)

        self.results.delete(*self.results.get_children())

        for file in files:
            file_name = os.path.basename(file)
            file_size = os.path.getsize(file)
            file_path = os.path.dirname(file)

            if file_size_format == "bytes":
                file_size = str(file_size) + " bytes"
            elif file_size_format == "kb":
                file_size = str(file_size / 1024) + " KB"
            elif file_size_format == "mb":
                file_size = str(file_size / 1024 / 1024) + " MB"
            elif file_size_format == "gb":
                file_size = str(file_size / 1024 / 1024 / 1024) + " GB"

            self.results.insert("", "end", text=file_name, values=(file_size, file_path))

        for dir in dirs:
            dir_name = os.path.basename(dir)
            dir_path = os.path.dirname(dir)

            self.results.insert("", "end", text=dir_name, values=("", dir_path))

    def open_file(self, event):
        item = self.results.selection()[0]
        path = self.results.item(item, "values")[1]
        os.startfile(path)


if __name__ == "__main__":
    root = Tk()
    MainGUI(root)
    root.mainloop()
