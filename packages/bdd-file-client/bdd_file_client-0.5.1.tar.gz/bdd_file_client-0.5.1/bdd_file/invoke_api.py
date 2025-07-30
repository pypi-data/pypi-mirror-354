import functools
import json
from typing import IO, Callable, Type, TypeVar

import requests
from pydantic import JsonValue

from .exception import BddFileError
from .models import BddFileInfo, BddFilePaged, BddFileResponse, Biz

Data = TypeVar("Data")


def _invoke_api(
    api_name: str, response_type: Type[Data]
) -> Callable[[Callable[..., requests.Response]], Callable[..., Data]]:
    def wrapper(func: Callable[..., requests.Response]) -> Callable[..., Data]:
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs) -> Data:
            try:
                raw_response = func(*args, **kwargs)
            except Exception as e:
                raise BddFileError(f"{api_name}失败: {e}") from e

            if raw_response.status_code != 200:
                raise BddFileError(f"{api_name}失败: {raw_response.status_code} {raw_response.text}")

            response = BddFileResponse[response_type].model_validate_json(raw_response.text)
            if response.code != 0 or response.data is None:
                raise BddFileError(f"{api_name}失败: {response.message}")
            return response.data

        return inner_wrapper

    return wrapper


@_invoke_api("上传文件", int)
def upload_simple(
    serivce_url: str, stream: IO[bytes], filename: str, user_id: str, biz: str, biz_params: JsonValue
) -> requests.Response:
    params = json.dumps({"filename": filename, "biz": Biz(biz).value, "biz_params": biz_params})
    return requests.post(
        f"{serivce_url}/uploadSimpleFile",
        files={"file": (filename, stream, "application/octet-stream")},
        data={"params": params},
        headers={"X-User-Id": user_id},
    )


def download(service_url: str, file_id: int, user_id: str, stream: IO[bytes]) -> None:
    try:
        raw_response = requests.get(
            f"{service_url}/downloadFile", params={"file_id": file_id}, headers={"X-User-Id": user_id}, stream=True
        )
    except Exception as e:
        raise BddFileError(f"下载文件失败: {e}") from e

    if raw_response.status_code != 200:
        raise BddFileError(f"下载文件失败: {raw_response.status_code} {raw_response.text}")

    for chunk in raw_response.iter_content(chunk_size=64 * 1024):
        stream.write(chunk)


@_invoke_api("获取下载URL", str)
def get_download_url(service_url: str, file_id: int, user_id: str, expires_seconds: int) -> requests.Response:
    return requests.get(
        f"{service_url}/getFileDownloadUrl",
        params={"file_id": file_id, "expires_in": expires_seconds},
        headers={"X-User-Id": user_id},
    )


@_invoke_api("删除文件", int)
def delete_file(service_url: str, file_id: int, user_id: str) -> requests.Response:
    return requests.delete(f"{service_url}/deleteFile", params={"file_id": file_id}, headers={"X-User-Id": user_id})


@_invoke_api("获取聊天文件列表", BddFilePaged[BddFileInfo])
def list_chat_files(service_url: str, chat_id: str, user_id: str, offset: int, limit: int) -> requests.Response:
    return requests.get(
        f"{service_url}/listChatFiles",
        params={"chat_id": chat_id, "offset": offset, "limit": limit},
        headers={"X-User-Id": user_id},
    )
