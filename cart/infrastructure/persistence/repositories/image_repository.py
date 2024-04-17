from cart.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from cart.infrastructure.persistence.configurations.models import Image


class ImageRepository(SQLAlchemyRepository):
    model = Image
