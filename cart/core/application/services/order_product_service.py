import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from cart.core.application.abstract_classes import abstract_unit_of_work
from cart.infrastructure.persistence.configurations.models import Order
from cart.core.application.services.user_service import UserService
from cart.presentation.specifications.user_specification import UserUUIDSpecification
from cart.presentation.specifications.order_specification import OrderUserIdSpecification
from cart.presentation.specifications.order_product_specification import OrderProductOrderIdSpecification


class OrderProductService:
    @staticmethod
    async def add_in_order_product(uow: abstract_unit_of_work.AbstractUnitOfWork, order_id: int, products: list[dict]):
        try:
            async with uow:
                order_products = await uow.order_product.add_many(order_id=order_id, product_ids=[int(i['id']) for i in products])
                await uow.flush(order_products)
                await uow.commit()
                return order_products
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    async def get_all_orders(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: OrderUserIdSpecification.is_satisfied):
        try:
            async with uow:
                all_orders = await uow.order.get_many(specification)
                order_products = []
                for i in all_orders:
                    orders = [j.__dict__ for j in await uow.order_product.get_many(order_id=i.id)]
                    for order in orders:
                        order['datetime'] = i.datetime_of_order
                        order['name'] = order['product'].name
                    order_products.append([i.__dict__ for i in await uow.order_product.get_many(order_id=i.id)])
                return order_products
        except SQLAlchemyError as e:
            print(e)
            await uow.rollback()
