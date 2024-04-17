from auth.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from auth.infrastructure.persistence.configurations.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
