from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
