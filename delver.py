# Copyright (c) 2021 Nicolas Riquet (MIT license)

"""
This module contains the delver itself . This is where all the main processing takes place.
Please note that GitDelver heavily uses the PyDriller open source mining library (https://github.com/ishepard/pydriller).
GitDelver basically uses PyDriller to traverse all the repository commits, files and methods and then produces various datasets
for further analysis in Jupyter notebooks.

The delver is designed to be called either by the GitDelver console program or directly from any other module using Pandas dataframes
(e.g., Jupyer notebooks).
"""

import utilities
from config import config_params
from pydriller import Repository 
import pandas as pd
from pathlib import Path
from collections import namedtuple
from datetime import datetime
from typing import Callable, List

# Named tuple for storing the produced datasets. It has two attributes :
# the name of the dataset and a Pandas dataframe.
DataSet = namedtuple("DataSet", ["name", "dataframe"])


class Delver:
    """
    Main class of GitDelver. It does all the repository history processing.
    """
    
    def __init__(self, repository_path: str, csv_output_folder_path: str = "", log: Callable[[str], None] = None, 
                 keep_unsupported_files: bool = False, verbose: bool = True):
        """
        Constructor.
        
        Takes the path to the repository to be analyzed, the path where the CSV files are to be generated,
        a logging function for reporting feedback, a boolean telling if unsupported files should be reported,
        and a boolean telling if verbose mode should be used.
        """

        self.repository_path = repository_path
                
        try:
            self.repository_name = Path(self.repository_path).parts[-1]
            self.repository = Repository(path_to_repo=repository_path, num_workers = 1)
        except Exception as ex:
            utilities._handle_error(ex)
        
        self.csv_output_folder_path = csv_output_folder_path
        
        self.log = log
        
        self.keep_unsupported_files = keep_unsupported_files
        self.verbose = verbose
        
        self._commits_processed = 0

    
    def delve(self) -> List[DataSet]:
        """
        Main method of GitDelver. It traverses all the repository commits, files and methods, and returns a list of datasets
        caontained in Pandas dataframes. The use of Pandas dataframes does not slow down the generation of CSV files by the
        GitDelver console application but it does increade the memory usage as the entire datasets are stored in memory before
        being written to files. The advantage of this implementation is that it supports the use case of people who want to
        directly analyze a single Git repository from their Jupyter notebooks and who do not wish to process several repositories
        in bulk with the GitDelver console application.
        """
        
        # Preparation of the datasets.
        commits_columns = ["Repository", "Branches", "NbBranches", "CommitId", "Message", "Author", "DateTime", "Date", "HourOfDay",
                           "Merge", "BugFix", "SATD", "NbModifiedFiles", "NbModProductionFiles", "NbModTestFiles", "ModifiedFiles", 
                           "NbModifications", "NbInsertions", "NbDeletions"]
        commits_rows = []        
        files_columns = ["Repository", "Branches", "NbBranches", "FilePath", "FileName", "FileExtension", "FileType", "ChangeType",
                         "NbMethods", "NbMethodsChanged", "NLOC", "CCN", "SATD", "SATDLine", "NbLinesAdded","NbLinesDeleted", "CommitId",
                         "Author", "DateTime", "Date", "HourOfDay"]        
        files_rows = []        
        methods_columns = ["Repository", "Branches", "NbBranches", "FilePath", "FileName", "FileType", "MethodName", "NbParams", "NLOC", 
                           "CCN", "CommitId", "Author","DateTime", "Date", "HourOfDay"]
        methods_rows = []
        
        SATD_keywords = config_params["SATD_keywords"]
        bugfix_keywords = config_params["bugfix_keywords"]

        # Process all the commits contained in the repository.
        for commit in self.repository.traverse_commits():
            
            self._commits_processed += 1
            
            # Prints progression messages if verbore mode is set.
            if (self.log is not None and self.verbose and self._commits_processed % 10 == 0):
                self.log("Processed {} commits from repository {}. Continuing...".format(self._commits_processed, self.repository_name.upper()), True)
            
            # Process the commit.
            branches = str(commit.branches)
            nb_branches = len(commit.branches)
            commit_date = commit.author_date.date()
            commit_hour_of_day = commit.author_date.time().hour
            
            list_of_file_names = []
            
            commit_nb_prod_files = 0
            commit_nb_test_files = 0
            
            commit_contains_SATD = False
            commit_is_bugfix = utilities.is_bugfix(bugfix_keywords, commit.msg)
            
            # Process all the files contained in the commit.
            for file in commit.modified_files:
                list_of_file_names.append(file.filename)
                
                file_extension = Path(file.filename).suffix
                
                if (self.keep_unsupported_files or file.language_supported):
                    if (file.new_path is not None):
                        file_path = file.new_path
                    else:
                        file_path = file.old_path
                                                    
                    change_type = utilities.change_type_as_string(file.change_type)                
                    file_type = utilities.get_file_type(file.filename)
                    
                    if (file_type == "Production"):
                        commit_nb_prod_files += 1
                    elif (file_type == "Test"):
                        commit_nb_test_files += 1
                    
                    file_contains_SATD, SATDLine = utilities.is_SATD(SATD_keywords, file.diff_parsed)
                    commit_contains_SATD = file_contains_SATD
                    
                    # Create the methods dataset (process all the methods contained in the file).
                    for method in file.methods:
                        methods_rows.append((self.repository_name, branches, nb_branches, file_path, method.filename, file_type, method.name,
                                            len(method.parameters), method.nloc, method.complexity,                                        
                                            commit.hash, commit.author.name, commit.author_date, commit_date,
                                            commit_hour_of_day))
                    
                    # Create the files dataset.
                    files_rows.append((self.repository_name, branches, nb_branches, file_path, file.filename, file_extension, file_type, change_type,
                                       len(file.methods), len(file.changed_methods), file.nloc,
                                       file.complexity, file_contains_SATD, SATDLine, file.added_lines, file.deleted_lines, commit.hash,
                                       commit.author.name, commit.author_date, commit_date, commit_hour_of_day))
            
            # Create the commits dataset.
            commits_rows.append((self.repository_name, branches, nb_branches, commit.hash, commit.msg, commit.author.name, commit.author_date,
                                 commit_date, commit_hour_of_day, commit.merge, commit_is_bugfix, commit_contains_SATD, commit.files,
                                 commit_nb_prod_files, commit_nb_test_files, "\n".join(list_of_file_names), commit.lines,
                                 commit.insertions, commit.deletions))
        
        # Build the datasets.
        datasets = [
            DataSet("commits_history", pd.DataFrame(commits_rows, columns=commits_columns)),
            DataSet("files_history", pd.DataFrame(files_rows, columns=files_columns)),
            DataSet("methods_history", pd.DataFrame(methods_rows, columns=methods_columns))
            ]
        
        return datasets
        
    
    def _produce_csv(self, datasets: List[DataSet]):
        """
        Generates CSV files from the Pandas datasets.
        Side effect: CSV files are written in csv_output_folder_path.
        """
    
        for dataset in datasets:
            path = str(Path(self.csv_output_folder_path).joinpath("{}_{}.csv".format(self.repository_name, dataset.name)))
            
            try:
                dataset.dataframe.to_csv(path, index=False)
            except Exception as ex:
                utilities._handle_error(ex)
    
    
    def run(self):
        """
        Combines the delving and CSV generating operations. This is mainly used by the GitDelver console application.
        """
        
        if self.log is not None:        
            start_time = datetime.now()
            self.log("Starting delving into repository {}. This operation may take several minutes...".format(self.repository_name.upper()))
        
        datasets = self.delve()
        
        self._produce_csv(datasets)
        
        if self.log is not None:
            end_time = datetime.now()
            self.log("Analysis of repository {} complete. Processed {} commits in {}".format(self.repository_name.upper(), self._commits_processed, end_time - start_time))