from typing import IO

import requests
from pydantic import JsonValue

from .exception import BddFileError
from .models import BddFileResponse, BddFileUploadResult, UploadParams


def upload_simple(
    serivce_url: str, stream: IO[bytes], filename: str, user_id: str, biz: str, biz_params: JsonValue
) -> BddFileUploadResult:
    params = UploadParams(filename=filename, biz=biz, biz_params=biz_params)
    try:
        raw_response = requests.post(
            f"{serivce_url}/uploadSimpleFile",
            files={"file": (filename, stream, "application/octet-stream")},
            data={"params": params.model_dump_json()},
            headers={"X-User-Id": user_id},
        )
    except Exception as e:
        raise BddFileError(f"上传文件失败: {e}") from e

    if raw_response.status_code != 200:
        raise BddFileError(f"上传文件失败: {raw_response.status_code} {raw_response.text}")

    response = BddFileResponse[int].model_validate_json(raw_response.text)
    if response.code != 0:
        raise BddFileError(f"上传文件失败: {response.message}")
    return BddFileUploadResult(file_id=response.data)


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
