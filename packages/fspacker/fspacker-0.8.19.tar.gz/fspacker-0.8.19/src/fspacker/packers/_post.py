import logging
import shutil

from fspacker.packers._base import BasePacker
from fspacker.settings import get_settings

logger = logging.getLogger(__name__)


class PostPacker(BasePacker):
    NAME = "项目后处理打包"

    def pack(self) -> None:
        if get_settings().mode.archive:
            logger.info(f"压缩文件: [[green]{self.info.dist_dir}[/]]")
            shutil.make_archive(
                self.info.dist_dir.name,
                "zip",
                self.info.dist_dir.parent,
                self.info.dist_dir.name,
            )
