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
This module contains the unit tests for the "gitdelver" module.
"""

import pytest, gitdelver
from typing import Callable, Dict
from utilities import AnalysisMode
from pathlib import Path

@pytest.fixture
def gitdelver_config_params_fixture() -> Dict[str, str]:
    """
    This test fixture initializes the config_params dictionary.
    """

    config_params = {
    "repo_path": str(Path.home()),
    "csv_output_folder_path": str(Path.home()),
    "keep_unsupported_files": False,
    "analysis_mode": AnalysisMode.COMMITS_FILES,
    "nb_processes": 4,
    "nb_commits_before_checkpoint": 50,
    "verbose": True,
    "SATD_keywords": ["//todo", "#todo", "//fixme", "#fixme", "//tofix", "#tofix",
                     "//hack", "#hack", "//workaround", "#workaround"],
    "bugfix_keywords": ["fix", "solve", "bug", "defect", "problem"]
    }
    
    return config_params


def test_check_config_params_valid(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises no SystemExit exception when all parameters are present and valid.
    """
    
    config_params = gitdelver_config_params_fixture
    
    gitdelver._check_config_params(config_params)
        

def test_check_config_params_missing_repo_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when repo_path is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("repo_path", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_csv_output_folder_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when csv_output_folder_path is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("csv_output_folder_path", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_keep_unsupported_files(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when keep_unsupported_files is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("keep_unsupported_files", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_analysis_mode(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when analysis_mode is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("analysis_mode", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_nb_processes(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when nb_processes is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("nb_processes", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_nb_commits_before_checkpoint(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when nb_commits_before_checkpoint is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("nb_commits_before_checkpoint", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_verbose(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when verbose is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("verbose", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_SATD_keywords(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when SATD_keywords is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("SATD_keywords", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_missing_bugfix_keywords(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when bugfix_keywords is missing.
    """
    
    config_params = gitdelver_config_params_fixture.pop("bugfix_keywords", None)
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_empty_repo_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when repo_path is empty.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["repo_path"] = ""
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_invalid_repo_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when repo_path is invalid.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["repo_path"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_empty_csv_output_folder_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when csv_output_folder_path is empty.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["csv_output_folder_path"] = ""
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_invalid_csv_output_folder_path(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when csv_output_folder_path is invalid.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["csv_output_folder_path"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_keep_unsupported_files_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when keep_unsupported_files is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["keep_unsupported_files"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_analysis_mode_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when analysis_mode is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["analysis_mode"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_nb_processes_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when nb_processes is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["nb_processes"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)


def test_check_config_params_nb_commits_before_checkpoint_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when nb_commits_before_checkpoint is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["nb_commits_before_checkpoint"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)
        

def test_check_config_params_verbose_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when verbose is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["verbose"] = "test"
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)
        

def test_check_config_params_SATD_keywords_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when SATD_keywords is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["SATD_keywords"] = [1, 2]
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)
        

def test_check_config_params_bugfix_keywords_wrong_type(gitdelver_config_params_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that _check_config_params raises a SystemExit exception when bugfix_keywords is of the wrong type.
    """
    
    config_params = gitdelver_config_params_fixture
    
    config_params["bugfix_keywords"] = [1, 2]
    
    with pytest.raises(SystemExit):
        gitdelver._check_config_params(config_params)