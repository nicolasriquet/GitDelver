# Copyright (c) 2021 Nicolas Riquet (MIT license)

"""
This module contains the configuration parameters used when GitDelver is launched.
"""

config_params = {
    # File system path (using regular forward slashes) to either a single Git repository to be analyzed or a folder
    # containing multiple repositories to be processed in bulk. In the latter case, 
    # each subfolder is assumed to be a regular directory containing a .git folder.
    # Example of structure for bulk analysis:
    # repositories_folder_path/repo 1/(.git + code files)
    # repositories_folder_path/repo N/(.git + code files)
    "repo_path": "ENTER FILE SYSTEM PATH HERE",
    
    # File system path (using regular forward slashes) to the folder where the generated CSV files are to be created.
    "csv_output_folder_path": "ENTER FILE SYSTEM PATH HERE",
    
    # GitDelver uses some advanced features of PyDriller that are only available for
    # supported file types (i.e. most common source code files).
    # Set this option to True if you want GitDelver to report unsupported files as well.
    "keep_unsupported_files": False,
    
    # GitDelver uses Python multiprocessing for analyzing multiple repositories at once.
    # Nowadays, most computers have at least 4 virtual CPUs, so this is the default value.
    # You can set it to less or more in function of your needs. GitDelver will check that
    # the entered value is correct and will limit this parameter to the maximum number of
    # available vitrtual CPUs.
    "nb_processes": 4,
    
    # This parameter sets the volume of feedback information provided by GitDelver. The analysis
    # operation can take dozens of minutes for big repositories, so it is advised to set
    # this to True in order to monitor its progression.
    "verbose": True,
    
    # This parameter configures the keywords that should be used to detect Self-Admitted Technical Debt in
    # the lines of code.
    "SATD_keywords": ["//todo", "#todo", "//fixme", "#fixme", "//tofix", "#tofix",
                     "//hack", "#hack", "//workaround", "#workaround"],
    
    # This parameter configures the keywords that should be used to detect bug fixes in commit messages.
    "bugfix_keywords": ["fix", "solve", "bug", "defect", "problem"]
    }