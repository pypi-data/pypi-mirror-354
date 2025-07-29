from pathlib import Path

import pytest

from fspacker.exceptions import ProjectParseError
from fspacker.exceptions import RunExecutableError
from fspacker.parsers.manager import ProjectManager
from fspacker.parsers.project import Project
from fspacker.settings import get_settings


@pytest.fixture(autouse=True)
def reset_mode() -> None:
    get_settings().mode.reset()


def test_manager_parse_single(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex00_simple)
    assert "已解析项目" in caplog.text
    assert len(manager.projects) == 1


def test_manager_parse_single_no_recursive(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    get_settings().mode.recursive = False
    manager = ProjectManager(dir_ex00_simple)
    assert "已解析项目" in caplog.text
    assert len(manager.projects) == 1


def test_manager_parse_multiple(
    dir_examples: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    get_settings().mode.recursive = True
    manager = ProjectManager(dir_examples)
    assert "已解析项目" in caplog.text
    assert len(manager.projects) > 1


def test_manager_parse_error_invalid_root_dir(tmp_path: Path) -> None:
    with pytest.raises(ProjectParseError) as execinfo:
        ProjectManager(tmp_path / "invalid_dir")

    assert "根目录无效" in str(execinfo.value)


def test_manager_parse_error_no_project(
    dir_ex90_error_no_project: Path,
) -> None:
    get_settings().mode.recursive = False

    with pytest.raises(ProjectParseError) as execinfo:
        ProjectManager(dir_ex90_error_no_project)

    assert "路径下未找到有效的 pyproject.toml 文件" in str(execinfo.value)


def test_manager_parse_error_no_project_recursive(
    dir_ex90_error_no_project: Path,
) -> None:
    get_settings().mode.recursive = True

    with pytest.raises(ProjectParseError) as execinfo:
        ProjectManager(dir_ex90_error_no_project)

    assert "路径下未找到有效的 pyproject.toml 文件" in str(execinfo.value)


def test_manager_build_without_cache(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
) -> None:
    cache_dir = tmp_path / ".cache"
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    get_settings().dirs.cache = cache_dir
    get_settings().dirs.embed = cache_dir / "embed-repo"

    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    manager.build()
    assert "从地址下载运行时" in caplog.text


def test_manager_build_without_embed(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
) -> None:
    embed_dir = tmp_path / "embed-repo"
    if not embed_dir.exists():
        embed_dir.mkdir(parents=True)

    get_settings().dirs.embed = embed_dir

    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    manager.build()
    assert "非离线模式, 获取运行时" in caplog.text


def test_manager_build_without_libs(
    dir_ex01_helloworld: Path,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
) -> None:
    libs_dir = tmp_path / "libs-repo"
    if not libs_dir.exists():
        libs_dir.mkdir(parents=True)

    get_settings().dirs.libs = libs_dir

    manager = ProjectManager(dir_ex01_helloworld)
    manager.clean()
    manager.build()
    assert "下载依赖" in caplog.text


def test_manager_build_with_diff_embed(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    if not get_settings().dirs.embed.exists():
        get_settings().dirs.embed.mkdir(parents=True)

    project = Project(dir_ex00_simple)
    with project.embed_filepath.open("wb") as f:
        f.write(b"invalid")

    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    manager.build()
    assert "校验和不一致, 重新下载" in caplog.text


def test_manager_build_tkinter(
    dir_ex03_tkinter: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex03_tkinter)
    manager.clean()
    manager.build()
    assert "检测到 tkinter 相关依赖" in caplog.text


def test_manager_build_pyqt(
    dir_ex04_pyside2: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    get_settings().mode.simplify = True

    manager = ProjectManager(dir_ex04_pyside2)
    manager.clean()
    manager.build()
    assert "检测到目标库: PySide2" in caplog.text


def test_manager_build_bottle(
    dir_ex31_bottle: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex31_bottle)
    manager.clean()
    manager.build()
    assert "打包依赖: [[green bold]bottle>=0.13.2[/]" in caplog.text


def test_manager_build_bottle_twice(
    dir_ex31_bottle: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex31_bottle)
    manager.clean()
    manager.build()
    manager.build()
    assert "依赖库已存在, 跳过: " in caplog.text


def test_manager_build_bottle_twice_after_clean(
    dir_ex31_bottle: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex31_bottle)
    manager.clean()
    manager.build()
    manager.clean()
    manager.build()
    assert "找到本地满足要求的依赖" in caplog.text


def test_manager_build_orderedset(
    dir_ex06_from_source: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex06_from_source)
    manager.clean()
    manager.build()
    assert "找到压缩包库文件:" in caplog.text


def test_manager_build_error_no_source(
    dir_ex91_error_no_source: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex91_error_no_source)
    manager.clean()
    manager.build()

    assert "未找到入口 Python 文件" in caplog.text


def test_manager_build_error_without_embed_and_offline(
    dir_ex00_simple: Path,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    embed_dir = tmp_path / "embed-repo"
    if not embed_dir.exists():
        embed_dir.mkdir(parents=True)

    get_settings().dirs.embed = embed_dir
    get_settings().mode.offline = True

    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    manager.build()

    assert "离线模式且本地运行时不存在" in caplog.text


def test_manager_run_single(
    dir_ex00_simple: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    manager.build()
    manager.run()

    assert "调用可执行文件" in caplog.text


def test_manager_run_multi(
    dir_ex00_simple: Path,
    dir_ex01_helloworld: Path,
    dir_examples: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    get_settings().mode.recursive = True

    for root_dir in (dir_ex00_simple, dir_ex01_helloworld):
        manager = ProjectManager(root_dir)
        manager.clean()
        manager.build()

    ProjectManager(dir_examples).run("ex01_helloworld")
    assert "调用可执行文件" in caplog.text


def test_manager_run_error_multi_executable_no_name(
    dir_examples: Path,
) -> None:
    get_settings().mode.recursive = True

    manager = ProjectManager(dir_examples)
    manager.clean()

    with pytest.raises(RunExecutableError) as execinfo:
        manager.run()

    assert "存在多个项目" in str(execinfo.value)
    assert "请输入名称" in str(execinfo.value)


def test_manager_run_error_multi_executable_name_not_match(
    dir_examples: Path,
) -> None:
    get_settings().mode.recursive = True

    app_name = "test123"

    manager = ProjectManager(dir_examples)
    with pytest.raises(RunExecutableError) as execinfo:
        manager.run(app_name)

    assert "未找到项目" in str(execinfo.value)


def test_manager_run_error_no_executable(dir_ex00_simple: Path) -> None:
    """测试没有可执行文件."""
    manager = ProjectManager(dir_ex00_simple)
    manager.clean()
    with pytest.raises(RunExecutableError) as execinfo:
        manager.run()

    assert "项目可执行文件不存在" in str(execinfo.value)
