# GitDelver

*GitDelver* is a Python tool for analyzing Git repositories in bulk and generating various datasets for research purposes. It processes all commits, modified files and modified methods, performs a set of analyses and then produces several datasets (CSV files).

#### About the paper

*GitDelver* has been developed for the needs of the following paper:

*Riquet, N., Devroey, X., & Vanderose, B. (2022, May). GitDelver Enterprise Dataset (GDED): An Industrial Closed-source Dataset for Socio-Technical Research. In 19th International Conference on Mining Software Repositories (MSR'22), May 23-24, 2022, Pittsburgh, PA, USA. ACM Press.*


## Generated datasets

*GitDelver* produces the following datasets *for each processed repository*. In nominal cases, three datasets are generated for each repository. A fourth dataset may be generated on the rare occasion that a supported file could not be analyzed (this occurs for some obfuscated / uglified JavaScript files).

### commits_history

*commits_history* has the following columns:

* Repository: the name of the repository.
* Branches: the list of branches in which this modification has been integrated (works best if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated (works best if you target a bare repository).
* CommitId: the identifier of the commit.
* Message: the message of the commit.
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.
* Merge: flag telling if the commit is a merge commit.
* BugFix: flag telling if the modification is a bugfix.
* SATD: flag telling if the modification contains Self-Admitted Technical Debt.
* NbModifiedFiles: the total number of files (supported and unsupported) modified by this commit.
* ModifiedFiles: the list of files modified by this commit.
* NbModifiedProdSourceFiles: the number of production source files modified by this commit.
* NbModifiedTestSourceFiles: the number of test source files modified by this commit.
* NbModifications: the total number of modifications done by this commit.
* NbInsertions: the number of insertions done by the commit.
* NbDeletions: the number of deletions done by the commit.

### files_history

*files_history* has the following columns:

* Repository: the name of the repository.
* Branches: the list of branches in which this modification has been integrated (works best if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated (works best if you target a bare repository).
* OldFilePath: the old relative path to the file.
* FilePath: the relative path to the file.
* FileName: the name of the file.
* FileExtension: the file extension.
* FileType: the type of the file ("Production" or "Test").
* ChangeType: the type of the change ("ADD", "COPY", "RENAME", "DELETE", "MODIFY" or "UNKNOWN").
* NbMethods: the number of methods in the file.
* NbMethodsChanged: the number of methods that have been modified in this file for this commit.
* NLOC: the number of lines of code of the file.
* Complexity: the Weighted Methods per Class complexity, i.e., the sum of the cyclomatic complexity numbers of all the methods of the file.
* NlocDivByNbMethods: the number of lines of code of the file divided by the number of methods of the file.
* ComplexDivByNbMethods: the complexity of the file divided by the number of methods of the file.
* SATD: flag telling if the modification contains Self-Admitted Technical Debt.
* SATDLine: the line that triggered the SATD flag.
* NbLinesAdded: the number of lines added.
* NbLinesDeleted: the number of lines deleted.
* CommitId: the identifier of the commit.
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.

### methods_history

This dataset is produced if the 'analysis_mode' config parameter is set to AnalysisMode.COMMITS_FILES_METHODS.

*methods_history* has the following columns:

* Repository: the name of the repository.
* Branches: the list of branches in which this modification has been integrated (works best if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated (works best if you target a bare repository).
* OldFilePath: the old relative path to the file.
* FilePath: the relative path to the file.
* FileName: the name of the file.
* FileType: the type of the file ("Production" or "Test").
* MethodName: the name of the method.
* NbParams: the number of parameters in the method signature.
* NLOC: the number of lines of code of the method.
* Complexity: the cyclomatic complexity number of the method.
* CommitId: the identifier of the commit.
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.

### analysis_errors (this is generated only in the case of rare analysis errors)

A fourth dataset may be generated on the rare occasion that a supported file could not be analyzed (this occurs for some obfuscated / uglified JavaScript files).

*analysis_errors* has the following columns:

* Repository: the name of the repository.
* SkippedModificationFilePath: the relative path to the file that could not be analyzed.
* SkippedModificationFileName: the name of the file that could not be analyzed.
* CommitId: the identifier of the commit.

## Requirements

**GitDelver** requires that the following software be installed in your environment:

* Python 3.6+.
* PyDriller 2.0+ (use pip or conda to install it).
* Pandas 1.2+ (use pip or conda to install it).

## License

Copyright (c) 2021 Nicolas Riquet.

*GitDelver* is open source software and is distributed under the Apache license, version 2.0. Contributions are welcome!

## Usage

*GitDelver* can be used for either analyzing a single repository or multiple repositories in bulk. Please note that it is required that you first **set a few configuration parameters (mainly folder paths) in the *config.py* file** before launching the application (further information is provided below and in the configuration file itself). To run the **GitDelver** console program, simply launch a terminal, go to your local **GitDelver** folder and run the command *python gitdelver.py*.

## Configuration parameters to be set in *config.py*

* repo_path: file system path to either a single Git repository to be analyzed or a folder containing multiple repositories to be processed in bulk. In the latter case, each subfolder is assumed to be a regular directory containing a .git folder. Example of structure for bulk analysis:
  * repositories_folder_path/repo 1/(.git + code files)
  * repositories_folder_path/repo N/(.git + code files)  
* csv_output_folder_path: file system path to the folder where the generated CSV files are to be created.
* keep_unsupported_files: *GitDelver* uses some advanced features of PyDriller that are only available for supported file types (i.e. most common source code files). Set this option to True if you want *GitDelver* to report unsupported files as well.
* analysis_mode: GitDelver supports two modes of analysis.
    * AnalysisMode.COMMITS_FILES: produces the 'commits_history' and 'files_history' datasets. This is the default mode
    * AnalysisMode.COMMITS_FILES_METHODS: produces the 'commits_history', 'files_history' and the 'methods_history' datasets. This mode takes more time.
* nb_processes: *GitDelver* uses Python multiprocessing for analyzing multiple repositories at once. Nowadays, most computers have at least 4 virtual CPUs, so this is the default value. You can set it to less or more in function of your needs. *GitDelver* will check that the entered value is correct and will limit this parameter to the maximum number of available vitrtual CPUs.
* nb_commits_before_checkpoint: this parameter tells the *GitDelver* to write the current results to disk and free up memory once a certain amount of commits have been processed. The tool will resume its analyses afterwards and will continue writing to disk each time this amount of new commits has been processed. If the parameter is set to 0 no writing to disk will occur until all commits have been processed. The default value is 50 commits.
* verbose: this parameter sets the volume of feedback information provided by *GitDelver*. The analysis operation can take dozens of minutes for big repositories, so it is advised to set this to True in order to monitor its progression.
* SATD_keywords: this parameter configures the keywords that should be used to detect Self-Admitted Technical Debt in the lines of code.
* bugfix_keywords: this parameter configures the keywords that should be used to detect bug fixes in commit messages.

## Acknowledgements

*GitDelver* uses the *PyDriller*, *Lizard* and *Pandas* tools under the hood. The author would like to thank the people who contributed to these projects.