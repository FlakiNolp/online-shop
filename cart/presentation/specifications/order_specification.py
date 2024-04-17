from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification


class ProductIdSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: int) -> dict:
        return {'id': filters}


class OrderUserIdSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: int) -> dict:
        return {'user_id': filters}