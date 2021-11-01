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
    
    def __init__(self, repository_path: str, csv_output_folder_path: str = "", keep_unsupported_files: bool = False,
                 analysis_mode = utilities.AnalysisMode.COMMITS_FILES, nb_commits_before_checkpoint: int = 50,
                 log: Callable[[str], None] = None, verbose: bool = True):
        """
        Constructor.
        
        Takes the path to the repository to be analyzed, the path where the CSV files are to be generated,
        a boolean telling if unsupported files should be reported, an analysis mode,
        a logging function for reporting feedback, and a boolean telling if verbose mode should be used.
        """

        self.repository_path = repository_path
                
        try:
            self.repository_name = Path(self.repository_path).parts[-1]
            self.repository = Repository(path_to_repo=repository_path, num_workers = 1)
        except Exception as ex:
            utilities._handle_error(ex)
        
        self.csv_output_folder_path = csv_output_folder_path        
        self.keep_unsupported_files = keep_unsupported_files        
        self.analysis_mode = analysis_mode        
        self.nb_commits_before_checkpoint = nb_commits_before_checkpoint        
        self.log = log        
        self.verbose = verbose
        
        self._commits_processed = 0
        self._is_first_write = True
        
    
    def run(self) -> List[DataSet]:
        """
        Main method of GitDelver. It traverses all the repository commits, files and methods, and returns a list of datasets
        caontained in Pandas dataframes.
        """
        
        # Preparation of the datasets.
        commits_columns = ["Repository", "Branches", "NbBranches", "CommitId", "Message", "Author", "DateTime", "Date", "HourOfDay",
                           "Merge", "BugFix", "SATD", "NbModifiedFiles", "ModifiedFiles", "NbModifiedProdSourceFiles",
                           "NbModifiedTestSourceFiles", "NbModifications", "NbInsertions", "NbDeletions"]
        
        files_columns = ["Repository", "Branches", "NbBranches", "OldFilePath", "FilePath", "FileName", "FileExtension", "FileType", 
                         "ChangeType", "NbMethods", "NbMethodsChanged", "NLOC", "Complexity", "NlocDivByNbMethods", 
                         "ComplexDivByNbMethods", "SATD", "SATDLine", "NbLinesAdded","NbLinesDeleted", "CommitId", "Author", "DateTime", 
                         "Date", "HourOfDay"]
        
        methods_columns = ["Repository", "Branches", "NbBranches", "OldFilePath", "FilePath", "FileName", "FileType", "MethodName", "NbParams", "NLOC", 
                           "Complexity", "CommitId", "Author","DateTime", "Date", "HourOfDay"]
        
        analysis_errors_columns = ["Repository", "SkippedModificationFilePath", "SkippedModificationFileName", "CommitId"]
        
        commits_rows = []
        files_rows = []
        methods_rows = []
        analysis_errors_rows = []
        
        SATD_keywords = config_params["SATD_keywords"]
        bugfix_keywords = config_params["bugfix_keywords"]
        
        if self.log is not None:        
            start_time = datetime.now()
            self.log("Starting delving into {}. This operation may take several minutes/hours depending on the size of the repository...".format(self.repository_name.upper()))

        # Process all the commits contained in the repository.
        for commit in self.repository.traverse_commits():
            
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
                    change_type = utilities.change_type_as_string(file.change_type)                
                    file_type = utilities.get_file_type(file.filename)
                    
                    # Determine the type of the file.
                    if (file_type == "Production"):
                        commit_nb_prod_files += 1
                        
                    elif (file_type == "Test"):
                        commit_nb_test_files += 1
                    
                    # Determine if there is self-admitted technical debt.
                    file_contains_SATD, SATDLine = utilities.is_SATD(SATD_keywords, file.diff_parsed)
                    commit_contains_SATD = file_contains_SATD
                    
                    # Create the methods dataset (process all the methods contained in the file).
                    try:
                        file_methods = file.methods
                        nb_methods = len(file_methods)
                        
                        file_changed_methods = file.changed_methods
                    except:
                        # RecursionError bug in Lizard library for some (obfuscated / uglified) JavaScript files => skip the files entirely and
                        # add them to the dataset of errors.
                        analysis_errors_rows.append((self.repository_name, file.old_path, file.filename, commit.hash))
                        self.log("!!! Impossible to analyze the methods of file '{}' in commit {} from {}.Skipping file modification altogether...".format(file.filename, 
                                                                                                                                                  commit.hash, self.repository_name.upper()))
                        continue
                    
                    # Calculate derived metrics based on NLOC/Complexity and the number of methods.
                    try:                    
                        nloc_div_by_nb_methods = round(file.nloc / nb_methods, 2)
                        complex_div_by_nb_methods = round(file.complexity / nb_methods, 2)
                    except:
                        nloc_div_by_nb_methods = 0.00
                        complex_div_by_nb_methods = 0.00
                    
                    if (self.analysis_mode == utilities.AnalysisMode.COMMITS_FILES_METHODS):
                        for method in file_methods:
                            # Appends the data to the method dataset.
                            methods_rows.append((self.repository_name, branches, nb_branches, file.old_path, file.new_path, method.filename, file_type,
                                                 utilities.short_method_name(method.name), len(method.parameters), method.nloc,
                                                 method.complexity, commit.hash, commit.author.name, commit.author_date, commit_date,
                                                 commit_hour_of_day))
                    
                    # Appends the data to the file dataset.
                    files_rows.append((self.repository_name, branches, nb_branches, file.old_path, file.new_path, file.filename, file_extension, file_type, change_type,
                                       nb_methods, len(file_changed_methods), file.nloc, file.complexity, nloc_div_by_nb_methods, complex_div_by_nb_methods, 
                                       file_contains_SATD, SATDLine, file.added_lines, file.deleted_lines, commit.hash, commit.author.name, commit.author_date, 
                                       commit_date, commit_hour_of_day))
            
            # Appends the data to the commit dataset.
            commits_rows.append((self.repository_name, branches, nb_branches, commit.hash, commit.msg, commit.author.name, commit.author_date,
                                 commit_date, commit_hour_of_day, commit.merge, commit_is_bugfix, commit_contains_SATD, commit.files,
                                 "\n".join(list_of_file_names), commit_nb_prod_files, commit_nb_test_files, commit.lines,
                                 commit.insertions, commit.deletions))
            
            if (self._commits_processed > 0 and self.nb_commits_before_checkpoint > 0 and self._commits_processed % self.nb_commits_before_checkpoint == 0): 
                # Generate intermediary datasets.
                self._generate_dataset(commits_rows, commits_columns,
                               files_rows, files_columns,
                               methods_rows, methods_columns,
                               analysis_errors_rows, analysis_errors_columns)
                
                # Reset rows lists to free up memory.
                commits_rows = []
                files_rows = []
                methods_rows = []
                analysis_errors_rows = []
                
                saved_to_disk_message = "Reached checkpoint and saved current data to disk. "
            else: saved_to_disk_message = ""
            
            # Prints progression messages if verbose mode is set.
            if (self._commits_processed > 0  and self._commits_processed % 10 == 0 and self.log is not None and self.verbose):
                self.log("Processed {} commits from {}. {}Continuing...".format(self._commits_processed, self.repository_name.upper(), saved_to_disk_message), True)
            
            
            self._commits_processed += 1  
        
        
        # Generate the full final datasets.
        datasets = self._generate_dataset(commits_rows, commits_columns,
                               files_rows, files_columns,
                               methods_rows, methods_columns,
                               analysis_errors_rows, analysis_errors_columns)
        
        if self.log is not None:
            end_time = datetime.now()
            self.log("Analysis of {} complete. Processed {} commits in {}.".format(self.repository_name.upper(), self._commits_processed, end_time - start_time))
        
        
        if self.nb_commits_before_checkpoint == 0:
            # Useful only when nb_commits_before_checkpoint = 0. Mainly used for unit tests.
            return datasets
    
    
    def _build_datasets_objects(self, commits_rows: List, commits_columns: List,
                                   files_rows: List, files_columns: List,
                                   methods_rows: List, methods_columns: List,
                                   analysis_errors_rows: List, analysis_errors_columns: List) -> List[DataSet]:
        """
        Builds the datasets collection. This method returns a list of datasets contained in Pandas dataframes.

        """
        
        datasets = [DataSet("commits_history", pd.DataFrame(commits_rows, columns=commits_columns))]
        
        datasets.append(DataSet("files_history", pd.DataFrame(files_rows, columns=files_columns)))
        
        if (self.analysis_mode == utilities.AnalysisMode.COMMITS_FILES_METHODS):
            datasets.append(DataSet("methods_history", pd.DataFrame(methods_rows, columns=methods_columns)))
        
        # Add the the dataset of errors if there were analysis problems. 
        if len(analysis_errors_rows) > 0:
            datasets.append(DataSet("analysis_errors", pd.DataFrame(analysis_errors_rows, columns=analysis_errors_columns)))
        
        return datasets
    
    
    def _produce_csv(self, datasets: List[DataSet]):
        """
        Generates CSV files from the Pandas datasets. 
        Side effect: CSV files are written in csv_output_folder_path.
        """
        
        for dataset in datasets:
            
            path = str(Path(self.csv_output_folder_path).joinpath("{}_{}.csv".format(self.repository_name, dataset.name)))
            
            if (self.nb_commits_before_checkpoint > 0 and not self._is_first_write):
                # This is an intermediary write. Append to the file.
                
                if (self._is_first_write and Path(path).exists()):
                    utilities._handle_error("File \"{}\" already exists. Aborting to avoid appending data to it...".format(path))
                
                try:
                    dataset.dataframe.to_csv(path, mode='a', header=False, index=False)
                except Exception as ex:
                    utilities._handle_error(ex)
            else:
                # This is the first write.
                try:
                    dataset.dataframe.to_csv(path, index=False)
                    
                    self._is_first_write = False
                    
                except Exception as ex:
                    utilities._handle_error(ex)
        
    
    
    def _generate_dataset(self, commits_rows: List, commits_columns: List,
                                   files_rows: List, files_columns: List,
                                   methods_rows: List, methods_columns: List,
                                   analysis_errors_rows: List, analysis_errors_columns: List):
        """
        This method combines the generation of the dataset objects and the production of the CSV files.

        """
        
        # Build the datasets collection.
        datasets = self._build_datasets_objects(commits_rows, commits_columns,
                                                   files_rows, files_columns,
                                                   methods_rows, methods_columns,
                                                   analysis_errors_rows, analysis_errors_columns)
        
        
        self._produce_csv(datasets)
        
        
        if self.nb_commits_before_checkpoint == 0:
            # Useful only when nb_commits_before_checkpoint = 0. Mainly used for unit tests.
            return datasets
        