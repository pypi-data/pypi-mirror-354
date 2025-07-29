# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__version__ = "0.2.9"
__release__ = 20250609

from os.path import isfile, isdir

__all__ = ['extension', 'Filepath', 'get_folder', 'get_file', 'get_name', 'get_extension']


class Filepath(object):
    slots = ['folder', 'name', 'extension', 'file_path']
    def __init__(self, file_path: str):
        _temp = extension(file_path)
        self.file_path = _temp[3]
        self.folder = _temp[2]
        self.name = _temp[1]
        self.extension = _temp[0]

    def get_folder(self):
        return self.folder

    def get_file(self):
        return f'{self.name}{self.extension}'

    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    @property
    def ext(self):
        return self.extension


def extension(file_path: str, backslash_to_slash=True, back_compatibility=False):
    """
    receives a string indicating a FileName.Extension or
    Path/FileName.Extension and returns a tuple containing
    [0] the .Extension of the file in filepath,
    [1] the name of the FileName without extension_,
    [2] the Directory containing the file,
    [3] the fullpath

    in case an item is not present an empty string is returned by default.
    """

    file_path = file_path.strip()

    if bool(backslash_to_slash) is True:
        file_path = file_path.replace('\\', '/')

    if '/' in file_path:
        len_path = len(file_path) - file_path[::-1].index('/')
        path_ = file_path[:len_path]
    else:
        len_path = 0
        path_ = ''

    if '.' in file_path[len_path:]:
        file_name_ = file_path[len_path:len(file_path) - file_path[::-1].index('.') - 1]
        extension_ = file_path[len(file_path) - file_path[::-1].index('.') - 1:]
    else:
        file_name_ = file_path[len_path:]
        extension_ = ''

    fullpath_ = f"{path_}{file_name_}{extension_}".strip()
    if not isfile(fullpath_) and isdir(fullpath_):
        file_name_, extension_, path_= '', '', f"{path_}{file_name_}{extension_}"
        if not path_.endswith('/'):
            path_ += '/'

    if back_compatibility:
        return file_name_, extension_, path_, fullpath_
    else:
        return extension_, file_name_, path_, fullpath_

def get_folder(file_path: str) -> str:
    """
    receives a string indicating a FileName.Extension or
    Path/FileName.Extension and returns the folder where the file is located.
    """
    return extension(file_path)[2]

def get_file(file_path: str) -> str:
    """
    receives a string indicating a FileName.Extension or
    Path/FileName.Extension and returns the name of the file without extension.
    """
    full_path = extension(file_path)
    return f'{full_path[1]}{full_path[0]}'

def get_extension(file_path: str) -> str:
    """
    receives a string indicating a FileName.Extension or
    Path/FileName.Extension and returns the file extension.
    """
    return extension(file_path)[0]

def get_name(file_path: str) -> str:
    """
    receives a string indicating a FileName.Extension or
    Path/FileName.Extension and returns the name of the file without extension.
    """
    return extension(file_path)[1]
