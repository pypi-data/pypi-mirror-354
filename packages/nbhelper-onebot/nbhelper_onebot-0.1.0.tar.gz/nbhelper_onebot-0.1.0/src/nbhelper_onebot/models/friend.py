from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Friend(BaseModel):
    """
    好友信息类
    """

    birthday_year: int | None = Field(0, description="出生年份")
    birthday_month: int | None = Field(0, description="出生月份")
    birthday_day: int | None = Field(0, description="出生日")
    user_id: int = Field(..., description="用户ID")
    age: int | None = Field(0, description="年龄")
    phone_num: str | None = Field("", description="手机号码")
    email: str | None = Field("", description="电子邮箱")
    category_id: int | None = Field(0, description="好友分组ID")
    nickname: str = Field(..., description="好友昵称")
    remark: str | None = Field("", description="好友备注")
    sex: Literal["male", "female", "unknown"] = Field("unknown", description="性别")
    level: int = Field(0, description="好友等级")

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
