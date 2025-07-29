import sys
import os


def setup_additional_dependency_path(relative_path: str) -> None:
    """
    Add the relative_path directory to the Python path.
    This allows imports from the relative_path directory to work in the Function runtime.
    The relative_path should be relative to the placement of the samsarafn.py file.
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path_dir = os.path.join(file_dir, relative_path)

    if relative_path_dir not in sys.path:
        sys.path.append(relative_path_dir)
