from api.core.application.abstract_classes.abstract_specification import AbstractSpecification
from api.presentation.schemas.product import GetProduct


class ProductsFilterSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: GetProduct) -> dict:
        return {'category': filters.category, 'price_from': filters.price_from, "price_to": filters.price_to}


class ProductNameSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: str) -> dict:
        return {'name': filters}
