from typing import List, Sequence
import sqlalchemy
from sqlalchemy import select

from cart.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from cart.infrastructure.persistence.configurations.models import OrderProduct


class OrderProductRepository(SQLAlchemyRepository):
    model = OrderProduct

    async def add_many(self, order_id: int, product_ids: List[int]) -> List[OrderProduct]:
        try:
            products = []
            for i in product_ids:
                products.append(OrderProduct(order_id=order_id, product_id=i))
            self._session.add_all(products)
            return products
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(e)
            raise e

    async def get_many(self, order_id: int) -> Sequence[OrderProduct]:
        try:
            return (await self._session.scalars(select(self.model).where(OrderProduct.order_id == order_id))).unique().all()
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(e)
            raise e

