# Git Delver unit tests

The GitDelver unit tests use the pytest framework and the pytest-cov plugin (for test coverage).

If you do not have a virtual environment configured, just run a terminal in the GitDelver root folder and run one of the following commands:

python -m pytest

python -m pytest --cov=. tests/

!!! WARNING 1: the goal of these tests is to validate the specific features brought by GitDelver and not
to validate the underlying PyDriller implementations. PyDriller has its own test suite and it is
quite comprehensive.

!!! WARNING 2: these tests rely on the presence of test repositories in the "tests" folder. However,
Git does not like sub-repositories that are not Git sub-modules. So, for theses tests to work, be sure
to unzip "test_repos.zip" inside the "tests" folder.
Example structure: gitdelver/tests/test_repos/small_repo.