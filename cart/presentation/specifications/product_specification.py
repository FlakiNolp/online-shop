from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.presentation.schemas.product import GetProduct


class ProductsFilterSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: GetProduct) -> dict:
        return {'category': filters.category, 'price_from': filters.price_from, "price_to": filters.price_to}


class ProductNameSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: str) -> dict:
        return {'name': filters}


class ProductIdSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: list[int]) -> dict:
        return {'id': filters}
