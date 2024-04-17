from sqlalchemy.exc import SQLAlchemyError

from cart.core.application.abstract_classes import abstract_unit_of_work


class CategoryService:
    @staticmethod
    async def get_categories(uow: abstract_unit_of_work.AbstractUnitOfWork):
        try:
            async with uow:
                return await uow.category.get_many()
        except SQLAlchemyError as e:
            raise e
