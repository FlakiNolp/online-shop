from auth.core.application.abstract_classes.abstract_specification import AbstractSpecification


class UserFormSpecification(AbstractSpecification):
    @staticmethod
    def is_satisfied(email: str) -> dict:
        return {'email': email}
