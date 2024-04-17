from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.presentation.schemas.product import GetProduct


class CollectionId(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: int) -> dict:
        return {'product_id': filters}
