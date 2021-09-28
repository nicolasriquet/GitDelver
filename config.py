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
This module contains the configuration parameters used when GitDelver is launched.
"""

from utilities import AnalysisMode

config_params = {
    # File system path (using regular forward slashes, even on Windows so use C:/) 
    # to either a single Git repository to be analyzed or a folder
    # containing multiple repositories to be processed in bulk. In the latter case, 
    # each subfolder is assumed to be a regular directory containing a .git folder.
    # Example of structure for bulk analysis:
    # repositories_folder_path/repo 1/(.git + code files, or bare repo content)
    # repositories_folder_path/repo N/(.git + code files, or bare repo content)
    "repo_path": r"ENTER FILE SYSTEM PATH HERE",
    
    # File system path (using regular forward slashes, even on Windows so use C:/) 
    # to the folder where the generated CSV files are to be created.
    "csv_output_folder_path": r"ENTER FILE SYSTEM PATH HERE",
    
    # GitDelver uses some advanced features of PyDriller that are only available for
    # supported file types (i.e. most common source code files).
    # Set this option to True if you want GitDelver to report unsupported files as well.
    "keep_unsupported_files": False,
    
    # GitDelver supports three modes of analysis:
    # AnalysisMode.COMMITS: produces only the 'commits_history' dataset.
    # AnalysisMode.COMMITS_FILES: produces the 'commits_history' and 'files_history' datasets. CAN TAKE SOME TIME!
    # AnalysisMode. COMMITS_FILES_METHODS: produces the 'commits_history', 'files_history' and the 'methods_history' datasets. CAN TAKE A VERY LONG TIME!
    "analysis_mode": AnalysisMode.COMMITS_FILES,
    
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