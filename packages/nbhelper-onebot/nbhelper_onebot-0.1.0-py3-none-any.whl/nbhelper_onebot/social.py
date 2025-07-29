import asyncio

from cachetools import TTLCache
from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel, Field

from .configs import nbconfig
from .errors import FetchError
from .models import Friend, Group, GroupMember, GroupMembers
from .obapi import get_group_list, get_friend_list, delete_friend, get_group_member_list, set_group_leave


class Social(BaseModel):
    """
    社交管理类，用于管理好友和群信息
    """

    _bot: Bot = None  # 存放Bot实例
    _social_cache = TTLCache(
        maxsize=nbconfig.social_cache_size, ttl=nbconfig.social_cache_ttl
    )  # 社交信息缓存
    is_initialized: bool = Field(default=False, description="是否已初始化")
    friends: list[Friend] = Field(default_factory=list, description="好友列表")
    groups: list[Group] = Field(default_factory=list, description="群列表")

    class Config:
        arbitrary_types_allowed = True
        ignored_types = (Bot,)  # 忽略 Bot 类型字段的序列化和验证

    async def set_bot(self, bot: Bot):
        """设置Bot实例"""
        self._bot = bot
        return self

    async def update_all_friends(self) -> None:
        """更新好友列表"""
        friend_list = await get_friend_list(self._bot)
        self.friends = [Friend(**f) for f in friend_list]

    async def update_all_friends_without_cache(self) -> None:
        """更新好友列表，不使用缓存"""
        friend_list = await get_friend_list(self._bot, no_cache=True)
        self.friends = [Friend(**f) for f in friend_list]

    async def update_all_groups(self) -> None:
        """更新群列表"""
        group_list = await get_group_list(self._bot)
        groups = [Group(**g) for g in group_list]
        # 异步获取每个群的成员列表
        tasks = [self.fetch_member_list(group) for group in groups]
        member_lists = await asyncio.gather(*tasks)
        # 用 model_copy 更新 member_list 字段
        updated_groups = [
            group.model_copy(update={"member_list": member_list})
            for group, member_list in zip(groups, member_lists)
        ]
        self.groups = updated_groups

    async def update_all_groups_without_cache(self) -> None:
        """更新群列表，不使用缓存"""
        group_list = await get_group_list(self._bot, no_cache=True)
        groups = [Group(**g) for g in group_list]
        tasks = [self.fetch_member_list_without_cache(group) for group in groups]
        member_lists = await asyncio.gather(*tasks)
        updated_groups = [
            group.model_copy(update={"member_list": member_list})
            for group, member_list in zip(groups, member_lists)
        ]
        self.groups = updated_groups

    async def get_friend(self, user_id: int | str) -> Friend | None:
        """获取指定用户ID的好友信息"""

        user_id = int(user_id)  # 确保user_id是整数
        if user_id in self._social_cache:
            return self._social_cache[f"friend_{user_id}"]
        for friend in self.friends:
            if friend.user_id == user_id:
                self._social_cache[f"friend_{user_id}"] = friend
                return friend
        return None

    async def get_friend_without_cache(self, user_id: int | str) -> Friend | None:
        """不使用缓存，获取指定用户ID的好友信息"""
        for friend in self.friends:
            if friend.user_id == int(user_id):
                return friend
        return None

    async def get_group(self, group_id: int | str) -> Group | None:
        """获取指定群ID的群信息"""
        group_id = int(group_id)  # 确保group_id是整数
        if group_id in self._social_cache:
            return self._social_cache[f"group_{group_id}"]
        for group in self.groups:
            if group.group_id == group_id:
                self._social_cache[f"group_{group_id}"] = group
                return group
        return None

    async def get_group_without_cache(self, group_id: int | str) -> Group | None:
        """不使用缓存，获取指定群ID的群信息"""
        for group in self.groups:
            if group.group_id == int(group_id):
                return group
        return None

    async def delete_friend(
            self, friends: list[Friend | int | str] | Friend | int | str, temp_block=False, temp_both_del=False
    ) -> bool:
        """删除好友"""
        try:
            if not isinstance(friends, list):
                friends = [friends]
            for friend in friends:
                res = await delete_friend(self._bot,
                                          friend_id=friend.user_id if isinstance(friend, Friend) else int(friend),
                                          temp_block=temp_block, temp_both_del=temp_both_del)
                if res["result"] == 0:
                    # 删除成功后从缓存中移除好友
                    if isinstance(friend, Friend):
                        self._social_cache.pop(friend.user_id, None)
                    else:
                        self._social_cache.pop(int(friend), None)
                    # 从好友列表中移除
                    self.friends = [f for f in self.friends if
                                    f.user_id != (friend.user_id if isinstance(friend, Friend) else int(friend))]
                    return True
                else:
                    return False
            return False
        except Exception as e:
            raise Exception(f"Failed to delete friend {self.user_id}: {e}")

    async def fetch_member_list(self, group: Group | int | str):
        """从QQ服务器获取群成员列表"""
        # 使用缓存获取群成员列表
        member_list = await get_group_member_list(
            self._bot, group_id=group.group_id if isinstance(group, Group) else int(group)
        )
        if member_list:
            # 将获取到的成员列表转换为GroupMembers对象
            res = GroupMembers([GroupMember(**m) for m in member_list])
            return res
        else:
            raise FetchError("Failed to fetch member list for group.")

    async def fetch_member_list_without_cache(self, group: Group | int | str):
        """从QQ服务器获取群成员列表，不使用缓存"""
        member_list = await get_group_member_list(
            self._bot, group_id=group.group_id if isinstance(group, Group) else int(group), no_cache=True
        )
        if member_list:
            # 将获取到的成员列表转换为GroupMembers对象
            res = GroupMembers([GroupMember(**m) for m in member_list])
            return res
        else:
            raise FetchError("Failed to fetch member list for group.")

    async def leave_group(self, group: Group | int | str) -> None:
        """退出群聊"""
        await set_group_leave(self._bot, group_id=group.group_id if isinstance(group, Group) else int(group))
        # 从缓存中移除群信息
        group_id = group.group_id if isinstance(group, Group) else int(group)
        self._social_cache.pop(f"group_{group_id}", None)
        # 从群列表中移除
        self.groups = [g for g in self.groups if g.group_id != group_id]


