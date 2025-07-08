from pydantic import BaseModel
from typing import List, Optional


class TranslateRequest(BaseModel):
    text: List[str]
    source_language: Optional[str] = "auto"  # 使用 Optional，避免客户端必须传递此参数
    target_language: Optional[str] = "cn"