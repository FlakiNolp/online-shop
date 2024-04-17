from auth.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from auth.infrastructure.persistence.configurations.models import Image


class ImageRepository(SQLAlchemyRepository):
    _model = Image
