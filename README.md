# GitDelver

Copyright (c) 2021 Nicolas Riquet

**GitDelver** is a Python tool for analyzing Git repositories in bulk and generating various datasets for research purposes. It basically analyzes all commits, modified files and modified methods, performs a set of analyses and then produces several CSV files containing all the generated data.

## Generated datasets

**GitDelver** produces the following datasets *for each processed repository* (i.e., 3 datasets are generated for each repository).

### commits_history

*commits_history* has the following columns:

* Repository: the name of the repository.
* Branches: the list of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* CommitId: the identifier of the commit.
* Message: message of the commit.
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.
* Merge: flag telling if the commit is a merge commit.
* BugFix: flag telling if the modification is a bugfix.
* SATD: flag telling if the modification contains Self-Admitted Technical Debt.
* NbModifiedFiles: the number of files modified by this commit.
* NbModProductionFiles: the number of production files modified by this commit.
* NbModTestFiles: the number of test files modified by this commit.
* ModifiedFiles: the list of files modified by this commit.
* NbModifications: the total number of modifications done by this commit.
* NbInsertions: the number of insertions done by the commit.
* NbDeletions: the number of deletions done by the commit.

### files_history

*files_history* has the following columns:

* Repository: the name of the repository
* Branches: the list of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* FilePath: the relative path to file.
* FileName: the name of the file.
* FileExtension: the file extension.
* FileType: the type of the file ("Production" or "Test")
* ChangeType: the type of change ("ADD", "COPY", "RENAME", "DELETE", "MODIFY" or "UNKNOWN")
* NbMethods: the number of methods in the file.
* NbMethodsChanged: the number of methods that have been modified in this file for this commit.
* NLOC: the number of lines of code of the file.
* CCN: the Cyclomatic Complexity Number of the file.
* SATD: flag telling if the modification contains Self-Admitted Technical Debt.
* SATDLine: the line that triggered the SATD flag.
* NbLinesAdded: the number of lines added.
* NbLinesDeleted the number of lines deleted.
* CommitId: the identifier of the commit
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.

### methods_history

*methods_history* has the following columns:

* Repository: the name of the repository
* Branches: the list of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* NbBranches: the number of branches in which this modification has been integrated. Make sure you have done a *git checkout* on all the branches that you want to analyze (all branches will be analyzed if you target a bare repository).
* FilePath: the relative path to file.
* FileName: the name of the file.
* FileType: the type of the file ("Production" or "Test")
* MethodName: the name of the method.
* NbParams: the number of parameters in the method signature.
* NLOC: the number of lines of code of the file.
* CCN: the Cyclomatic Complexity Number of the method.
* CommitId: the identifier of the commit
* Author: the author of the modification.
* DateTime: the date and time of the modification.
* Date: the date of the modification.
* HourOfDay: the hour of the day at which the modification took place.

## Requirements

**GitDelver** requires that the following software be installed in your environment:

* Python 3.6+
* PyDriller 2.0+ (use pip or conda to install it).
* Pandas 1.2+ (use pip or conda to install it).

**GitDelver** heavily uses PyDriller and Pandas and the author is very grateful to their contributors.

## License

**GitDelver** is open source software and is distributed under the MIT license. Contributions are welcome!

## Usage

**GitDelver** can be used in two ways.

### GitDelver console program

The **GitDelver console program** can be used for either analyzing a single repository or multiple repositories in bulk. This is the default mode. It both analyzes the repositories and produces the aforementioned CSV files. Please note that it is required that your first **set a few configuration parameters (mainly folder paths) in the *config.py* file** before launching the application (further information is provided below and in the configuration file itself). To run the **GitDelver** console program, simply run a terminal, go to your local **GitDelver** folder and enter the following command *python gitdelver*.

### Use the GitDelver API from another Python tool (e.g., Jupyter notebook)

You can also directly use the **GitDelver** API from another Python tool like a **Jupyter notebook**. **GitDelver** internally uses Pandas dataframes for storing and processing data and these dataframes can be obtained by directly calling the *delve* method of the *Delver* class. By doing this, you can use the datasets without having to first import CSV files.

## Configuration parameters to be set in *config.py*

* repo_path: file system path (using regular forward slashes) to either a single Git repository to be analyzed or a folder containing multiple repositories to be processed in bulk. In the latter case, each subfolder is assumed to be a regular directory containing a .git folder. Example of structure for bulk analysis:
  * repositories_folder_path/repo 1/(.git + code files)
  * repositories_folder_path/repo N/(.git + code files)  
* csv_output_folder_path: file system path (using regular forward slashes) to the folder where the generated CSV files are to be created.
* keep_unsupported_files: **GitDelver** uses some advanced features of PyDriller that are only available for supported file types (i.e. most common source code files). Set this option to True if you want **GitDelver** to report unsupported files as well.
* nb_processes: **GitDelver** uses Python multiprocessing for analyzing multiple repositories at once. Nowadays, most computers have at least 4 virtual CPUs, so this is the default value. You can set it to less or more in function of your needs. **GitDelver** will check that the entered value is correct and will limit this parameter to the maximum number of available vitrtual CPUs.
* verbose: this parameter sets the volume of feedback information provided by **GitDelver**. The analysis operation can take dozens of minutes for big repositories, so it is advised to set this to True in order to monitor its progression.
* SATD_keywords: this parameter configures the keywords that should be used to detect Self-Admitted Technical Debt in the lines of code.
* bugfix_keywords: this parameter configures the keywords that should be used to detect bug fixes in commit messages.
