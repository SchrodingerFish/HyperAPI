from pydantic import BaseModel
from typing import Optional

class SearchQuery(BaseModel):
    num: Optional[int] = 10  # Number of results to return (default: 10)
    page: Optional[int] = 1
    q: str  # Search query
    gl: str = "cn"  # Geo location (default: China)
    hl: str = "zh-cn"  # Human language (default: Simplified Chinese)
    tbs: Optional[str] = "qdr:h"  # Time-based search filter (Optional, default: last hour)