from auth.core.domain.entity.order import Order
from auth.core.domain.entity.product import Product


class OrderProduct:
    _id: int
    _order: Order
    _product: Product
