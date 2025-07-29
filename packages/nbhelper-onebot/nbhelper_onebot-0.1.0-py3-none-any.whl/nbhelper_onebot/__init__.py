import asyncio
import threading
from pathlib import Path

from cachetools import TTLCache
from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, GroupMessageEvent

from .configs import NBHelperConfig, nbconfig
from .obapi import get_group_file_url
from .social import SocialManager
from .utils import download, download_async, ensure_dir, has_file


class NBHelper:
    config: NBHelperConfig  # 配置项
    _social_manager: SocialManager  # 社交管理器，用于管理好友和群信息
    _message_cache: TTLCache  # 消息缓存，使用TTLCache实现自动过期
    _cache_lock: threading.RLock  # 线程锁，保证缓存操作的线程安全

    def init(self, no_cache: bool = False):
        """初始化NBHelper实例"""
        self.config = nbconfig

        # 初始化各项功能
        self._init_message_cache()
        self._init_paths()
        self._init_social_manager(no_cache)

    def _init_message_cache(self):
        """初始化消息缓存"""
        # 使用TTLCache替代LRUCache，自动过期旧消息
        self._message_cache = TTLCache(
            maxsize=self.config.message_cache_size,
            ttl=self.config.message_cache_ttl,  # 5分钟过期
        )
        # 添加线程锁保证线程安全
        self._cache_lock = threading.RLock()

    def _init_paths(self):
        """初始化文件和数据存储路径"""
        # 这里可以添加代码来创建必要的目录结构
        ensure_dir(self.config.download_path)
        ensure_dir(self.config.data_path)

    def _init_social_manager(self, no_cache: bool = False):
        """初始化社交管理器"""
        self._social_manager = SocialManager()

        driver = get_driver()

        @driver.on_bot_connect
        async def _(bot: Bot):
            """当Bot连接时，添加Bot的社交管理类"""
            logger.debug(f"Adding social manager for bot {bot.self_id}")
            if no_cache:
                if not await self._social_manager.add_without_cache(bot):  # 不使用缓存
                    logger.error(f"Failed to add social manager for bot {bot.self_id}.")
                else:
                    logger.debug("Social manager added successfully.")
            else:
                if not await self._social_manager.add(bot):
                    logger.error(f"Failed to add social manager for bot {bot.self_id}.")
                else:
                    logger.debug("Social manager added successfully.")

        @driver.on_bot_disconnect
        async def _(bot: Bot):
            """当Bot断开连接时，移除Bot的社交管理类"""
            logger.info(f"Removing social manager for bot {bot.self_id}.")
            if bot.self_id in self._social_manager:
                del self._social_manager[bot.self_id]
                logger.debug(f"Removed social manager for bot {bot.self_id}.")
            else:
                logger.warning(f"Social manager for bot {bot.self_id} not found.")

    def message_deduplication(self, message_event: MessageEvent) -> bool:
        """检查消息是否重复，未重复返回True，重复返回False"""
        if not self.config.is_deduplicate_message:
            return True  # 如果未启用消息去重功能，直接返回True
        key = message_event.message_id
        with self._cache_lock:
            if key in self._message_cache:
                return False
            self._message_cache[key] = True  # 缓存消息ID，标记消息
            return True

    @staticmethod
    def has_image_segment(msg: Message | MessageEvent) -> bool:
        """检查消息中是否包含图片类型的元素"""
        if isinstance(msg, MessageEvent):
            msg = msg.message
        # 遍历消息，找到其中的图片类型元素
        for segment in msg:
            if segment.type == "image":
                return True
        return False

    @staticmethod
    def has_file_segment(msg: Message | MessageEvent) -> bool:
        """检查消息中是否包含文件类型的元素"""
        if isinstance(msg, MessageEvent):
            msg = msg.message
        # 遍历消息，找到其中的文件类型元素
        for segment in msg:
            if segment.type == "file":
                return True
        return False

    def download_images(self, msg: Message | MessageEvent) -> list[Path]:
        """下载消息中的图片，返回下载的图片文件路径列表"""
        logger.debug(f"Downloading images from message: {msg.message_id}.")

        if isinstance(msg, MessageEvent):
            msg = msg.message
        # 遍历消息，找到其中的图片类型元素并下载
        file_path_list: list[Path] = []
        for segment in msg:
            if segment.type == "image":
                # 这里可以添加下载图片的逻辑
                url = segment.data.get("url", "")
                file = segment.data.get("file", "image.jpg")
                if (
                        not has_file(file, self.config.download_path)
                        or not self.config.is_deduplicate_image_downloading
                ):  # 如果文件不存在或未启用去重
                    file_path = download(
                        url,
                        self.config.download_path,
                        file,
                    )
                    if file_path:
                        file_path_list.append(file_path)
                else:
                    logger.debug(f"File already exists, skipping download: {file}.")
        return file_path_list

    async def download_images_async(self, msg: Message | MessageEvent) -> list[Path]:
        """异步并发下载消息中的图片，返回下载的图片文件路径列表"""
        logger.debug(
            f"Downloading images asynchronously from message: {msg.message_id}."
        )
        if isinstance(msg, MessageEvent):
            msg = msg.message

        # 遍历消息，找到其中的图片类型元素并记录
        file_list: list[dict[str, str]] = []  # 存储下载的文件信息，键为文件名，值为URL
        seen_filenames: set[str] = set()  # 记录已处理的文件名，用于去重

        for segment in msg:
            if segment.type == "image":
                url = segment.data.get("url", "")
                filename = segment.data.get("file", "image.jpg")

                # 检查文件名是否已存在，仅在启用去重时进行检查
                if (
                        filename in seen_filenames
                        and self.config.is_deduplicate_image_downloading
                ):
                    logger.debug(f"Filename already exists, skipping: {filename}.")
                    continue

                # 添加文件名到集合中
                seen_filenames.add(filename)

                # 添加到下载列表
                file_list.append({"url": url, "filename": filename})

        # 如果没有需要下载的图片，直接返回空列表
        if not file_list:
            return []

        # 异步并发下载所有图片
        download_tasks = [
            download_async(
                url=item["url"],
                download_path=self.config.download_path,
                filename=item["filename"],
            )
            for item in file_list
        ]

        # 执行并发下载并收集结果
        downloaded_files = await asyncio.gather(*download_tasks)

        # 过滤掉下载失败的情况（None）
        return [file_path for file_path in downloaded_files if file_path is not None]

    async def download_group_file(self, event: GroupMessageEvent) -> Path | None:
        """下载消息中的文件，返回下载的文件路径，如果没有文件则返回None"""
        logger.debug(f"Downloading file from message: {event.message_id}.")
        # 遍历消息，找到其中的文件类型元素并下载
        if self.has_file_segment(event):
            for segment in event.message:
                if segment.type == "file":
                    file = segment.data["file"]  # 获取文件的文件名称
                    file_id = segment.data["file_id"]  # 获取文件的文件信息
                    # 　检查文件是否已存在
                    if not has_file(file, self.config.download_path):
                        url = await get_group_file_url(event.group_id, file_id)
                        if not url:
                            logger.error(f"Failed to get file URL for {file}.")
                            return None
                        file_path = await download_async(url, self.config.download_path, file)
                        if file_path:
                            logger.debug(f"Downloaded file: {file_path}.")
                            return file_path
                        else:
                            logger.error(f"Failed to download file: {file}.")
                    break
        return None

    def get_social(self, bot: Bot | str | int):
        """获取指定Bot的社交管理类"""
        return self._social_manager.get_social(bot)

    def get_social_without_wait(self, bot: Bot | str | int):
        """获取指定Bot的社交管理类，不等待社交管理类初始化完成"""
        return self._social_manager.get_social_without_wait(bot)


nbhelper = NBHelper()  # 全局唯一实例，便于在插件中直接使用
