from typing import Generic, TypeVar

from pydantic import BaseModel, JsonValue

T = TypeVar("T")


class BddFileResponse(BaseModel, Generic[T]):
    code: int
    data: T | None
    message: str | None
    trace_id: str


class BddFileUploadResult(BaseModel):
    file_id: int | None = None
    session_id: str | None = None


class UploadParams(BaseModel):
    filename: str
    biz: str
    biz_params: JsonValue
