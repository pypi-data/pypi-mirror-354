from __future__ import annotations

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


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="Run slow tests",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="需要 --runslow 选项")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


@pytest.fixture
def dir_examples() -> Path:
    return DIR_EXAMPLES


@pytest.fixture(autouse=True, scope="session")
def clear_dist_folders() -> None:
    dist_folders = [x for x in DIR_EXAMPLES.rglob("dist") if x.is_dir()]
    for dist_folder in dist_folders:
        shutil.rmtree(dist_folder, ignore_errors=True)
