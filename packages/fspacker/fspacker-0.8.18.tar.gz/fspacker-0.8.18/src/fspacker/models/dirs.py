from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

__all__ = ["Dirs", "default_cache_dir"]

# cache settings
default_cache_dir = Path("~").expanduser() / ".cache" / "fspacker"


class Dirs(BaseModel):
    """目录配置."""

    cache: Path = default_cache_dir
    embed: Path = cache / "embed-repo"
    libs: Path = cache / "libs-repo"
    checksum: str = ""

    def __str__(self) -> str:
        """字符串化.

        Returns:
            str: 字符串.
        """
        return f"cache=[{self.cache}], embed=[{self.embed}], libs=[{self.libs}]"

    @property
    def entries(self) -> tuple[Path, Path, Path]:
        """获取所有目录.

        Returns:
            tuple[Path, Path, Path]: 所有目录
        """
        return (self.cache, self.embed, self.libs)
