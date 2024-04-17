from auth.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from auth.infrastructure.persistence.configurations.models import Order


class OrderRepository(SQLAlchemyRepository):
    _model = Order
