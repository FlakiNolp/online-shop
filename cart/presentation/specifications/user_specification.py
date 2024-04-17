from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification


class UserFormSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(email: str) -> dict:
        return {'email': email}


class UserUUIDSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(uuid: str) -> dict:
        return {'uuid': uuid}
