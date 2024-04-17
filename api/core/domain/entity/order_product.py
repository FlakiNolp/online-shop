from api.core.domain.entity.order import Order
from api.core.domain.entity.product import Product


class OrderProduct:
    _id: int
    _order: Order
    _product: Product
