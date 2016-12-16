import os


def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError('No file at location \'%s\'' % filepath)


def check_directory_exists(directorypath):
    if not os.path.isdir(directorypath):
        raise FileNotFoundError('No directory at location \'%s\'' % directorypath)
