from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import OrderProduct


class OrderProductRepository(SQLAlchemyRepository):
    model = OrderProduct
