from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification


class OrderProductOrderIdSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(filters: int) -> dict:
        return {'order_id': filters}
