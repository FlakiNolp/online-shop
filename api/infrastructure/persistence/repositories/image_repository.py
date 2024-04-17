from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import Image


class ImageRepository(SQLAlchemyRepository):
    model = Image
