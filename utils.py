import os
import sys


def sys_exit(message: str):
    sys.exit(message)


def check_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        message = ' '.join(['Path does not exist:', dir_path])
        sys_exit(message)
    return True


def check_file(file_path: str):
    if not os.path.isfile(file_path):
        message = ' '.join(['Path does not exist:', file_path])
        sys_exit(message)


def create_dir(dir_path: str):
    if not os.path.isfile(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            description = ['Creation of the directory', 'failed']
            message = ' '.join([description[0], dir_path, description[1]])
            sys_exit(message)
        else:
            description = 'Successfully created the directory'
            message = ' '.join([description, dir_path])
            print(message)
    else:
        description = 'Directory already exists'
        message = ' '.join([description, message])
        print(message)
