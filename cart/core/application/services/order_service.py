import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from cart.core.application.abstract_classes import abstract_unit_of_work, abstract_specification
from cart.infrastructure.persistence.configurations.models import Order
from cart.core.application.services.user_service import UserService
from cart.core.application.services.order_product_service import OrderProductService
from cart.core.application.services.product_service import ProductService
from cart.presentation.specifications.user_specification import UserUUIDSpecification
from cart.presentation.specifications.product_specification import ProductIdSpecification


class OrderService:
    @staticmethod
    async def create_new_order(uow: abstract_unit_of_work.AbstractUnitOfWork, user_uuid: str, products: list[dict]) -> Order:
        try:
            async with uow:
                user_id = (await UserService.get_user_by_uuid(uow, UserUUIDSpecification.is_satisfied(uuid=user_uuid))).get('id')
                order = await uow.order.add({'datetime_of_order': datetime.datetime.now(), 'user_id': user_id})
                await uow.flush([order])
                await uow.commit()
                await OrderProductService.add_in_order_product(uow, order.id, products)
                for product in products:
                    await ProductService.update_number_of_quantity(uow, quantity=product['quantity'], specification=ProductIdSpecification.is_satisfied(int(product['id'])))
                await uow.commit()
                return order
        except SQLAlchemyError as e:
            await uow.rollback()
            raise e

    @staticmethod
    async def get_all_orders(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: abstract_specification.AbstractSpecification) -> List[dict]:
        try:
            async with uow:
                return await uow.order_product.get_many(specification)
        except SQLAlchemyError as e:
            await uow.rollback()
            print(e)