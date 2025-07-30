# Copyright 2025 Ravetta Stefano
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
import shutil


# /---------------\
# |-- Directory --|
# \---------------/


def is_directory(directory):
    """
    Method that, given a path, returns True if it refers to a directory.

    :param directory: path of the directory
    :return: True if it is a directory, False otherwise
    """

    return os.path.isdir(directory)


def make_directory(directory):
    """
    Method that, given the path of the directory to create, creates it if it does not exist.

    :param directory: path of the directory to create
    """

    if not is_directory(directory):
        os.makedirs(directory)


def _copytree(src, dst, symlinks=False, ignore=None):
    """
    Private method that copies or links a directory and its contents, not ignored, to the specified destination.

    :param src: path of the folder to copy
    :param dst: destination path of the folder to copy
    :param symlinks: if True, files inside the directory are linked in the destination, otherwise they are copied
    :param ignore: files to ignore
    """

    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if exists(dst):
        if not is_directory(dst):
            return False
    else:
        os.makedirs(dst)

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                _copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported files types
                shutil.copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))

    try:
        shutil.copystat(src, dst)
    except OSError as why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying files access times may fail on Windows
            pass
        else:
            errors.append((src, dst, str(why)))

    if errors:
        raise shutil.Error(errors)


# /----------\
# |-- File --|
# \----------/


def copy(source, destination, *ignore):
    """
    Method that copies a file or a directory, and its contents, to the specified destination.
    When copying a directory, you can specify files to ignore.
    If the file already exists at the destination, it will be replaced.
    If the directory already exists at the destination, only matching files are replaced and extra files are not deleted.

    :param source: file or directory to copy
    :param destination: name of the copied file or directory
    :param ignore: rules to ignore files when copying inside a directory
    :return: True if everything went well, False otherwise
    """

    if is_file(source):
        shutil.copy(source, destination)
        return True
    elif is_directory(source):
        if ignore:
            _copytree(source, destination, ignore=shutil.ignore_patterns(*ignore))
        else:
            _copytree(source, destination)
        return True
    return False


def exists(location_file):
    """
    Method that, given the path of a file or directory, indicates whether it exists or not.

    :param location_file: path of the file or directory
    :return: True if it exists, False otherwise
    """

    return os.path.exists(location_file)


def is_file(location_file):
    """
    Method that, given a path, returns True if it refers to a file.

    :param location_file: path of the file
    :return: True if it is a file, False otherwise
    """

    return os.path.isfile(location_file)


def write(location_file, data, mode="w"):
    """
    Method that, given the path of a file, writes the passed string inside it.

    :param location_file: path of the file
    :param data: string to write
    :param mode: mode in which to write
    :return: True if everything went well, False otherwise
    """

    if not exists(location_file) or is_file(location_file):
        with open(location_file, mode) as _file:
            _file.write(data)
            _file.close()

        return True
    return False


# /----------\
# |-- Json --|
# \----------/


def json_encode(obj, encoder=None, indent=None) -> str:
    """
    Method to encode a python object in a json string.

    :param obj: python object to be encoded
    :param encoder:
    :param indent:
    :return: json string
    """
    return json.dumps(obj, cls=encoder, indent=indent)


def json_decode(_json):
    """
    Method to decode a json files or a json string in a python object.

    :param _json: json files or json string
    :return: python object
    """
    if not type(_json) is str:
        _json = json_encode(_json)

    if os.path.isfile(_json):
        with open(_json, "r") as _file:
            _data = json.load(_file)
            _file.close()
    else:
        _data = json.loads(_json)

    return _data


# /-----------\
# |-- Regex --|
# \-----------/


def regex_match(regex, value):
    return regex is None or re.match(regex, str(value)) is not None


def regex_not_match(regex, value):
    return not regex_match(regex, value)
