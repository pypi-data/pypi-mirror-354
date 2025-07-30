from tempfile import NamedTemporaryFile

import pytest

from bdd_file import BddFileClient


@pytest.fixture(scope="session")
def bdd_file_client() -> BddFileClient:
    return BddFileClient(default_user_id="114514")


@pytest.fixture(scope="session")
def upload_simple_file(bdd_file_client: BddFileClient) -> int:
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"test")
        temp_file.close()

        result = bdd_file_client.upload(
            path=temp_file.name, mode="simple", biz="chat", biz_params={"chat_id": "191810"}
        )
        assert result.file_id is not None
        assert result.session_id is None
        assert isinstance(result.file_id, int)

    return result.file_id


def test_download_file(bdd_file_client: BddFileClient, upload_simple_file: int):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.close()

        bdd_file_client.download(file_id=upload_simple_file, path=temp_file.name)
        with open(temp_file.name, "rb") as f:
            assert f.read() == b"test"
