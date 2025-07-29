import logging
import shutil
from pathlib import Path

import pytest

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

CWD = Path(__file__).parent
DIR_ROOT = CWD.parent
DIR_EXAMPLES = DIR_ROOT / "examples"


pytest_plugins = [
    "tests.fixtures.cli",
    "tests.fixtures.dirs",
]


@pytest.fixture
def dir_examples() -> Path:
    return DIR_EXAMPLES


@pytest.fixture(autouse=True, scope="session")
def clear_dist_folders() -> None:
    dist_folders = [x for x in DIR_EXAMPLES.rglob("dist") if x.is_dir()]
    for dist_folder in dist_folders:
        shutil.rmtree(dist_folder, ignore_errors=True)
