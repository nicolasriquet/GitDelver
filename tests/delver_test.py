# Copyright (c) 2021 Nicolas Riquet (MIT license)

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


@pytest.fixture
def delver_fixture() -> List[pd.DataFrame]:
    """
    This test fixture initializes the test repository.
    """

    current_dir = os.path.dirname(__file__)
    
    delver = Delver(current_dir + "/test_repos/small_repo")
    
    datasets = delver.delve()
    
    return datasets


def test_delver_delve_nb_datasets(delver_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that Delver returns the expected number of datasets.
    """
    
    datasets = delver_fixture
    
    assert len(datasets) == 3


def test_delver_delve_datasets_names(delver_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated datasets have the expected names.
    """
    
    datasets = delver_fixture
    
    test_pass = False
    
    if (datasets[0].name == "commits_history" or
        datasets[1].name == "files_history" or
        datasets[2].name == "methods_history"):
        test_pass = True
    
    assert test_pass is True


def test_delver_delve_datasets_shapes(delver_fixture: Callable[[None], List[pd.DataFrame]]):
    """
    This unit test checks that the generated datasets have the expected shapes.
    """
    
    datasets = delver_fixture
    
    test_pass = False
    
    if (datasets[0].dataframe.shape == (5, 19) or
        datasets[1].dataframe.shape == (6, 21) or
        datasets[2].dataframe.shape == (70, 15)):
        test_pass = True
    
    assert test_pass is True