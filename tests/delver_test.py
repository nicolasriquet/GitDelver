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
This module contains the unit tests for the "delver" module.
!!! WARNING 1: the goal of these tests is to validate the specific features brought by GitDelver and not
to validate the underlying PyDriller implementations. PyDriller has its own test suite and it is
quite comprehensive.
!!! WARNING 2: these tests rely on the presence of test repositories in the "tests" folder. However,
Git does not like sub-repositories that are not Git sub-modules. So, for theses tests to work, be sure
to unzip "test_repos.zip" directly inside the "tests" folder.
Example structure: gitdelver/tests/test_repos/small_repo.
"""

import pytest, os
from delver import Delver
import pandas as pd
from typing import Callable, List
import utilities


@pytest.fixture
def delver_COMMITS_FILES_METHODS_fixture() -> List[pd.DataFrame]:
    """
    This test fixture initializes the test repository.
    """

    current_dir = os.path.dirname(__file__)
    repo_path = current_dir + "/test_repos/small_repo"
    
    delver = Delver(repo_path, analysis_mode = utilities.AnalysisMode.COMMITS_FILES_METHODS, nb_commits_before_checkpoint = 0)
    
    datasets = delver.run()
    
    return datasets


@pytest.fixture
def delver_COMMITS_FILES_fixture() -> List[pd.DataFrame]:
    """
    This test fixture initializes the test repository.
    """

    current_dir = os.path.dirname(__file__)
    repo_path = current_dir + "/test_repos/small_repo"
    
    delver = Delver(repo_path, analysis_mode = utilities.AnalysisMode.COMMITS_FILES, nb_commits_before_checkpoint = 0)
    
    datasets = delver.run()
    
    return datasets


def test_delver_COMMITS_FILES_METHODS_run_nb_datasets(delver_COMMITS_FILES_METHODS_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that Delver returns the expected number of datasets.
    """
    
    datasets = delver_COMMITS_FILES_METHODS_fixture
    
    assert len(datasets) == 3


def test_delver_COMMITS_FILES_run_nb_datasets(delver_COMMITS_FILES_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that Delver returns the expected number of datasets.
    """
    
    datasets = delver_COMMITS_FILES_fixture
    
    assert len(datasets) == 2


def test_delver_run_datasets_names(delver_COMMITS_FILES_METHODS_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated datasets have the expected names.
    """
    
    datasets = delver_COMMITS_FILES_METHODS_fixture
    
    test_pass = False
    
    if (datasets[0].name == "commits_history" or
        datasets[1].name == "files_history" or
        datasets[2].name == "methods_history"):
        test_pass = True
    
    assert test_pass is True


def test_delver_run_commits_dataset_shape(delver_COMMITS_FILES_METHODS_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated commits dataset has the expected shape.
    """
    
    datasets = delver_COMMITS_FILES_METHODS_fixture
    
    test_pass = False
    
    if (datasets[0].dataframe.shape == (5, 19)):
        test_pass = True
    
    assert test_pass is True


def test_delver_run_files_dataset_shape(delver_COMMITS_FILES_METHODS_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated files dataset has the expected shape.
    """
    
    datasets = delver_COMMITS_FILES_METHODS_fixture
    
    test_pass = False
    
    if (datasets[1].dataframe.shape == (6, 24)):
        test_pass = True
    
    assert test_pass is True


def test_delver_run_methods_dataset_shape(delver_COMMITS_FILES_METHODS_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated methods dataset has the expected shape.
    """
    
    datasets = delver_COMMITS_FILES_METHODS_fixture
    
    test_pass = False
    
    if (datasets[2].dataframe.shape == (70, 16)):
        test_pass = True
    
    assert test_pass is True