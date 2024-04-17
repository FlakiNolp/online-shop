from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from api.core.application.abstract_classes import abstract_unit_of_work
from api.core.application.abstract_classes.abstract_specification import AbstractSpecification


class ProductService:
    @staticmethod
    async def get_many_products_with_params(uow: abstract_unit_of_work.AbstractUnitOfWork,
                                            specification: AbstractSpecification.is_satisfied) -> dict:
        try:
            async with uow:
                return await uow.product.get_many(specification)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    async def get_product(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: AbstractSpecification.is_satisfied):
        try:
            async with uow:
                return await uow.product.get_one(specification)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail="Product not found")
