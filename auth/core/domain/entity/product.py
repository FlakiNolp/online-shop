from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from auth.core.domain.entity.image import Image
from auth.core.domain.entity.category import Category


@dataclass
class Product:
    _id: int
    _name: str
    _description: str
    _price: Decimal("0.00")
    _quantity: int
    _images: List[Image]
    _category: List[Category]

