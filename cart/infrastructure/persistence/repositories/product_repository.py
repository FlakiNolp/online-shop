import sqlalchemy.exc
from sqlalchemy import select, and_, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from cart.infrastructure.persistence.configurations.models import Product, User, Order, OrderProduct, Category, Image
from cart.infrastructure.persistence.repositories.category_repository import CategoryRepository
from cart.infrastructure.persistence.repositories.image_repository import ImageRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    def __dict_product__(cls, results):
        dictionary = {}
        for i in results:
            if i[0] not in dictionary.keys():
                dictionary[i[0]] = {'name': i[1], 'description': i[2], 'price': i[3], 'quantity': i[4],
                                    'category': i[5],
                                    'images': [i[6]]}
            else:
                dictionary[i[0]]['images'].append(i[6])
        return dictionary

    async def get_many_for_catalog(self, specification: AbstractSpecification.is_satisfied = None) -> Sequence[model]:
        if specification is None:
            specification = {}
        try:
            query = select(self.model.id, self.model.name, self.model.description, self.model.price, self.model.quantity,
                           CategoryRepository.model.name, ImageRepository.model.name).join(CategoryRepository.model).join(
                ImageRepository.model, isouter=True)
            if specification.get('category') is not None:
                query = query.filter(CategoryRepository.model.name == specification['category'])
            if specification.get('price_from') is not None:
                query = query.filter(specification['price_from'] <= self.model.price)
            if specification.get('price_to') is not None:
                query = query.filter(specification['price_to'] >= self.model.price)
            if specification.get('id') is not None:
                query = query.filter(self.model.id.in_(specification['id']))
            return self.__dict_product__((await self._session.execute(query)).all())
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

    async def update(self, quantity: int, specification: AbstractSpecification.is_satisfied) -> Product:
        if specification is None:
            raise ValueError
        try:
            product = (await self._session.scalars(select(self.model).filter_by(**specification))).one()
            product.quantity -= quantity
            self._session.add(product)
            return product
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e
