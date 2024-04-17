import asyncio
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from cart.core.application.abstract_classes import abstract_unit_of_work
from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.infrastructure.persistence.configurations.models import Base
from cart.infrastructure.persistence.configurations.models import Product


class ProductService:
    @staticmethod
    async def get_many_products_with_params(uow: abstract_unit_of_work.AbstractUnitOfWork,
                                            specification: AbstractSpecification.is_satisfied):
        try:
            async with uow:
                return await uow.product.get_many_for_catalog(specification)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    async def get_product(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: AbstractSpecification.is_satisfied) -> dict:
        try:
            async with uow:
                res = await uow.product.get_one(specification)
                return res
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail="Product not found")

    @staticmethod
    async def update_number_of_quantity(uow: abstract_unit_of_work.AbstractUnitOfWork, quantity: int, specification: AbstractSpecification.is_satisfied) -> Product:
        try:
            async with uow:
                product = await uow.product.update(quantity, specification)
                await uow.flush([product])
                await uow.commit()
                return product
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail="Product not found")

    @staticmethod
    async def check_many_product_with_quantity(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: AbstractSpecification.is_satisfied):
        # try:
        #     async with uow:
        #         queries = set()
        #         for id in specification.keys():
        #
        #             products = await uow.product.get_many_for_catalog(specification=specification)
        #             if len(specification.)
        ...
