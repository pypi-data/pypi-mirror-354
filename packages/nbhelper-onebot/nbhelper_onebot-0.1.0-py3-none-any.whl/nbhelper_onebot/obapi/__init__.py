from nonebot.adapters.onebot.v11 import Bot

from src.nbhelper_onebot.errors import FetchError


async def get_group_member_info(bot: Bot, group_id: int, user_id: int, no_cache: bool = False) -> dict:
    """获取群成员信息"""
    member_info = await bot.call_api("get_group_member_info", group_id=group_id, user_id=user_id, no_cache=no_cache)
    if not member_info:
        raise FetchError(f"Failed to fetch member info for user {user_id} in group {group_id}.")
    return member_info


async def get_group_file_url(bot: Bot, group_id: int, file_id: str) -> str:
    """从QQ服务器获取群文件的下载链接"""
    file_info = await bot.call_api(
        "get_group_file_url", group_id=group_id, file_id=file_id
    )
    if not file_info["url"]:
        raise FetchError(f"Failed to fetch file URL for file_id {file_id} in group {group_id}.")
    return file_info["url"]


async def get_group_list(bot: Bot, no_cache: bool = False) -> list[dict]:
    """获取群列表"""
    group_list = await bot.call_api("get_group_list", no_cache=no_cache)
    if not group_list:
        raise FetchError("Failed to fetch group list.")
    return group_list


async def get_friend_list(bot: Bot, no_cache: bool = False) -> list[dict]:
    """获取好友列表"""
    friend_list = await bot.call_api("get_friend_list", no_cache=no_cache)
    if not friend_list:
        raise FetchError("Failed to fetch friend list.")
    return friend_list


async def get_group_member_list(bot: Bot, group_id: int, no_cache: bool = False) -> list[dict]:
    """获取群成员列表"""
    member_list = await bot.call_api("get_group_member_list", group_id=group_id, no_cache=no_cache)
    if not member_list:
        raise FetchError(f"Failed to fetch member list for group {group_id}.")
    return member_list


async def delete_friend(bot: Bot, friend_id: int, temp_block: bool = False, temp_both_del: bool = False):
    """删除好友"""
    res = await bot.call_api(
        "delete_friend",
        user_id=bot.self_id,
        friend_id=friend_id,
        temp_block=temp_block,
        temp_both_del=temp_both_del,
    )
    if res["result"] == 0:
        return True
    else:
        return False


async def set_group_leave(bot: Bot, group_id: int):
    """退出群聊"""
    await bot.call_api("set_group_leave", group_id=group_id)
