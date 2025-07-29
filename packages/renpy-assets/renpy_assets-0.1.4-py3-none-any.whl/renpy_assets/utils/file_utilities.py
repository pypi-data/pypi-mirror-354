import os
import re
from pathlib import Path
from typing import List


def find_files_by_patterns(
    root_dir: str,
    patterns: List[str]
) -> List[Path]:
    """
    Recursively search for files under `root_dir` that match any of the given regex patterns.

    Args:
        root_dir (str): The root directory to start the search.
        patterns (List[str]): A list of regex patterns to match filenames.

    Returns:
        List[Path]: List of matching file paths.
    """
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
    matches = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            for pattern in compiled_patterns:
                if pattern.search(filename):
                    matches.append(Path(dirpath) / filename)
                    break

    return matches
