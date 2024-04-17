from auth.infrastructure.persistence.repositories.sqlalchemy_repository import SQLAlchemyRepository
from auth.infrastructure.persistence.configurations.models import OrderProduct


class OrderProductRepository(SQLAlchemyRepository):
    _model = OrderProduct
