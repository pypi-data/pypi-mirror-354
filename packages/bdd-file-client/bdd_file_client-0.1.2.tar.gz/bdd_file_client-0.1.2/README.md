# BDD File Client

BDD 平台文件服务客户端

## 安装方式

```shell
$ pip install bdd-file-client
```

## 快速开始

### 配置 BddFileClient

```python
from bdd_file import BddFileClient, UploadMode

client = BddFileClient(
    profile="dev",            # 可选 dev、beta、prod，默认为 dev
    default_user_id="114514", # 默认的用户 ID，可在调用时覆盖
)
```

- `profile` 用于指定后端环境，会自动映射到对应的服务地址
- `default_user_id`、`default_biz`、`default_mode` 均为可选，若在调用时未显式提供则使用此处的默认值

### 上传文件

```python
# 1. 通过文件路径上传（简单上传）
result = client.upload(
    path="example.png",
    mode=UploadMode.SIMPLE,   # 默认 auto，可选 simple、chunked
    biz="chat",
    biz_params={"chat_id": "191810"},
)
print("上传成功，file_id =", result.file_id)

# 2. 通过文件流上传
with open("example.png", "rb") as f:
    result = client.upload(
        stream=f,
        filename="example.png",           # 当使用 stream 时，必须显式指定文件名
        biz="chat",
        biz_params={"chat_id": "191810"},
    )
```

注意
- `path` 与 `stream` 只能二选一
- 分片上传（UploadMode.CHUNKED）暂未实现，设置后会抛出 `BddFileError`

### 下载文件

```python
# 保存到本地文件
client.download(
    file_id=result.file_id,
    path="downloaded.png",
)

# 或写入到自定义流
from io import BytesIO

buffer = BytesIO()
client.download(file_id=result.file_id, stream=buffer)
print(buffer.getvalue())
```

### 错误处理

所有业务及网络错误都会抛出 `bdd_file.BddFileError`，可按需捕获：

```python
from bdd_file import BddFileClient, BddFileError

client = BddFileClient(default_user_id="114514")
try:
    result = client.upload(path="not_exists.txt", biz="chat")
except BddFileError as e:
    print("操作失败：", e)
```
