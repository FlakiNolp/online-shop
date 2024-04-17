import datetime

from cart.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from cart.infrastructure.persistence.configurations.models import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order