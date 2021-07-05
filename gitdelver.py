# Copyright (c) 2021 Nicolas Riquet (MIT license)

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
        params["nb_processes"]
        params["verbose"]
    except:
        utilities._handle_error("Missing configuration parameter")
    
    list_of_path_vars = ["repo_path", "csv_output_folder_path"]
    
    for path_var in list_of_path_vars:
        path = params[path_var]
        
        if not (Path(path).exists()):
            utilities._handle_error("Path \"{}\" does not exist".format(path))
    
    if not isinstance(params["keep_unsupported_files"], bool):
        utilities._handle_error("Configuration parameter \"keep_unsupported_files\" has an invalid value")
    
    nb_processes = params["nb_processes"]
    
    if not isinstance(nb_processes, int) or nb_processes <= 1:
        utilities._handle_error("Configuration parameter \"nb_processes\" has an invalid value")
    
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
    verbose = config_params["verbose"]
    
    gitdelver = Delver(repo_path, csv_output_folder_path, utilities._log, keep_unsupported_files, verbose)
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