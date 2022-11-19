from typing import Optional

from pydantic import BaseModel

from src.models.kink import Kink


class CombinedKink(BaseModel):
    kink_name: str
    user_kink: Optional[Kink]
    link_kink: Optional[Kink]
