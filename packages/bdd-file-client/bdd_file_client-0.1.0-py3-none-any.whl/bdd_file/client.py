from enum import Enum
from pathlib import Path
from typing import IO

from pydantic import JsonValue

from .exception import BddFileError
from .invoke_api import download, upload_simple
from .models import BddFileUploadResult
from .settings import BDD_FILE_PROFILES, settings


class UploadMode(str, Enum):
    """
    上传模式

    SIMPLE: 简单上传，不支持断点续传
    CHUNKED: 分片上传，支持断点续传
    AUTO: 自动选择上传模式，如果文件大于 100MB，则使用分片上传，否则使用简单上传
    """

    SIMPLE = "simple"
    CHUNKED = "chunked"
    AUTO = "auto"


class BddFileClient:
    def __init__(
        self,
        profile: str = settings.PROFILE,
        default_user_id: str | None = None,
        default_biz: str | None = None,
        default_mode: UploadMode | None = None,
    ):
        self.service_url = BDD_FILE_PROFILES[profile]
        self.default_user_id = default_user_id
        self.default_biz = default_biz
        self.default_mode = default_mode

    def upload(
        self,
        *,
        path: str | Path | None = None,
        stream: IO[bytes] | None = None,
        filename: str | None = None,
        mode: UploadMode | str = UploadMode.AUTO,
        session_id: str | None = None,
        user_id: str | None = None,
        biz: str | None = None,
        biz_params: JsonValue = None,
    ) -> BddFileUploadResult:
        """
        上传文件

        参数：
            - path: 文件路径，path 和 stream 只能传一个
            - stream: 文件流，path 和 stream 只能传一个
            - filename: 文件名，如果传了，则使用这个文件名，否则使用 path 的文件名；传 stream 时，filename 必须传
            - mode: 上传模式，默认使用 client 的 default_mode
            - session_id: 分片上传的会话ID，用于恢复之前的分片上传
            - user_id: 用户ID，如果没有传，则使用 client 的 default_user_id
            - biz: 业务类型，如果没有传，则使用 client 的 default_biz
            - biz_params: 业务参数，JSON 格式

        返回：
            - BddFileUploadResult: 上传结果
        """
        mode = UploadMode(mode)
        if mode == UploadMode.CHUNKED or session_id is not None:
            raise BddFileError("分片上传暂未实现")

        user_id = self._ensure_user_id(user_id)
        if biz is None:
            if self.default_biz is None:
                raise BddFileError("biz为空")
            biz = self.default_biz

        if stream is None and path is not None:
            path = Path(path)
            filename = filename or path.name
            with open(path, "rb") as f:
                return upload_simple(self.service_url, f, filename, user_id, biz, biz_params)
        elif stream is not None and path is None:
            if filename is None:
                raise BddFileError("filename为空")
            return upload_simple(self.service_url, stream, filename, user_id, biz, biz_params)
        elif stream is None and path is None:
            raise BddFileError("path和stream不能同时为空")
        else:
            raise BddFileError("path和stream不能同时设置")

    def download(
        self,
        *,
        file_id: int,
        user_id: str | None = None,
        path: str | Path | None = None,
        stream: IO[bytes] | None = None,
    ) -> None:
        """
        下载文件

        参数：
            - file_id: 文件ID
            - user_id: 用户ID，如果没有传，则使用 client 的 default_user_id
            - path: 文件路径，如果传了，则将文件下载到这个路径，与 stream 只能传一个
            - stream: 文件流，如果传了，则将文件下载到这个流，与 path 只能传一个
        """
        user_id = self._ensure_user_id(user_id)

        if path is not None and stream is None:
            with open(path, "wb") as f:
                download(self.service_url, file_id, user_id, f)
        elif stream is not None and path is None:
            download(self.service_url, file_id, user_id, stream)
        elif stream is None and path is None:
            raise BddFileError("path和stream不能同时为空")
        else:
            raise BddFileError("path和stream不能同时设置")

    def _ensure_user_id(self, user_id: str | None) -> str:
        if user_id is None:
            if self.default_user_id is None:
                raise BddFileError("user_id为空")
            return self.default_user_id
        return user_id
