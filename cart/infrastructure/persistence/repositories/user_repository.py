from cart.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from cart.infrastructure.persistence.configurations.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
