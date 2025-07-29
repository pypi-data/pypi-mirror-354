from pydantic import BaseModel, ConfigDict, Field

from .group_member import GroupMembers


class Group(BaseModel):
    """
    群信息类
    """

    group_all_shut: int = Field(0, description="群全员禁言状态，0为未禁言，1为已禁言")
    group_remark: str | None = Field(
        None, description="群备注，可能为None"
    )  # 群备注可能为None，表示没有备注
    group_id: int = Field(..., description="群ID")
    group_name: str = Field(..., description="群名称")
    member_count: int = Field(..., description="群成员数量")
    max_member_count: int = Field(..., description="群最大成员数量")
    member_list: GroupMembers = Field(
        default_factory=GroupMembers, description="群成员列表"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
