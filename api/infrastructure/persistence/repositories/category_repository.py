from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import List


from api.core.application.abstract_classes.abstract_specification import AbstractSpecification
from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category

    async def get_many(self, specification: AbstractSpecification.is_satisfied = None) -> List[dict]:
        if specification is None:
            specification = {}
        try:
            return self.__dict__((await self._session.scalars(select(self.model.name).filter_by(**specification))).unique().all())
        except SQLAlchemyError as e:
            print(e)
