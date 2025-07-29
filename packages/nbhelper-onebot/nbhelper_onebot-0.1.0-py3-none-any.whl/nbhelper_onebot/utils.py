import os
import ssl
import uuid
from pathlib import Path

import httpx


def ensure_dir(dir_path: os.PathLike) -> bool:
    """
    确保目录存在，如果不存在则创建目录
    """
    if not os.path.exists(dir_path):  # 检查目录是否存在，如果不存在则创建目录
        os.makedirs(dir_path)
        return True
    else:
        return False


def ensure_file(file_path: os.PathLike) -> bool:
    """
    确保文件存在，如果不存在则创建空文件
    """
    if not os.path.exists(file_path):  # 检查文件是否存在，如果不存在则创建空文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        return True
    else:
        return False


def has_file(file_name: str, dir_path: os.PathLike) -> bool:
    """
    检查指定目录下是否存在指定文件
    """
    return os.path.exists(os.path.join(dir_path, file_name))


def file_name_deduplication(file_name: str, dir_path: os.PathLike) -> str:
    """
    确保文件名在指定目录下唯一，如果文件名已存在，则在文件名后添加数字后缀
    """
    base_name, ext = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    while os.path.exists(os.path.join(dir_path, new_file_name)):
        new_file_name = f"{base_name}_{counter}{ext}"
        counter += 1
    return new_file_name


async def download_async(
    url: str, download_path: Path, filename: str = uuid.uuid4().__str__()
) -> Path | None:
    """
    使用不强制安全的SSL上下文下载文件到指定的目录，如果成功下载则返回文件路径，否则返回None。

    请注意，这个函数不会创建目录结构，因此在调用此函数之前，请确保`download_path`目录已存在。
    """
    try:
        # 创建自定义 SSL 上下文
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "DEFAULT@SECLEVEL=1"
        )  # 降低安全级别，允许更多的加密算法

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(10.0), verify=ssl_context
        ) as client:
            response = await client.get(url)
            if response.status_code == 200:
                # ensure_dir(os.path.dirname(target_path))
                file_path = download_path.joinpath(filename)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
    except Exception as e:
        raise e
    return None


def download(
    url: str, download_path: Path, filename: str = uuid.uuid4().__str__()
) -> Path | None:
    """
    使用不强制安全的SSL上下文下载文件到指定的目录，如果成功下载则返回文件路径，否则返回None。

    请注意，这个函数不会创建目录结构，因此在调用此函数之前，请确保`download_path`目录已存在。
    """
    try:
        # 创建自定义 SSL 上下文
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "DEFAULT@SECLEVEL=1"
        )  # 降低安全级别，允许更多的加密算法

        with httpx.Client(timeout=httpx.Timeout(10.0), verify=ssl_context) as client:
            response = client.get(url)
            if response.status_code == 200:
                # ensure_dir(os.path.dirname(target_path))
                file_path = download_path.joinpath(filename)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
    except Exception as e:
        raise e
    return None
