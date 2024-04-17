import auth.core.domain.schemas.user
from auth.core.application.abstract_classes import abstract_unit_of_work
from auth.core.application.abstract_classes.abstract_specification import AbstractSpecification


class UserService:
    @staticmethod
    async def add(uow: abstract_unit_of_work.AbstractUnitOfWork, user: auth.core.domain.schemas.user.User):
        async with uow:
            user_uuid = await uow.user.add(data=user.model_dump())
            await uow.commit()
            return user_uuid

    @staticmethod
    async def get(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: AbstractSpecification.is_satisfied):
        async with uow:
            res = await uow.user.get(specification)
            await uow.commit()
            return res
