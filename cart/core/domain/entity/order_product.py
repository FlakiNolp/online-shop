from cart.core.domain.entity.order import Order
from cart.core.domain.entity.product import Product


class OrderProduct:
    _id: int
    _order: Order
    _product: Product
