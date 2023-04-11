import os


def index_files(target_dir):
    indexed_files = []
    indexed_dirs = []

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            indexed_files.append(os.path.join(root, file))

        for cur_dir in dirs:
            indexed_dirs.append(os.path.join(root, cur_dir))

    return indexed_files, indexed_dirs
