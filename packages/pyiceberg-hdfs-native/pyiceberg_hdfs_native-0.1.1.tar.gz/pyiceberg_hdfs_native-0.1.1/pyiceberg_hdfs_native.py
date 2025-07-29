from functools import lru_cache
from typing import Callable, ClassVar
from fsspec import AbstractFileSystem
from hdfs_native import fsspec
from pyiceberg.io.fsspec import FsspecFileIO
from pyiceberg.typedef import Properties


_HDFS_SCHEME = "hdfs"


class HdfsFileSystem(fsspec.HdfsFileSystem):
    protocol: ClassVar[str] = _HDFS_SCHEME


class HdfsFileIO(FsspecFileIO):
    def __init__(self, properties: Properties) -> None:
        super().__init__(properties)
        self.get_fs: Callable[[str], AbstractFileSystem] = lru_cache(self._get_fs)

    def _get_fs(self, scheme: str) -> AbstractFileSystem:
        if scheme != "hdfs":
            raise ValueError(f"Unsupported scheme: {scheme}")
        return HdfsFileSystem()
