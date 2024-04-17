from auth.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from auth.infrastructure.persistence.configurations.models import Category


class CategoryRepository(SQLAlchemyRepository):
    _model = Category
