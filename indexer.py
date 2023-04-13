import os


def index_files(target_dir):
    indexed_files = []
    indexed_dirs = []

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            indexed_files.append(os.path.join(root, file))

        for cur_dir in dirs:
            indexed_dirs.append(os.path.join(root, cur_dir))

    # Save to file
    with open("indexed_files.txt", "w") as f:
        for file in indexed_files:
            f.write(file + "\n")

    with open("indexed_dirs.txt", "w") as f:
        for dir in indexed_dirs:
            f.write(dir + "\n")

    return indexed_files, indexed_dirs
