#    Copyright 2021 Nicolas Riquet
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
This module contains the configuration parameters used when GitDelver is launched.
"""

from utilities import AnalysisMode

config_params = {
    # File system path to either a single Git repository to be analyzed or a folder
    # containing multiple repositories to be processed in bulk. In the latter case, 
    # each subfolder is assumed to be a regular directory containing a .git folder.
    # Example of structure for bulk analysis:
    # repositories_folder_path/repo 1/(.git + code files, or bare repo content)
    # repositories_folder_path/repo N/(.git + code files, or bare repo content)
    "repo_path": r"ENTER FILE SYSTEM PATH HERE",
    
    # File system path to the folder where the generated CSV files are to be created.
    "csv_output_folder_path": r"ENTER FILE SYSTEM PATH HERE",
    
    # GitDelver uses some advanced features of PyDriller that are only available for
    # supported file types (i.e. most common source code files).
    # Set this option to True if you want GitDelver to report unsupported files as well.
    "keep_unsupported_files": False,
    
    # GitDelver supports three modes of analysis:
    # AnalysisMode.COMMITS_FILES: produces the 'commits_history' and 'files_history' datasets. Warning: columns related to methods will not be calculated.
    # AnalysisMode.COMMITS_FILES_METHODS: produces the 'commits_history', 'files_history' and the 'methods_history' datasets. This is the default mode but it takes more time.
    "analysis_mode": AnalysisMode.COMMITS_FILES,
    
    # GitDelver uses Python multiprocessing for analyzing multiple repositories at once.
    # Nowadays, most computers have at least 4 virtual CPUs, so this is the default value.
    # You can set it to less or more in function of your needs. GitDelver will check that
    # the entered value is correct and will limit this parameter to the maximum number of
    # available vitrtual CPUs.
    "nb_processes": 4,
    
    
    # This parameter tells the GitDelver to write the current results to disk and free up memory once a certain amount
    # of commits have been processed. The tool will resume its analyses afterwards and will 
    # continue writing to disk each time this amount of new commits has been processed. If the parameter
    # is set to 0 no writing to disk will occur until all commits have been processed.
    # The default value is 50 commits.
    "nb_commits_before_checkpoint": 50,
    
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
