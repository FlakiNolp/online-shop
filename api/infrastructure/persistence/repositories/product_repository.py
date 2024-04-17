import sqlalchemy.exc
from sqlalchemy import select, Sequence

from api.core.application.abstract_classes.abstract_specification import AbstractSpecification
from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import Product
from api.infrastructure.persistence.repositories.category_repository import CategoryRepository
from api.infrastructure.persistence.repositories.image_repository import ImageRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    @classmethod
    def __dict__(cls, results):
        dictionary = {}
        for i in results:
            if i[0] not in dictionary.keys():
                dictionary[i[0]] = {'name': i[1], 'description': i[2], 'price': i[3], 'quantity': i[4], 'category': i[5],
                                    'images': [i[6]]}
            else:
                dictionary[i[0]]['images'].append(i[6])
        return dictionary

    async def get_many(self, specification: AbstractSpecification.is_satisfied = None) -> dict:
        if specification is None:
            specification = {}
        try:
            query = select(self.model.id, self.model.name, self.model.description, self.model.price, self.model.quantity,
                           CategoryRepository.model.name, ImageRepository.model.name).join(
                CategoryRepository.model).join(
                ImageRepository.model, isouter=True)
            if specification['category'] is not None:
                query = query.filter(CategoryRepository.model.name == specification['category'])
            if specification['price_from'] is not None:
                query = query.filter(specification['price_from'] <= self.model.price)
            if specification['price_to'] is not None:
                query = query.filter(specification['price_to'] >= self.model.price)
            return self.__dict__((await self._session.execute(query)).all())
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e
