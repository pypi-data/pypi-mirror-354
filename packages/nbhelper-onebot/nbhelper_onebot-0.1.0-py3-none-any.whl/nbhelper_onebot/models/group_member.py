from datetime import datetime
from typing import Literal

from cachetools import func
from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel, ConfigDict, Field

from ..configs import nbconfig
from ..obapi import get_group_member_info


class GroupMember(BaseModel):
    """
    群成员信息类
    """

    group_id: int = Field(..., description="群ID")
    user_id: int = Field(..., description="用户ID")
    nickname: str = Field(..., description="用户昵称")
    card: str | None = Field("", description="群名片")
    sex: Literal["male", "female", "unknown"] = Field("unknown", description="性别")
    age: int = Field(0, description="年龄")
    area: str | None = Field("", description="地区")
    level: str | None = Field("", description="等级")
    qq_level: int = Field(0, description="QQ等级")
    join_time: int = Field(..., description="入群时间戳")
    last_sent_time: int = Field(..., description="最后发言时间戳")
    title_expire_time: int = Field(0, description="头衔过期时间戳")
    unfriendly: bool = Field(False, description="是否不友好")
    card_changeable: bool = Field(False, description="是否可以修改群名片")
    is_robot: bool = Field(False, description="是否为机器人")
    shut_up_timestamp: int = Field(0, description="禁言时间戳")
    role: Literal["owner", "admin", "member"] = Field(
        "member", description="群成员角色，owner为群主，admin为管理员，member为普通成员"
    )
    title: str | None = Field(
        None, description="群成员头衔，可能为None"
    )  # 头衔可能为None，表示没有头衔

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    # 添加时间戳转换方法
    async def join_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.join_time)

    async def last_sent_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.last_sent_time)

    async def fetch_full_member_info(self, bot: Bot) -> "GroupMember":
        """从QQ服务器获取完整的群成员信息"""
        member_info = await get_group_member_info(bot, group_id=self.group_id, user_id=self.user_id)
        if not member_info:
            raise ValueError(
                f"Failed to fetch member info for user_id {self.user_id} in group {self.group_id}."
            )
        # 生成一个新的 GroupMember 实例
        return GroupMember(**member_info)

    async def fetch_full_member_info_without_cache(self, bot: Bot) -> "GroupMember":
        """从QQ服务器获取完整的群成员信息，不使用缓存"""
        member_info = await get_group_member_info(bot, group_id=self.group_id, user_id=self.user_id, no_cache=True)
        if not member_info:
            raise ValueError(
                f"Failed to fetch member info for user_id {self.user_id} in group {self.group_id}."
            )
        # 生成一个新的 GroupMember 实例
        return GroupMember(**member_info)


class GroupMembers(tuple[GroupMember]):
    """
    群成员列表类
    """

    def __new__(cls, members=None):
        if members is None:
            members = []
        return super().__new__(cls, members)

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def get_member_by_id(self, user_id: int) -> GroupMember | None:
        """根据用户ID获取群成员信息"""
        for member in self:
            if member.user_id == user_id:
                return member
        return None

    async def get_member_by_id_without_cache(self, user_id: int) -> GroupMember | None:
        """不使用缓存，根据用户ID获取群成员信息"""
        for member in self:
            if member.user_id == user_id:
                return member
        return None

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def get_members_by_role(
            self, role: Literal["owner", "admin", "member"]
    ) -> list[GroupMember]:
        """根据角色获取群成员列表"""
        return [member for member in self if member.role == role]

    async def get_members_by_role_without_cache(
            self, role: Literal["owner", "admin", "member"]
    ) -> list[GroupMember]:
        """不使用缓存，根据角色获取群成员列表"""
        return [member for member in self if member.role == role]

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def is_in_group(self, user_id: int) -> bool:
        """检查用户是否在群中"""
        return any(member.user_id == user_id for member in self)

    async def is_in_group_without_cache(self, user_id: int) -> bool:
        """不使用缓存，检查用户是否在群中"""
        return any(member.user_id == user_id for member in self)

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def get_owner(self):
        """获取群主信息"""
        for member in self:
            if member.role == "owner":
                return member
        return None

    async def get_owner_without_cache(self):
        """不使用缓存，获取群主信息"""
        for member in self:
            if member.role == "owner":
                return member
        return None

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def get_admins(self) -> list[GroupMember]:
        """获取群管理员列表"""
        return [member for member in self if member.role == "admin"]

    async def get_admins_without_cache(self) -> list[GroupMember]:
        """不使用缓存，获取群管理员列表"""
        return [member for member in self if member.role == "admin"]

    @func.ttl_cache(nbconfig.func_cache_size, ttl=nbconfig.func_cache_ttl)
    async def get_admins_and_owner(self) -> list[GroupMember]:
        """获取群管理员和群主列表"""
        return [member for member in self if member.role in ["admin", "owner"]]

    async def get_admins_and_owner_without_cache(self) -> list[GroupMember]:
        """不使用缓存，获取群管理员和群主列表"""
        return [member for member in self if member.role in ["admin", "owner"]]
