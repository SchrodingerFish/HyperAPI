from pydantic import BaseModel
from typing import Any, Optional


class Response(BaseModel):
    code: int       # 响应状态码
    message: str    # 响应消息
    data: Optional[Any] = None  # 响应数据，默认为 None

    @staticmethod
    def success(data: Any, message: str = "Success"):
        """
        创建一个成功的响应模型
        """
        return Response(
            code=200,
            message=message,
            data=data
        )

    @staticmethod
    def error(code: int, message: str, data: Optional[Any] = None):
        """
        创建一个错误的响应模型
        """
        return Response(
            code=code,
            message=message,
            data=data
        )
