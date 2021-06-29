# Copyright (c) 2021 Nicolas Riquet (MIT license)

"""
This module contains all utility functions used by GitDelver.
"""

import sys
from datetime import datetime
from typing import List, Dict, Tuple
import enum


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


def change_type_as_string(modification_type_enum_value: enum) -> str:
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