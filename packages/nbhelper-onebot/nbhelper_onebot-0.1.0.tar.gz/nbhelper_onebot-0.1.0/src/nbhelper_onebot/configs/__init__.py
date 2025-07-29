from pathlib import Path

from pydantic import BaseModel, Field


class NBHelperConfig(BaseModel):
    message_cache_size: int = Field(
        default=1000, description="缓存消息ID的最大数量，默认为1000"
    )
    message_cache_ttl: int = Field(
        default=300, description="缓存消息ID的过期时间，单位为秒，默认为300秒（5分钟）"
    )
    func_cache_size: int = Field(
        default=1000,
        description="缓存函数结果的最大数量，默认为128，这个缓存大小不宜设置的太大，因为函数缓存是为每个函数单独创建的",
    )
    func_cache_ttl: int = Field(
        default=60, description="缓存函数结果的过期时间，单位为秒，默认为60秒"
    )
    social_cache_size: int = Field(
        default=256,
        description="社交信息缓存的最大数量，默认为256，对每个Bot实例单独缓存社交信息",
    )
    social_cache_ttl: int = Field(
        default=60, description="社交信息缓存的过期时间，单位为秒，默认为60秒"
    )
    download_path: Path = Field(
        default=Path("../files"),
        description="下载文件的存储路径，默认为工作目录下的downloads文件夹",
    )
    data_path: Path = Field(
        default=Path("../datas"),
        description="数据持久化路径，默认为工作目录下的datas文件夹",
    )
    is_deduplicate_message: bool = Field(
        default=True, description="是否启用消息去重功能，默认为True"
    )
    is_deduplicate_image_downloading: bool = Field(
        default=True,
        description="是否启用图片去重功能，默认为True，启用后将避免重复下载相同的图片，但是也会导致后续下载的图片无法覆盖之前下载的同名图片。",
    )


nbconfig = NBHelperConfig()  # 实例化配置类，方便在其他模块中使用
