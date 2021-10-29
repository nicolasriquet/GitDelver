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
This module contains the GitDelver console application. It basically reads the configuration parameters
and then launches several processes, each running its own delver.
"""

import os
import multiprocessing as mp
from datetime import datetime
from pathlib import Path
from delver import Delver
from config import config_params
import utilities


def _check_config_params(params: config_params):
    """
    Check that the values set in the configuration parameters are valid and raise an error if it is not
    the case.
    """

    try:
        params["repo_path"]
        params["csv_output_folder_path"]
        params["keep_unsupported_files"]
        params["analysis_mode"]
        params["nb_processes"]
        params["nb_commits_before_checkpoint"]
        params["verbose"]
        params["SATD_keywords"]
        params["bugfix_keywords"]        
    except:
        utilities._handle_error(("Missing configuration parameter. All of the following should be set: repo_path," 
                                " csv_output_folder_path, keep_unsupported_files, analysis_mode, nb_processes," 
                                " nb_commits_before_checkpoint, verbose, SATD_keywords, bugfix_keywords."))
    
    list_of_path_vars = ["repo_path", "csv_output_folder_path"]
    
    for path_var in list_of_path_vars:
        path = params[path_var]
        
        if not (Path(path).exists()):
            utilities._handle_error("Path \"{}\" does not exist".format(path))
    
    if not isinstance(params["keep_unsupported_files"], bool):
        utilities._handle_error("Configuration parameter \"keep_unsupported_files\" has an invalid value")
    
    if (params["analysis_mode"] not in [utilities.AnalysisMode.COMMITS, utilities.AnalysisMode.COMMITS_FILES,
                                        utilities.AnalysisMode.COMMITS_FILES_METHODS]):
        utilities._handle_error("Configuration parameter \"analysis_mode\" has an invalid value")
    
    if not isinstance(params["nb_processes"], int) or params["nb_processes"] <= 1:
        utilities._handle_error("Configuration parameter \"nb_processes\" has an invalid value")
        
    if not isinstance(params["nb_commits_before_checkpoint"], int) or params["nb_commits_before_checkpoint"] < 0:
        utilities._handle_error("Configuration parameter \"nb_commits_before_checkpoint\" has an invalid value")
    
    if not isinstance(params["verbose"], bool):
        utilities._handle_error("Configuration parameter \"verbose\" has an invalid value")
    
    if not all(isinstance(x, str) for x in params["SATD_keywords"]):
        utilities._handle_error("Configuration parameter \"SATD_keywords\" has invalid values")
    
    if not all(isinstance(x, str) for x in params["bugfix_keywords"]):
        utilities._handle_error("Configuration parameter \"bugfix_keywords\" has invalid values")
        
        
def _go_delving(repo_path: str):
    """
    This function is executed by every process started by the GitDelver console application. It reads
    configuaration parameters and then starts one delver per process.
    """

    csv_output_folder_path = config_params["csv_output_folder_path"]
    keep_unsupported_files = config_params["keep_unsupported_files"]
    analysis_mode = config_params["analysis_mode"]
    nb_commits_before_checkpoint = config_params["nb_commits_before_checkpoint"]
    verbose = config_params["verbose"]
    
    gitdelver = Delver(repo_path, csv_output_folder_path, keep_unsupported_files, analysis_mode, 
                       nb_commits_before_checkpoint, utilities._log, verbose)
    
    gitdelver.run()


if __name__ == "__main__":
    """
    This is the starting point of the GitDelver console application.
    """
    
    start_time = datetime.now()    
    
    _check_config_params(config_params)
    
    repo_path = config_params["repo_path"]
    
    if (utilities.is_single_repository(repo_path)):
        # The path given is a single repository.
        
        _go_delving(repo_path)
                
    else:
        # The path given is a folder containing several repositories to be processed in bulk.
        repositories_list = [f.path for f in os.scandir(repo_path) if f.is_dir()]
            
        nb_processes_config = config_params["nb_processes"]
        nb_cores = mp.cpu_count()
        nb_processes = nb_processes_config if (nb_processes_config >= 1 and nb_processes_config <= nb_cores) else nb_cores
    
        utilities._log("Starting {} delving processes on the repositories located at {}.".format(nb_processes, repo_path))
        
        pool = mp.Pool(nb_processes)
        pool.map(_go_delving, repositories_list)
    
    end_time = datetime.now()
    utilities._log("Mining process completed in {}.".format(end_time - start_time))