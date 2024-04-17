from dataclasses import dataclass
from typing import Literal, Optional, List
from uuid import UUID

from cart.core.domain.entity.order import Order


@dataclass
class User:
    _id: int
    _uuid: UUID
    _email: str
    _hashed_password: str
    _role: Literal["Admin", "User"]
    _orders: Optional[List[Order]]
