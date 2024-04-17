from api.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from api.infrastructure.persistence.configurations.models import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order
