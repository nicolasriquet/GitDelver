# MIT License
#
# Copyright (c) 2021 Nicolas Riquet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module contains all utility types and functions used by GitDelver.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from enum import Enum

class AnalysisMode(Enum):
    """
    Used to set the mode of the analysis: commits only, commits and files, commits and files and methods.
    """
    COMMITS = 1
    COMMITS_FILES = 2
    COMMITS_FILES_METHODS = 3


def get_file_type(file_name: str) -> str:
    """
    Returns "test" if file_name contains the string "test" else returns "Production".
    """

    result = "Production"
    
    if ("test" in file_name or "Test" in file_name):
        return "Test"

    return result


def keyword_match_found(keywords_list: List[str], string: str) -> bool:
    """
    Returns True if one of the words in keywords_list is present in string else returns False.
    """

    for word in keywords_list:
        if word in string.lower().replace(" ", ""): return True
    
    return False


def is_bugfix(bugfix_keywords: List[str], message: str) -> bool:
    """
    Returns True if one of the words in bugfix_keywords is present in message else returns False.
    """

    return keyword_match_found(bugfix_keywords, message)


def is_SATD(SATD_keywords: List[str], dict_of_modified_lines: Dict[str, List[tuple]]) -> Tuple[bool, str]:
    """
    Returns True if one of the words in SATD_keywords is present in the dict_of_modified_lines value structure (list of tuples)
    else returns False.
    """

    for key, value in dict_of_modified_lines.items():
        for line_tuple in value:
            match_found = keyword_match_found(SATD_keywords, line_tuple[1])
            
            if (key == "added" and match_found):
                return True, line_tuple[1]
    
    return False, ""


def change_type_as_string(modification_type_enum_value: Enum) -> str:
    """
    Returns a string representing the value of PyDriller's ModificationType enum. 
    PyDriller does not make this enum publicly available to the outside world.
    """
    
    change_type = ""
    
    if (str(modification_type_enum_value) == "ModificationType.ADD"):
        change_type = "ADD"
    elif (str(modification_type_enum_value) == "ModificationType.COPY"):
        change_type = "COPY"
    elif (str(modification_type_enum_value) == "ModificationType.RENAME"):
        change_type = "RENAME"
    elif (str(modification_type_enum_value) == "ModificationType.DELETE"):
        change_type = "DELETE"
    elif (str(modification_type_enum_value) == "ModificationType.MODIFY"):
        change_type = "MODIFY"
    elif (str(modification_type_enum_value) == "ModificationType.UNKNOWN"):
        change_type = "UNKNOWN"
    
    return change_type


def short_method_name(method_name: str) -> str:
    """
    This function takes a long method name like "class_name::method_name" and return the short method
    name without the class prefix and the "::" separator.
    """
    
    if "::" not in method_name:
        return method_name
    
    return method_name.split("::",1)[1] 


def is_single_repository(repo_path: str) -> bool:
    """
    This function returns True if repo_path points to a single repository (regular or bare) rather than a
    folder containing multiple repositories.
    """
    
    # For regular repositories
    if Path("{}/.git".format(repo_path)).exists():
        return True
    
    # For bare repositories
    if (Path("{}/hooks".format(repo_path)).exists() and
        Path("{}/refs".format(repo_path)).exists()):
        return True
    
    return False


def _log(message: str, verbose_info: bool = False, is_exception: bool = False):
    """
    Prints message on stdout with special formatting for verbose mode information and exceptions.
    Side effect: messages are displayed on the console.
    """
    
    if (is_exception):
        print("The following error occurred: {}".format(message))
    else:
        prefix = "        " if verbose_info else ""
        print("{}{}: {}".format(prefix, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))


def _handle_error(message: str):
    """
    Handles exceptions and reports exception message.
    Side effects: messages are displayed on the console and the program is terminated.
    """

    _log(message, False, True)
    sys.exit(1)