class SocialManager(dict[str, Social]):
    """
    社交管理器字典，用于存储每个Bot的社交管理类
    """

    async def add(self, bot: Bot) -> bool:
        """添加一个Bot的社交管理类"""
        if bot.self_id not in self:
            try:
                social = await Social().set_bot(bot)
                self[bot.self_id] = social
                await social.update_all_friends()
                await social.update_all_groups()
                social.is_initialized = True  # 标记社交管理类已初始化

                return True
            except Exception as e:
                raise e
        return False

    async def add_without_cache(self, bot: Bot) -> bool:
        """添加一个Bot的社交管理类"""
        if bot.self_id not in self:
            try:
                social = await Social().set_bot(bot)
                self[bot.self_id] = social  # 将社交类添加到字典中
                await social.update_all_friends_without_cache()
                await social.update_all_groups_without_cache()
                social.is_initialized = True  # 标记社交管理类已初始化
                return True
            except Exception as e:
                raise e
        return False

    async def get_social(self, bot: Bot | str | int) -> Social | None:
        """获取指定Bot的社交管理类，未初始化时阻塞等待，未找到时最多重试3次"""
        if isinstance(bot, Bot):
            bot = bot.self_id
        elif isinstance(bot, int):
            bot = str(bot)

        for _ in range(3):
            if bot in self:
                social = self[bot]
                while not social.is_initialized:
                    await asyncio.sleep(0.1)  # 阻塞直到初始化完成
                return social
            await asyncio.sleep(1)
        raise FetchError(f"Social manager for bot {bot} not found after 3 retries.")

    def get_social_without_wait(self, bot: Bot | str | int) -> Social | None:
        """获取指定Bot的社交管理类，不等待社交管理类初始化完成，但可能产生不安全的结果"""
        if isinstance(bot, Bot):
            bot = bot.self_id
        elif isinstance(bot, int):
            bot = str(bot)
        return self.get(bot)
